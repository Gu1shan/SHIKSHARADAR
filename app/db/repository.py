"""
Repository for SQLite persistence in Shiksha Radar.

Provides upsert/append semantics for multi-assessment uploads and
persistence of profiles, gaps, interventions, and outcomes.
"""
import json
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import List, Optional

import pandas as pd

from app.db.schema import init_db
from app.analytics.profiler import ConceptProfile, LearningGap

DEFAULT_DB_PATH = "shiksha_radar.db"


class Repository:
    """Thin data-access layer over sqlite3."""

    def __init__(self, db_path: str = DEFAULT_DB_PATH):
        self.db_path = str(db_path)
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("PRAGMA foreign_keys = ON")
        init_db(self.conn)

    def close(self) -> None:
        self.conn.close()

    # ------------------------------------------------------------------
    # Raw data: students / questions / responses (append-or-ignore)
    # ------------------------------------------------------------------

    def save_students(self, students_df: pd.DataFrame) -> int:
        rows = [
            (r.student_id, int(r.grade), str(r.section))
            for r in students_df.itertuples()
        ]
        self.conn.executemany(
            "INSERT OR IGNORE INTO students (student_id, grade, section) VALUES (?, ?, ?)",
            rows,
        )
        self.conn.commit()
        return len(rows)

    def save_questions(self, questions_df: pd.DataFrame) -> int:
        rows = [
            (
                r.question_id,
                getattr(r, "text", None),
                r.concept,
                getattr(r, "sub_concept", None),
                int(r.difficulty) if pd.notna(getattr(r, "difficulty", None)) else None,
                getattr(r, "expected_answer", None),
            )
            for r in questions_df.itertuples()
        ]
        self.conn.executemany(
            """INSERT OR IGNORE INTO questions
               (question_id, text, concept, sub_concept, difficulty, expected_answer)
               VALUES (?, ?, ?, ?, ?, ?)""",
            rows,
        )
        self.conn.commit()
        return len(rows)

    def save_responses(self, responses_df: pd.DataFrame) -> int:
        """Append responses; duplicates (by response_id) are ignored."""
        before = self._count("responses")
        rows = [
            (
                r.response_id,
                r.student_id,
                r.assessment_id,
                r.question_id,
                str(r.student_answer),
                1 if bool(r.is_correct) else 0,
                r.error_type if pd.notna(r.error_type) else None,
                str(r.created_at),
            )
            for r in responses_df.itertuples()
        ]
        self.conn.executemany(
            """INSERT OR IGNORE INTO responses
               (response_id, student_id, assessment_id, question_id,
                student_answer, is_correct, error_type, created_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            rows,
        )
        self.conn.commit()
        return self._count("responses") - before

    def load_all_data(self):
        """Load students, questions, concept_map, responses as DataFrames."""
        students = pd.read_sql_query("SELECT * FROM students", self.conn)
        questions = pd.read_sql_query("SELECT * FROM questions", self.conn)
        responses = pd.read_sql_query("SELECT * FROM responses", self.conn)
        if not responses.empty:
            responses["is_correct"] = responses["is_correct"].astype(bool)
        concept_map = questions[["question_id", "concept", "sub_concept"]].drop_duplicates()
        return students, questions, concept_map, responses

    # ------------------------------------------------------------------
    # Profiles & gaps
    # ------------------------------------------------------------------

    def save_profiles(self, profiles: List[ConceptProfile]) -> int:
        now = datetime.now().isoformat()
        for p in profiles:
            self.conn.execute(
                """INSERT INTO concept_profiles
                   (student_id, concept, total_attempts, total_errors, error_breakdown,
                    assessments_with_errors, first_error_date, last_error_date,
                    trend, confidence, error_rates, assessment_dates, updated_at)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                   ON CONFLICT(student_id, concept) DO UPDATE SET
                     total_attempts=excluded.total_attempts,
                     total_errors=excluded.total_errors,
                     error_breakdown=excluded.error_breakdown,
                     assessments_with_errors=excluded.assessments_with_errors,
                     first_error_date=excluded.first_error_date,
                     last_error_date=excluded.last_error_date,
                     trend=excluded.trend,
                     confidence=excluded.confidence,
                     error_rates=excluded.error_rates,
                     assessment_dates=excluded.assessment_dates,
                     updated_at=excluded.updated_at""",
                (
                    p.student_id, p.concept, p.total_attempts, p.total_errors,
                    json.dumps(p.error_breakdown), p.assessments_with_errors,
                    p.first_error_date, p.last_error_date, p.trend, p.confidence,
                    json.dumps(p.error_rates), json.dumps(p.assessment_dates), now,
                ),
            )
        self.conn.commit()
        return len(profiles)

    def save_gaps(self, gaps: List[LearningGap]) -> int:
        """Insert new gaps (deduplicated by student+concept+detected_at)."""
        count = 0
        for g in gaps:
            cur = self.conn.execute(
                """INSERT OR IGNORE INTO learning_gaps
                   (student_id, concept, sub_concept, dominant_error, evidence_count,
                    assessments_count, confidence, trend, detected_at, status)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    g.student_id, g.concept, g.sub_concept, g.dominant_error,
                    g.evidence_count, g.assessments_count, g.confidence, g.trend,
                    g.detected_at, g.status,
                ),
            )
            count += cur.rowcount
        self.conn.commit()
        return count

    def get_gaps(self, status: Optional[str] = None) -> List[dict]:
        query = "SELECT * FROM learning_gaps"
        params = ()
        if status:
            query += " WHERE status = ?"
            params = (status,)
        query += " ORDER BY confidence DESC"
        return [dict(r) for r in self.conn.execute(query, params).fetchall()]

    def update_gap_status(self, gap_id: int, status: str) -> None:
        self.conn.execute(
            "UPDATE learning_gaps SET status = ? WHERE gap_id = ?", (status, gap_id)
        )
        self.conn.commit()

    # ------------------------------------------------------------------
    # Interventions & outcomes
    # ------------------------------------------------------------------

    def save_intervention(self, intervention: dict) -> None:
        self.conn.execute(
            """INSERT OR REPLACE INTO interventions
               (intervention_id, gap_id, student_id, concept, dominant_error,
                template_id, steps, practice_questions, worksheet_path,
                created_by, created_at, approved)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                intervention["intervention_id"],
                intervention.get("gap_id"),
                intervention["student_id"],
                intervention["concept"],
                intervention.get("dominant_error"),
                intervention.get("template_id"),
                json.dumps(intervention.get("steps", [])),
                json.dumps(intervention.get("practice_questions", [])),
                intervention.get("worksheet_path"),
                intervention.get("created_by", "teacher"),
                intervention.get("created_at", datetime.now().isoformat()),
                1 if intervention.get("approved") else 0,
            ),
        )
        self.conn.commit()

    def get_interventions(self, student_id: Optional[str] = None) -> List[dict]:
        query = "SELECT * FROM interventions"
        params = ()
        if student_id:
            query += " WHERE student_id = ?"
            params = (student_id,)
        query += " ORDER BY created_at DESC"
        rows = [dict(r) for r in self.conn.execute(query, params).fetchall()]
        for row in rows:
            row["steps"] = json.loads(row["steps"] or "[]")
            row["practice_questions"] = json.loads(row["practice_questions"] or "[]")
            row["approved"] = bool(row["approved"])
        return rows

    def save_outcome(self, outcome: dict) -> None:
        self.conn.execute(
            """INSERT INTO intervention_outcomes
               (intervention_id, reassessment_id, before_error_rate,
                after_error_rate, outcome, evaluated_at)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (
                outcome["intervention_id"],
                outcome.get("reassessment_id"),
                outcome.get("before_error_rate"),
                outcome.get("after_error_rate"),
                outcome["outcome"],
                outcome.get("evaluated_at", datetime.now().isoformat()),
            ),
        )
        self.conn.commit()

    def get_outcomes(self, intervention_id: Optional[str] = None) -> List[dict]:
        query = "SELECT * FROM intervention_outcomes"
        params = ()
        if intervention_id:
            query += " WHERE intervention_id = ?"
            params = (intervention_id,)
        query += " ORDER BY evaluated_at DESC"
        return [dict(r) for r in self.conn.execute(query, params).fetchall()]

    # ------------------------------------------------------------------

    def _count(self, table: str) -> int:
        return self.conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]


if __name__ == "__main__":
    from app.data.loader import load_all_synthetic
    from app.analytics.profiler import build_concept_profiles, detect_learning_gaps

    students, questions, cmap, responses = load_all_synthetic()
    repo = Repository("/tmp/opencode/test_shiksha.db")
    print("students saved:", repo.save_students(students))
    print("questions saved:", repo.save_questions(questions))
    print("responses appended:", repo.save_responses(responses))
    profiles = build_concept_profiles(responses, questions)
    gaps = detect_learning_gaps(profiles)
    print("profiles saved:", repo.save_profiles(profiles))
    print("gaps inserted:", repo.save_gaps(gaps))
    s2, q2, c2, r2 = repo.load_all_data()
    print("reload:", len(s2), len(q2), len(r2))
    print("active gaps in DB:", len(repo.get_gaps("active")))
    repo.close()

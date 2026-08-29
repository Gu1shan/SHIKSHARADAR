"""
SQLite schema for Shiksha Radar.

Tables:
    students, questions, responses          - raw data
    concept_profiles                        - persisted student x concept profiles
    learning_gaps                           - detected gaps with status lifecycle
    interventions                           - assigned interventions
    intervention_outcomes                   - reassessment results (closed/persisted)
"""

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS students (
    student_id  TEXT PRIMARY KEY,
    grade       INTEGER,
    section     TEXT
);

CREATE TABLE IF NOT EXISTS questions (
    question_id      TEXT PRIMARY KEY,
    text             TEXT,
    concept          TEXT NOT NULL,
    sub_concept      TEXT,
    difficulty       INTEGER,
    expected_answer  TEXT
);

CREATE TABLE IF NOT EXISTS responses (
    response_id    TEXT PRIMARY KEY,
    student_id     TEXT NOT NULL REFERENCES students(student_id),
    assessment_id  TEXT NOT NULL,
    question_id    TEXT NOT NULL REFERENCES questions(question_id),
    student_answer TEXT,
    is_correct     INTEGER NOT NULL,
    error_type     TEXT,
    created_at     TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_responses_student ON responses(student_id);
CREATE INDEX IF NOT EXISTS idx_responses_assessment ON responses(assessment_id);

CREATE TABLE IF NOT EXISTS concept_profiles (
    profile_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id   TEXT NOT NULL REFERENCES students(student_id),
    concept      TEXT NOT NULL,
    total_attempts      INTEGER,
    total_errors        INTEGER,
    error_breakdown     TEXT,   -- JSON dict
    assessments_with_errors INTEGER,
    first_error_date    TEXT,
    last_error_date     TEXT,
    trend        TEXT,
    confidence   REAL,
    error_rates         TEXT,   -- JSON list
    assessment_dates    TEXT,   -- JSON list
    updated_at   TEXT,
    UNIQUE(student_id, concept)
);

CREATE TABLE IF NOT EXISTS learning_gaps (
    gap_id       INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id   TEXT NOT NULL REFERENCES students(student_id),
    concept      TEXT NOT NULL,
    sub_concept  TEXT,
    dominant_error      TEXT,
    evidence_count      INTEGER,
    assessments_count   INTEGER,
    confidence   REAL,
    trend        TEXT,
    detected_at  TEXT,
    status       TEXT DEFAULT 'active',  -- active | intervening | resolved | persisted
    UNIQUE(student_id, concept, detected_at)
);

CREATE TABLE IF NOT EXISTS interventions (
    intervention_id TEXT PRIMARY KEY,
    gap_id      INTEGER REFERENCES learning_gaps(gap_id),
    student_id  TEXT NOT NULL,
    concept     TEXT NOT NULL,
    dominant_error TEXT,
    template_id TEXT,
    steps       TEXT,           -- JSON list
    practice_questions TEXT,    -- JSON list
    worksheet_path TEXT,
    created_by  TEXT DEFAULT 'teacher',
    created_at  TEXT,
    approved    INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS intervention_outcomes (
    outcome_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    intervention_id TEXT NOT NULL REFERENCES interventions(intervention_id),
    reassessment_id  TEXT,
    before_error_rate REAL,
    after_error_rate  REAL,
    outcome      TEXT,           -- gap_closed | improved | persisted | worse
    evaluated_at TEXT
);
"""


def init_db(conn) -> None:
    """Create all tables if they don't exist."""
    conn.executescript(SCHEMA_SQL)
    conn.commit()

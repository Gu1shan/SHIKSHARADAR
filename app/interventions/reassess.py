"""
Reassessment planning and outcome tracking.

Closed feedback loop: Detect -> Intervene -> Reassess -> Compare ->
"Gap Closed" or "Persisted".
"""
from datetime import datetime, timedelta

from app.interventions.templates import evaluate_outcome


def build_reassessment_plan(intervention: dict, questions_df=None) -> dict:
    """
    Build a reassessment plan for an intervention:
    - 5-8 questions on the same concept (easier mix)
    - scheduled REASSESSMENT_INTERVAL_DAYS after intervention
    """
    interval_days = 14
    due = datetime.now() + timedelta(days=interval_days)

    question_pool = []
    if questions_df is not None and not questions_df.empty:
        pool = questions_df[questions_df["concept"] == intervention["concept"]]
        easy = pool[pool["difficulty"] == 1]["question_id"].tolist()
        medium = pool[pool["difficulty"] == 2]["question_id"].tolist()
        question_pool = (easy[:4] + medium[:3])[:7]

    return {
        "intervention_id": intervention["intervention_id"],
        "student_id": intervention["student_id"],
        "concept": intervention["concept"],
        "reassessment_id": f"REA-{intervention['intervention_id']}",
        "suggested_date": due.date().isoformat(),
        "question_ids": question_pool,
        "num_questions": len(question_pool),
    }


def record_outcome(before_error_rate: float, after_error_rate: float,
                   intervention_id: str) -> dict:
    """Evaluate and format an outcome record for persistence."""
    outcome = evaluate_outcome(before_error_rate, after_error_rate)
    return {
        "intervention_id": intervention_id,
        "before_error_rate": round(before_error_rate, 4),
        "after_error_rate": round(after_error_rate, 4),
        "outcome": outcome,
        "evaluated_at": datetime.now().isoformat(),
    }


OUTCOME_LABELS = {
    "gap_closed": "✅ Gap closed",
    "improved": "📈 Improved — keep practicing",
    "persisted": "⏳ Persisted — extend intervention",
    "worse": "⚠️ Worsened — escalate to remedial support",
}


if __name__ == "__main__":
    iv = {"intervention_id": "INT-X", "student_id": "S1", "concept": "Fractions"}
    print(build_reassessment_plan(iv))
    print(record_outcome(0.6, 0.05, "INT-X"))

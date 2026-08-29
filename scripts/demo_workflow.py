"""
End-to-end workflow test: Load -> Detect -> Explain -> Intervene -> Reassess -> Close Loop.
Also serves as the 3-minute live demo script (run each step, narrate).
"""
import os
import tempfile

from app.data.loader import load_all_synthetic
from app.analytics.profiler import build_concept_profiles, detect_learning_gaps
from app.db.repository import Repository
from app.llm.explainer import explain_gap
from app.interventions.templates import get_intervention
from app.interventions.worksheet import generate_worksheet_pdf
from app.interventions.reassess import build_reassessment_plan, record_outcome, OUTCOME_LABELS


def main():
    print("=" * 60)
    print("SHIKSHA RADAR - END-TO-END WORKFLOW")
    print("=" * 60)

    # 1. LOAD: synthetic assessment data
    students, questions, cmap, responses = load_all_synthetic()
    print(f"\n[1] LOADED   {len(students)} students | {len(questions)} questions | "
          f"{len(responses)} responses")

    # 2. DETECT: profiles + learning gaps
    profiles = build_concept_profiles(responses, questions)
    gaps = detect_learning_gaps(profiles)
    print(f"[2] DETECTED {len(profiles)} concept profiles -> {len(gaps)} learning gaps")

    # 3. PERSIST: SQLite
    db_path = os.path.join(tempfile.gettempdir(), "demo_shiksha.db")
    if os.path.exists(db_path):
        os.remove(db_path)
    repo = Repository(db_path)
    repo.save_students(students)
    repo.save_questions(questions)
    appended = repo.save_responses(responses)
    repo.save_profiles(profiles)
    n_gaps = repo.save_gaps(gaps)
    print(f"[3] PERSISTED to SQLite ({db_path}): {appended} new responses, {n_gaps} gaps")

    # 4. EXPLAIN: LLM explanation for top gap
    gap = max(gaps, key=lambda g: g.confidence)
    profile = next(p for p in profiles
                   if p.student_id == gap.student_id and p.concept == gap.concept)
    exp = explain_gap(gap, profile)
    print(f"\n[4] EXPLAINED ({exp.provider}, valid={exp.valid}) for "
          f"{gap.student_id} / {gap.concept}:")
    print("    " + exp.text.replace("\n", "\n    ")[:400])

    # 5. INTERVENE: suggestion + PDF worksheet
    iv = get_intervention(gap)
    iv["approved"] = True
    pdf_path = generate_worksheet_pdf(iv, os.path.join(tempfile.gettempdir(), "worksheets"))
    plan = build_reassessment_plan(iv, questions)
    repo.save_intervention(iv)
    print(f"\n[5] INTERVENTION {iv['intervention_id']} approved by teacher")
    print(f"    Worksheet PDF: {pdf_path}")
    print(f"    Reassessment {plan['reassessment_id']} on {plan['suggested_date']} "
          f"({plan['num_questions']} questions)")

    # 6. REASSESS & CLOSE LOOP: simulate improved error rate
    before = profile.error_rate
    after = max(0.0, before - 0.45)  # simulated post-intervention reassessment
    outcome = record_outcome(before, after, iv["intervention_id"])
    repo.save_outcome(outcome)
    gap.status = "resolved" if outcome["outcome"] == "gap_closed" else "persisted"
    print(f"\n[6] OUTCOME   {before:.0%} -> {after:.0%} : {OUTCOME_LABELS[outcome['outcome']]}")

    repo.close()
    print("\n" + "=" * 60)
    print("WORKFLOW COMPLETE: Detect -> Explain -> Intervene -> Close Loop ✓")
    print("=" * 60)


if __name__ == "__main__":
    main()

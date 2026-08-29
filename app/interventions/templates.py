"""
Intervention templates: (concept, error type) -> remediation steps + practice.

Teacher override is mandatory: interventions are only *suggestions* until
a teacher approves them in the dashboard.
"""
from datetime import datetime
from uuid import uuid4


# Steps keyed by dominant error type; concept-specific overrides below.
ERROR_TYPE_STEPS = {
    "misconception": [
        "Reteach the core rule using concrete objects or drawings",
        "Ask the student to explain the rule back in their own words",
        "Work through 3 guided examples together",
    ],
    "wrong_approach": [
        "Show one problem solved two ways (correct vs incorrect strategy)",
        "Have the student sort 6 problems by which strategy fits",
        "Practice 4 problems with the correct strategy",
    ],
    "formula_selection": [
        "Review when to use each operation with a decision chart",
        "Practice identifying the operation before solving (5 problems)",
    ],
    "denominator_handling": [
        "Revise common denominators using fraction strips",
        "Practice 5 addition/subtraction problems with unlike denominators",
    ],
    "sign_error": [
        "Revise sign rules with a number line",
        "Drill 8 signed-number problems with immediate feedback",
    ],
    "simplification": [
        "Model 'is this in simplest form?' check as a final step",
        "Practice simplifying 6 answers already correctly computed",
    ],
    "carry_borrow": [
        "Use column method with regrouping boxes for 5 problems",
        "Check place-value understanding with a quick warm-up",
    ],
    "decimal_placement": [
        "Teach estimate-first: predict if answer will be bigger or smaller",
        "Practice 6 decimal operation problems with estimation checks",
    ],
    "unit_conversion": [
        "Create a personal conversion reference card",
        "Practice 5 conversions using real classroom objects",
    ],
    "arithmetic": [
        "Short daily fluency drill (5 min) on basic operations",
        "Re-attempt missed problems with a calculator check afterwards",
    ],
    "multiplication_fact": [
        "Daily 5-minute multiplication fact practice for one week",
        "Use arrays to build understanding behind the facts",
    ],
    "division_fact": [
        "Daily 5-minute division fact practice linked to multiplication facts",
    ],
    "incomplete": [
        "Teach a simple 'finish and check' checklist",
        "Allow structured extra time on the next assessment",
    ],
    "misread": [
        "Teach underlining key numbers before solving",
        "Practice re-reading questions aloud on 4 problems",
    ],
    "copy_error": [
        "Encourage neat column layout; check transcription after each step",
    ],
    "transcription": [
        "Have the student read their written work aloud to catch slips",
    ],
    "blank": [
        "Start next session with success-building warm-up questions",
        "Check whether skipping is due to pacing, confidence, or understanding",
    ],
}

CONCEPT_STEPS = {
    "Fractions": [
        "Use fraction strips/paper folding to rebuild the concept visually",
    ],
    "Algebra": [
        "Re-introduce the variable as 'mystery box' before formal notation",
    ],
    "Decimals": [
        "Connect decimals to money and place-value blocks",
    ],
}

CONCEPT_PRACTICE = {
    "Fractions": [
        "3/4 + 1/4 = ?",
        "2/3 + 1/6 = ?",
        "Which is larger: 3/5 or 4/7? Explain how you know.",
        "3/4 of 20 = ?",
    ],
    "Algebra": [
        "x + 7 = 15, find x",
        "3x = 21, find x",
        "If a = 4, what is 2a + 3?",
        "Simplify: 5n - 2n + n",
    ],
    "Decimals": [
        "0.4 + 0.25 = ?",
        "Round 3.68 to one decimal place",
        "Which is larger: 0.7 or 0.65?",
        "2.5 x 10 = ?",
    ],
    "Geometry": [
        "Angles in a triangle add up to ___ degrees",
        "A rectangle is 6 cm by 4 cm. What is its perimeter?",
        "Draw a line of symmetry on a square.",
    ],
    "Measurement": [
        "How many cm in 2.5 m?",
        "Convert 1500 g to kg",
        "A jug holds 1.5 L. How many 250 mL cups fill it?",
    ],
    "Percentages": [
        "What is 50% of 80?",
        "What is 25% of 200?",
        "Write 3/4 as a percentage",
    ],
    "Ratio & Proportion": [
        "Simplify the ratio 12:18",
        "If 2 pens cost Rs 10, what do 5 pens cost?",
    ],
}

DEFAULT_PRACTICE = [
    "Solve: ____ (teacher to insert question)",
    "Solve: ____ (teacher to insert question)",
    "Explain your method for one problem above.",
]

REASSESSMENT_INTERVAL_DAYS = 14


def get_intervention(gap) -> dict:
    """Build an intervention suggestion for a learning gap (not yet approved)."""
    steps = list(CONCEPT_STEPS.get(gap.concept, []))
    steps += ERROR_TYPE_STEPS.get(
        gap.dominant_error,
        ["Assign targeted practice on this concept", "Reassess after two weeks"],
    )
    # de-duplicate while preserving order
    seen = set()
    steps = [s for s in steps if not (s in seen or seen.add(s))]

    practice = CONCEPT_PRACTICE.get(gap.concept, DEFAULT_PRACTICE)

    return {
        "intervention_id": f"INT-{uuid4().hex[:8].upper()}",
        "student_id": gap.student_id,
        "concept": gap.concept,
        "dominant_error": gap.dominant_error,
        "template_id": f"{gap.concept}:{gap.dominant_error}",
        "steps": steps,
        "practice_questions": practice,
        "reassessment_due": (
            datetime.now().toordinal() + REASSESSMENT_INTERVAL_DAYS
        ),
        "created_at": datetime.now().isoformat(),
        "approved": False,
    }


def evaluate_outcome(before_error_rate: float, after_error_rate: float) -> str:
    """
    Compare pre/post intervention error rates.

    Returns: gap_closed | improved | persisted | worse
    """
    delta = before_error_rate - after_error_rate
    if after_error_rate <= 0.10:
        return "gap_closed"
    if delta >= 0.15:
        return "improved"
    if delta <= -0.05:
        return "worse"
    return "persisted"


if __name__ == "__main__":
    class FakeGap:
        student_id = "Student_001"
        concept = "Fractions"
        dominant_error = "denominator_handling"

    iv = get_intervention(FakeGap())
    print(iv["intervention_id"], "|", iv["concept"])
    for s in iv["steps"]:
        print(" -", s)
    print("practice:", iv["practice_questions"])
    print("outcome checks:", evaluate_outcome(0.6, 0.05), evaluate_outcome(0.6, 0.5), evaluate_outcome(0.3, 0.5))

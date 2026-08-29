"""
Output validator for LLM-generated explanations.

Enforces responsible-AI rules:
- forbidden negative labels
- required evidence citations (error count, assessment count, confidence)
- length cap
"""


FORBIDDEN_LABELS = [
    "weak", "poor", "failing", "failure", "slow learner", "slow",
    "bad at", "hopeless", "stupid", "dumb", "lazy", "lost cause",
    "below average intelligence", "retarded",
]

REQUIRED_EVIDENCE_HINTS = ["confidence"]


def validate_explanation(text: str, gap) -> dict:
    """
    Validate an explanation against responsible-AI rules.

    Returns {"valid": bool, "warnings": [str], "sanitized": str}
    """
    warnings = []
    lowered = text.lower()

    # 1. Forbidden labels (word-boundary aware for short words)
    import re

    found_forbidden = []
    for label in FORBIDDEN_LABELS:
        pattern = r"\b" + re.escape(label) + r"\b"
        if re.search(pattern, lowered):
            found_forbidden.append(label)
    if found_forbidden:
        warnings.append(f"Forbidden labels used: {found_forbidden}")

    # 2. Evidence citations: error count and confidence should appear
    if gap.evidence_count and str(gap.evidence_count) not in text:
        warnings.append("Evidence citation missing: error count")
    if not any(h in lowered for h in REQUIRED_EVIDENCE_HINTS):
        warnings.append("Evidence citation missing: confidence")

    # 3. Length
    word_count = len(text.split())
    if word_count > 220:
        warnings.append(f"Explanation too long ({word_count} words)")

    sanitized = sanitize(text)
    return {
        "valid": len(warnings) == 0,
        "warnings": warnings,
        "sanitized": sanitized,
    }


def sanitize(text: str) -> str:
    """Replace forbidden labels with supportive language."""
    replacements = {
        "weak": "still developing",
        "poor": "emerging",
        "failing": "needing support",
        "failure": "needs additional support",
        "slow learner": "student who may benefit from additional support",
        "hopeless": "in need of targeted support",
        "stupid": "",
        "dumb": "",
        "lazy": "disengaged",
    }
    import re

    result = text
    for bad, good in replacements.items():
        pattern = re.compile(r"\b" + re.escape(bad) + r"\b", re.IGNORECASE)
        result = pattern.sub(good, result)
    return result


if __name__ == "__main__":
    class FakeGap:
        student_id = "Student_001"
        concept = "Fractions"
        evidence_count = 7
        assessments_count = 3

    sample = "This weak student is failing fractions with 7 errors; confidence is 82%."
    print(validate_explanation(sample, FakeGap()))

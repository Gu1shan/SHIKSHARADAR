"""
Prompt templates for the LLM explanation layer.

Design principles:
- Evidence JSON is always included; LLM must cite it.
- Responsible-AI guardrails are baked into the system prompt.
- Deterministic fallback exists if no API key is configured.
"""

SYSTEM_PROMPT = """You are an educational assistant helping a Class 5 math teacher \
understand why a student may be struggling with a specific concept.

STRICT RULES:
1. NEVER use negative labels such as "weak", "poor", "failing", "slow", "bad", or "hopeless".
2. Use supportive language: "possible learning gap", "repeated error pattern", \
"may benefit from additional support".
3. You MUST cite evidence: error count, assessment count, and confidence percentage.
4. Do NOT invent data that is not in the evidence JSON.
5. Keep the explanation under 150 words.
6. End with one concrete, actionable suggestion for the teacher.

FORMAT:
**What we observed:** <pattern summary with cited evidence>
**Likely cause:** <hypothesis based on dominant error type>
**Suggested next step:** <one concrete action>
"""


def build_evidence_json(gap) -> dict:
    """Build the compact evidence payload from a LearningGap."""
    return {
        "student_id": gap.student_id,
        "concept": gap.concept,
        "sub_concept": gap.sub_concept,
        "dominant_error_type": gap.dominant_error,
        "total_errors": gap.evidence_count,
        "assessments_with_errors": gap.assessments_count,
        "confidence": round(gap.confidence * 100, 1),
        "trend": gap.trend,
        "first_detected": (gap.detected_at or "")[:10],
    }


def build_user_prompt(gap, profile=None) -> str:
    """Build the user prompt containing evidence JSON."""
    import json

    evidence = build_evidence_json(gap)
    if profile is not None:
        evidence["error_breakdown"] = profile.error_breakdown
        evidence["error_rate_overall"] = (
            round(profile.error_rate * 100, 1) if profile.total_attempts else 0.0
        )

    error_hint = ERROR_HINTS.get(gap.dominant_error, "")
    return (
        "Explain this student's learning pattern to their teacher.\n\n"
        f"EVIDENCE JSON:\n{json.dumps(evidence, indent=2)}\n\n"
        f"Error-type context (for your reasoning only): {gap.dominant_error} — "
        f"{error_hint}\n"
    )


ERROR_HINTS = {
    "misconception": "student holds an incorrect mental model of the rule",
    "wrong_approach": "student applies a strategy that does not fit the problem",
    "formula_selection": "student picks the wrong formula or operation",
    "denominator_handling": "student treats denominators incorrectly in fraction operations",
    "sign_error": "student drops or flips positive/negative signs",
    "simplification": "student does not reduce answers to simplest form",
    "carry_borrow": "student makes regrouping mistakes in addition/subtraction",
    "decimal_placement": "student misplaces the decimal point",
    "unit_conversion": "student converts between units incorrectly",
    "arithmetic": "small calculation slips in basic operations",
    "multiplication_fact": "recall of multiplication tables is inconsistent",
    "division_fact": "recall of division facts is inconsistent",
    "incomplete": "student leaves answers unfinished",
    "misread": "student appears to misread the question",
    "copy_error": "student copies numbers incorrectly between steps",
    "transcription": "student writes a different value than intended",
    "ambiguous": "answer could not be confidently classified",
    "blank": "question left unanswered",
}


FALLBACK_TEMPLATE = """**What we observed:** Across {assessments} assessments, {student} made \
{errors} errors on **{concept}**, most frequently of the type "{dominant}". Detection confidence \
is {confidence:.0f}% and the trend is **{trend}**.

**Likely cause:** {cause}

**Suggested next step:** {next_step}
"""

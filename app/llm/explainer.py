"""
LLM explanation layer for Shiksha Radar.

Providers: Groq (Llama 3.1) or Gemini, selected via env vars:
    GROQ_API_KEY / GROQ_MODEL   (default: llama-3.1-8b-instant)
    GEMINI_API_KEY / GEMINI_MODEL (default: gemini-1.5-flash)

If no API key is configured, a deterministic template explanation is
returned so the product works fully offline.
"""
import os

import requests

from app.llm.prompts import SYSTEM_PROMPT, build_user_prompt, build_evidence_json, FALLBACK_TEMPLATE, ERROR_HINTS
from app.llm.validator import validate_explanation


class Explanation:
    def __init__(self, text: str, provider: str, valid: bool, warnings: list):
        self.text = text
        self.provider = provider
        self.valid = valid
        self.warnings = warnings


def explain_gap(gap, profile=None, timeout: int = 30) -> Explanation:
    """Explain a learning gap. Tries LLM providers, falls back to template."""
    raw_text, provider = _generate_raw(gap, profile, timeout)
    result = validate_explanation(raw_text, gap)
    return Explanation(
        text=result["sanitized"],
        provider=provider,
        valid=result["valid"],
        warnings=result["warnings"],
    )


def _generate_raw(gap, profile, timeout):
    groq_key = os.environ.get("GROQ_API_KEY")
    gemini_key = os.environ.get("GEMINI_API_KEY")

    if groq_key:
        try:
            return _explain_groq(gap, profile, groq_key, timeout), "groq"
        except Exception:
            pass
    if gemini_key:
        try:
            return _explain_gemini(gap, profile, gemini_key, timeout), "gemini"
        except Exception:
            pass
    return _fallback_text(gap, profile), "template-fallback"


def _explain_groq(gap, profile, api_key: str, timeout: int) -> str:
    model = os.environ.get("GROQ_MODEL", "llama-3.1-8b-instant")
    resp = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={"Authorization": f"Bearer {api_key}"},
        json={
            "model": model,
            "temperature": 0.3,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": build_user_prompt(gap, profile)},
            ],
        },
        timeout=timeout,
    )
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"]


def _explain_gemini(gap, profile, api_key: str, timeout: int) -> str:
    model = os.environ.get("GEMINI_MODEL", "gemini-1.5-flash")
    resp = requests.post(
        f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent",
        params={"key": api_key},
        json={
            "system_instruction": {"parts": [{"text": SYSTEM_PROMPT}]},
            "contents": [
                {"role": "user", "parts": [{"text": build_user_prompt(gap, profile)}]}
            ],
            "generationConfig": {"temperature": 0.3},
        },
        timeout=timeout,
    )
    resp.raise_for_status()
    return resp.json()["candidates"][0]["content"]["parts"][0]["text"]


_CAUSE_BY_CATEGORY = {
    "misconception": "an incorrect mental model of the rule that needs to be explicitly rebuilt",
    "wrong_approach": "a strategy being applied that does not fit this problem type",
    "formula_selection": "difficulty selecting the right operation or formula",
    "denominator_handling": "the denominator rule in fraction operations is not yet secure",
    "sign_error": "sign handling during multi-step work is inconsistent",
    "simplification": "answers are computed but not reduced to simplest form",
    "carry_borrow": "regrouping in multi-digit arithmetic breaks down",
    "decimal_placement": "decimal point placement rules are not yet automatic",
    "unit_conversion": "conversion factors between units are being mixed up",
    "arithmetic": "small calculation slips rather than conceptual confusion",
    "multiplication_fact": "multiplication fact recall is not yet fluent",
    "division_fact": "division fact recall is not yet fluent",
    "incomplete": "work is often left unfinished — pacing or confidence may be factors",
    "misread": "questions appear to be misread — checking strategies may help",
    "copy_error": "values are copied incorrectly between steps",
    "transcription": "written answers differ from the intended value",
    "ambiguous": "the pattern could not be confidently classified",
    "blank": "questions are being skipped — confidence or pacing may be factors",
}

_NEXT_STEP_BY_CATEGORY = {
    "misconception": "run a short diagnostic 1-on-1 and reteach the rule with concrete examples",
    "wrong_approach": "model worked examples comparing correct vs incorrect strategies",
    "formula_selection": "practice sorting problems by which operation they need before solving",
    "denominator_handling": "assign targeted fraction-worksheet practice on common denominators",
    "sign_error": "drill signed-number rules with immediate feedback",
    "simplification": "add a 'check your answer is in simplest form' step to routines",
    "carry_borrow": "use column-method practice with regrouping boxes",
    "decimal_placement": "estimate-first strategy: predict magnitude before computing",
    "unit_conversion": "create a conversion reference card and practice with real objects",
    "arithmetic": "short daily fluency drills on basic operations",
    "multiplication_fact": "daily 5-minute multiplication fact practice",
    "division_fact": "daily 5-minute division fact practice linked to multiplication",
    "incomplete": "allow extra time and teach a 'finish what you start' checklist",
    "misread": "teach underlining key numbers and re-reading the question",
    "copy_error": "encourage neat layout and step-by-step transcription checks",
    "transcription": "review written work aloud with the student",
    "blank": "check in about confidence; start with success-building questions",
}


def _fallback_text(gap, profile) -> str:
    cause = _CAUSE_BY_CATEGORY.get(
        gap.dominant_error, ERROR_HINTS.get(gap.dominant_error, "repeated errors of one type")
    )
    next_step = _NEXT_STEP_BY_CATEGORY.get(
        gap.dominant_error, "assign targeted practice on this concept and reassess in 2 weeks"
    )
    return FALLBACK_TEMPLATE.format(
        assessments=gap.assessments_count,
        student=gap.student_id,
        errors=gap.evidence_count,
        concept=gap.concept,
        dominant=gap.dominant_error,
        confidence=gap.confidence * 100,
        trend=gap.trend,
        cause=cause,
        next_step=next_step,
    )


if __name__ == "__main__":
    from app.data.loader import load_all_synthetic
    from app.analytics.profiler import build_concept_profiles, detect_learning_gaps

    students, questions, cmap, responses = load_all_synthetic()
    profiles = build_concept_profiles(responses, questions)
    gaps = detect_learning_gaps(profiles)
    gap = gaps[0]
    profile = next(p for p in profiles if p.student_id == gap.student_id and p.concept == gap.concept)
    exp = explain_gap(gap, profile)
    print(f"provider={exp.provider} valid={exp.valid} warnings={exp.warnings}\n")
    print(exp.text)

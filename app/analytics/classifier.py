"""
Rule-based error classification for Shiksha Radar.
Classifies incorrect answers into error types based on patterns.
"""
import re
from typing import Dict, List, Optional
from app.data.normalizer import normalize_answer


ERROR_TAXONOMY = {
    "conceptual": {
        "keywords": ["misconcept", "wrong_approach", "formula_selection", "misunderstand"],
        "patterns": [
            r"formula_selection",
            r"wrong.*approach",
            r"misconcept",
        ],
        "description": "Fundamental misunderstanding of concept"
    },
    "procedural": {
        "keywords": ["denominator_handling", "sign_error", "simplification", 
                     "carry_borrow", "decimal_placement", "unit_conversion"],
        "patterns": [
            r"denominator",
            r"sign.*error",
            r"simplif",
            r"carry|borrow",
            r"decimal.*place",
            r"unit.*convert",
        ],
        "description": "Correct concept but wrong procedure"
    },
    "calculation": {
        "keywords": ["arithmetic", "multiplication_fact", "division_fact"],
        "patterns": [
            r"arithmetic",
            r"multiplication.*fact",
            r"division.*fact",
            r"calculation",
        ],
        "description": "Basic arithmetic error"
    },
    "careless": {
        "keywords": ["incomplete", "misread", "copy_error", "transcription", "careless"],
        "patterns": [
            r"incomplete",
            r"misread",
            r"copy.*error",
            r"transcription",
            r"careless",
            r"typo",
        ],
        "description": "Careless mistake, not conceptual"
    },
    "unknown": {
        "keywords": ["ambiguous", "blank"],
        "patterns": [
            r"ambiguous",
            r"blank",
            r"unknown",
        ],
        "description": "Cannot classify"
    }
}

ERROR_TYPE_TO_CATEGORY = {}
for category, info in ERROR_TAXONOMY.items():
    for keyword in info["keywords"]:
        ERROR_TYPE_TO_CATEGORY[keyword] = category


def classify_error_type(student_answer: str, expected_answer: str, 
                        question_text: str = "", concept: str = "",
                        sub_concept: str = "") -> str:
    """
    Classify error type based on student answer, expected answer, and question context.
    
    For synthetic data, the error_type is already encoded in student_answer.
    For real data, this would use pattern matching on the actual answer content.
    """
    student_norm = normalize_answer(student_answer)
    expected_norm = normalize_answer(expected_answer)
    
    if student_norm.startswith("incorrect_"):
        error_type = student_norm.replace("incorrect_", "")
        return error_type
    
    if not student_norm or student_norm in ["", "blank", "null", "none", "nan"]:
        return "incomplete"
    
    error_lower = student_norm.lower()
    
    for error_type, category in ERROR_TYPE_TO_CATEGORY.items():
        if error_type in error_lower:
            return error_type
    
    for category, info in ERROR_TAXONOMY.items():
        for pattern in info["patterns"]:
            if re.search(pattern, error_lower, re.IGNORECASE):
                for keyword in info["keywords"]:
                    if keyword in error_lower:
                        return keyword
                return list(ERROR_TAXONOMY.keys())[0]
    
    if concept == "Fractions" and sub_concept in ["denominator_handling", "addition", "subtraction"]:
        return "denominator_handling"
    elif concept == "Fractions" and sub_concept == "simplification":
        return "simplification"
    elif concept == "Algebra" and sub_concept in ["equations", "sign_rules"]:
        return "sign_error"
    elif concept == "Geometry" and sub_concept == "area_perimeter":
        return "area_perimeter_confusion"
    elif concept in ["Measurement", "Decimals"]:
        return "unit_conversion"
    
    return "arithmetic"


def classify_batch(responses_df, questions_df) -> List[str]:
    """
    Classify error types for a batch of responses.
    
    Args:
        responses_df: DataFrame with response_id, student_answer, question_id, is_correct
        questions_df: DataFrame with question_id, text, concept, sub_concept, expected_answer
    
    Returns:
        List of error_type strings
    """
    question_lookup = questions_df.set_index("question_id").to_dict("index")
    
    error_types = []
    for _, row in responses_df.iterrows():
        if row["is_correct"]:
            error_types.append("")
            continue
        
        q_info = question_lookup.get(row["question_id"], {})
        error_type = classify_error_type(
            student_answer=row["student_answer"],
            expected_answer=q_info.get("expected_answer", ""),
            question_text=q_info.get("text", ""),
            concept=q_info.get("concept", ""),
            sub_concept=q_info.get("sub_concept", "")
        )
        error_types.append(error_type)
    
    return error_types


def get_error_category(error_type: str) -> str:
    """Get category for an error type."""
    return ERROR_TYPE_TO_CATEGORY.get(error_type, "unknown")


def get_all_error_types() -> List[str]:
    """Get all known error types."""
    types = set()
    for info in ERROR_TAXONOMY.values():
        types.update(info["keywords"])
    return sorted(types)


if __name__ == "__main__":
    test_cases = [
        ("incorrect_denominator_handling", "1/2", "Add 1/2 + 1/3", "Fractions", "denominator_handling"),
        ("incorrect_sign_error", "x+5=10", "Solve for x: x+5=10", "Algebra", "equations"),
        ("incorrect_simplification", "2/4", "Simplify 2/4", "Fractions", "simplification"),
        ("incorrect_arithmetic", "7", "5+3", "Arithmetic", ""),
        ("", "1/2", "Add 1/2 + 1/3", "Fractions", "denominator_handling"),
        ("incorrect_unknown", "idk", "What is 2+2?", "Arithmetic", ""),
    ]
    
    for student_ans, expected, question, concept, sub_concept in test_cases:
        result = classify_error_type(student_ans, expected, question, concept, sub_concept)
        print(f"'{student_ans}' -> {result} (category: {get_error_category(result)})")
    
    print(f"\nAll error types: {get_all_error_types()}")
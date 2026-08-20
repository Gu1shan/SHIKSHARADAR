"""
Answer normalization for Shiksha Radar.
Handles case, whitespace, unicode normalization for answer comparison.
"""
import unicodedata
import re
from typing import Union


def normalize_answer(answer: Union[str, float, int, None]) -> str:
    """
    Normalize an answer for comparison.
    
    Steps:
    1. Convert to string
    2. Strip whitespace
    3. Lowercase
    4. Unicode normalize (NFKC)
    5. Collapse multiple spaces
    6. Remove trailing/leading punctuation (optional)
    """
    if answer is None or (isinstance(answer, float) and pd_isna(answer)):
        return ""
    
    s = str(answer)
    s = s.strip()
    s = s.lower()
    s = unicodedata.normalize("NFKC", s)
    s = re.sub(r"\s+", " ", s)
    s = s.strip(" .,;:")
    
    return s


def pd_isna(val) -> bool:
    """Check if value is NA without importing pandas."""
    try:
        import pandas as pd
        return pd.isna(val)
    except ImportError:
        return val is None or (isinstance(val, float) and val != val)


def normalize_series(series) -> list:
    """Normalize a pandas Series of answers."""
    return [normalize_answer(x) for x in series]


def answers_match(student_answer: Union[str, float, int, None], 
                  expected_answer: Union[str, float, int, None],
                  tolerance: float = 0.01) -> bool:
    """
    Compare student answer to expected answer.
    
    For numeric answers, allows tolerance.
    For text answers, uses normalized string comparison.
    """
    student_norm = normalize_answer(student_answer)
    expected_norm = normalize_answer(expected_answer)
    
    if not student_norm and not expected_norm:
        return True
    if not student_norm or not expected_norm:
        return False
    
    try:
        student_num = float(student_norm)
        expected_num = float(expected_norm)
        return abs(student_num - expected_num) <= tolerance
    except ValueError:
        return student_norm == expected_norm


if __name__ == "__main__":
    test_cases = [
        ("  1/2  ", "1/2", True),
        ("1/2", " 1 / 2 ", False),
        ("0.5", "0.50", True),
        ("0.5", "0.51", False),
        ("  Hello World  ", "hello world", True),
        ("HELLO", "hello", True),
        ("", "", True),
        ("None", "", False),
        (None, "", True),
    ]
    
    for student, expected, should_match in test_cases:
        result = answers_match(student, expected)
        status = "✓" if result == should_match else "✗"
        print(f"{status} '{student}' vs '{expected}' -> {result} (expected {should_match})")
"""
Data loading and schema validation for Shiksha Radar.
"""
import pandas as pd
import json
from pathlib import Path
from typing import Dict, Tuple, Optional
from .validator import validate_schema


SCHEMA_DIR = Path(__file__).parent.parent.parent / "data" / "schemas"
SYNTHETIC_DIR = Path(__file__).parent.parent.parent / "data" / "synthetic"


def load_schema(schema_name: str) -> Dict:
    """Load a JSON schema file."""
    schema_path = SCHEMA_DIR / schema_name
    with open(schema_path) as f:
        return json.load(f)


def load_students(path: Optional[str] = None) -> pd.DataFrame:
    """Load and validate students.csv."""
    if path is None:
        path = SYNTHETIC_DIR / "students.csv"
    df = pd.read_csv(path)
    validate_schema(df, "students", "assessment_schema.json")
    return df


def load_questions(path: Optional[str] = None) -> pd.DataFrame:
    """Load and validate questions.csv."""
    if path is None:
        path = SYNTHETIC_DIR / "questions.csv"
    df = pd.read_csv(path)
    validate_schema(df, "questions", "question_schema.json")
    return df


def load_concept_map(path: Optional[str] = None) -> pd.DataFrame:
    """Load and validate concept_map.csv."""
    if path is None:
        path = SYNTHETIC_DIR / "concept_map.csv"
    df = pd.read_csv(path)
    validate_schema(df, "concept_map", "question_schema.json")
    return df


def load_responses(path: Optional[str] = None) -> pd.DataFrame:
    """Load and validate responses.csv."""
    if path is None:
        path = SYNTHETIC_DIR / "responses.csv"
    df = pd.read_csv(path)
    # Fill NaN in error_type with empty string (correct answers have no error type)
    if 'error_type' in df.columns:
        df['error_type'] = df['error_type'].fillna('')
    validate_schema(df, "responses", "assessment_schema.json")
    return df


def load_all_synthetic() -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Load all synthetic data files."""
    students = load_students()
    questions = load_questions()
    concept_map = load_concept_map()
    responses = load_responses()
    return students, questions, concept_map, responses


def print_data_summary(students: pd.DataFrame, questions: pd.DataFrame, 
                       concept_map: pd.DataFrame, responses: pd.DataFrame) -> None:
    """Print summary statistics for loaded data."""
    print("=== Data Summary ===")
    print(f"Students: {len(students)} rows, {students['student_id'].nunique()} unique")
    print(f"  Grades: {students['grade'].unique()}")
    print(f"  Sections: {students['section'].unique()}")
    print()
    print(f"Questions: {len(questions)} rows")
    print(f"  Concepts: {questions['concept'].nunique()} ({', '.join(sorted(questions['concept'].unique()))})")
    print(f"  Difficulties: {sorted(questions['difficulty'].unique())}")
    print()
    print(f"Concept Map: {len(concept_map)} rows")
    print()
    print(f"Responses: {len(responses)} rows")
    print(f"  Assessments: {responses['assessment_id'].nunique()} ({', '.join(sorted(responses['assessment_id'].unique()))})")
    print(f"  Students with responses: {responses['student_id'].nunique()}")
    print(f"  Overall accuracy: {responses['is_correct'].mean():.1%}")
    print(f"  Error types: {responses[~responses['is_correct']]['error_type'].nunique()} unique")
    print()


if __name__ == "__main__":
    students, questions, concept_map, responses = load_all_synthetic()
    print_data_summary(students, questions, concept_map, responses)
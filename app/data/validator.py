"""
Schema validation for CSV data using JSON schemas.
"""
import pandas as pd
import json
from pathlib import Path
from typing import Dict, List, Optional


SCHEMA_DIR = Path(__file__).parent.parent.parent / "data" / "schemas"


EXPECTED_TYPES = {
    "string": "object",
    "integer": "int64",
    "boolean": "bool",
}


def load_schema(schema_name: str) -> Dict:
    """Load a JSON schema file."""
    schema_path = SCHEMA_DIR / schema_name
    with open(schema_path) as f:
        return json.load(f)


def get_expected_columns(table_name: str, schema_name: str) -> Dict[str, str]:
    """Get expected columns and types from schema."""
    schema = load_schema(schema_name)
    if table_name not in schema:
        raise ValueError(f"Table '{table_name}' not found in schema '{schema_name}'")
    return schema[table_name]["columns"]


def validate_columns(df: pd.DataFrame, expected: Dict[str, str], table_name: str) -> List[str]:
    """Validate DataFrame columns match expected schema."""
    errors = []
    
    df_cols = set(df.columns)
    exp_cols = set(expected.keys())
    
    missing = exp_cols - df_cols
    if missing:
        errors.append(f"{table_name}: Missing columns: {sorted(missing)}")
    
    extra = df_cols - exp_cols
    if extra:
        errors.append(f"{table_name}: Extra columns: {sorted(extra)}")
    
    for col, exp_type in expected.items():
        if col in df.columns:
            actual_type = str(df[col].dtype)
            if exp_type == "integer" and not pd.api.types.is_integer_dtype(df[col]):
                errors.append(f"{table_name}.{col}: Expected integer, got {actual_type}")
            elif exp_type == "boolean" and not pd.api.types.is_bool_dtype(df[col]):
                errors.append(f"{table_name}.{col}: Expected boolean, got {actual_type}")
            elif exp_type == "string" and not pd.api.types.is_string_dtype(df[col]):
                errors.append(f"{table_name}.{col}: Expected string, got {actual_type}")
    
    return errors


def validate_nulls(df: pd.DataFrame, table_name: str) -> List[str]:
    """Check for null values in required columns."""
    errors = []
    null_counts = df.isnull().sum()
    for col, count in null_counts.items():
        if count > 0:
            errors.append(f"{table_name}.{col}: {count} null values")
    return errors


def validate_uniqueness(df: pd.DataFrame, table_name: str, key_columns: List[str]) -> List[str]:
    """Check for duplicate key values."""
    errors = []
    for key in key_columns:
        if key in df.columns:
            dup_count = df[key].duplicated().sum()
            if dup_count > 0:
                errors.append(f"{table_name}.{key}: {dup_count} duplicate values")
    return errors


def validate_schema(df: pd.DataFrame, table_name: str, schema_name: str, 
                    key_columns: Optional[List[str]] = None) -> None:
    """
    Validate DataFrame against JSON schema.
    
    Args:
        df: DataFrame to validate
        table_name: Name of the table in schema (e.g., 'students', 'questions')
        schema_name: Schema file name (e.g., 'assessment_schema.json')
        key_columns: Columns that should be unique (for duplicate checking)
    
    Raises:
        ValueError: If validation fails with detailed error messages
    """
    expected = get_expected_columns(table_name, schema_name)
    
    all_errors = []
    all_errors.extend(validate_columns(df, expected, table_name))
    all_errors.extend(validate_nulls(df, table_name))
    
    if key_columns:
        all_errors.extend(validate_uniqueness(df, table_name, key_columns))
    
    if all_errors:
        raise ValueError(f"Schema validation failed for {table_name}:\n" + "\n".join(all_errors))


def validate_students(df: pd.DataFrame) -> None:
    """Validate students DataFrame."""
    validate_schema(df, "students", "assessment_schema.json", key_columns=["student_id"])


def validate_questions(df: pd.DataFrame) -> None:
    """Validate questions DataFrame."""
    validate_schema(df, "questions", "question_schema.json", key_columns=["question_id"])


def validate_concept_map(df: pd.DataFrame) -> None:
    """Validate concept_map DataFrame."""
    validate_schema(df, "concept_map", "question_schema.json", key_columns=["question_id"])


def validate_responses(df: pd.DataFrame) -> None:
    """Validate responses DataFrame."""
    validate_schema(df, "responses", "assessment_schema.json", key_columns=["response_id"])


if __name__ == "__main__":
    import sys
    sys.path.insert(0, str(Path(__file__).parent.parent.parent))
    from app.data.loader import load_all_synthetic
    
    students, questions, concept_map, responses = load_all_synthetic()
    print("All validations passed!")
"""
Analytics package for Shiksha Radar.
"""
from .classifier import (
    classify_error_type,
    classify_batch,
    get_error_category,
    get_all_error_types,
    ERROR_TAXONOMY,
    ERROR_TYPE_TO_CATEGORY,
)
from .concept_mapper import ConceptMapper, load_concept_mapper
from .confidence import (
    wilson_score_interval,
    wilson_lower_bound,
    calculate_confidence,
    calculate_recency_weight,
    calculate_trend,
    detect_learning_gap,
)
from .profiler import (
    ConceptProfile,
    LearningGap,
    build_concept_profiles,
    detect_learning_gaps,
    get_student_gaps,
    get_class_gaps,
    get_concept_difficulty,
)

__all__ = [
    "classify_error_type",
    "classify_batch",
    "get_error_category",
    "get_all_error_types",
    "ERROR_TAXONOMY",
    "ERROR_TYPE_TO_CATEGORY",
    "ConceptMapper",
    "load_concept_mapper",
    "wilson_score_interval",
    "wilson_lower_bound",
    "calculate_confidence",
    "calculate_recency_weight",
    "calculate_trend",
    "detect_learning_gap",
    "ConceptProfile",
    "LearningGap",
    "build_concept_profiles",
    "detect_learning_gaps",
    "get_student_gaps",
    "get_class_gaps",
    "get_concept_difficulty",
]
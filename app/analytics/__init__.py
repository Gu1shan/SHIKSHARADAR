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

__all__ = [
    "classify_error_type",
    "classify_batch",
    "get_error_category",
    "get_all_error_types",
    "ERROR_TAXONOMY",
    "ERROR_TYPE_TO_CATEGORY",
]
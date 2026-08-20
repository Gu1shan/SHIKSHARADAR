"""
Concept profiling and learning gap detection for Shiksha Radar.
Builds student×concept profiles and detects learning gaps with evidence.
"""
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional
from datetime import datetime
import pandas as pd
import numpy as np
from app.analytics.confidence import (
    calculate_confidence, calculate_recency_weight, calculate_trend,
    detect_learning_gap, wilson_lower_bound
)
from app.data.normalizer import normalize_answer


@dataclass
class ConceptProfile:
    """Profile of a student's performance on a specific concept."""
    student_id: str
    concept: str
    sub_concept: Optional[str]
    total_attempts: int
    total_errors: int
    error_breakdown: Dict[str, int]
    assessments_with_errors: int
    first_error_date: Optional[str]
    last_error_date: Optional[str]
    trend: str
    confidence: float
    error_rates: List[float]
    assessment_dates: List[str]
    
    def to_dict(self) -> dict:
        return asdict(self)
    
    @property
    def error_rate(self) -> float:
        return self.total_errors / self.total_attempts if self.total_attempts > 0 else 0.0
    
    @property
    def has_gap(self) -> bool:
        return self.confidence >= 0.30 and self.total_errors >= 3 and self.assessments_with_errors >= 2


@dataclass
class LearningGap:
    """Detected learning gap with evidence."""
    student_id: str
    concept: str
    sub_concept: Optional[str]
    dominant_error: str
    evidence_count: int
    assessments_count: int
    confidence: float
    trend: str
    detected_at: str
    status: str = "active"  # active, intervening, resolved, persisted
    
    def to_dict(self) -> dict:
        return asdict(self)


def build_concept_profiles(responses_df: pd.DataFrame, 
                           questions_df: pd.DataFrame) -> List[ConceptProfile]:
    """
    Build concept profiles for all students from response data.
    
    Args:
        responses_df: DataFrame with response records
        questions_df: DataFrame with question metadata (concept, sub_concept)
    
    Returns:
        List of ConceptProfile objects
    """
    # Merge responses with question metadata
    merged = responses_df.merge(
        questions_df[["question_id", "concept", "sub_concept"]], 
        on="question_id", how="left"
    )
    
    # Parse dates
    merged["created_at"] = pd.to_datetime(merged["created_at"])
    
    profiles = []
    
    # Group by student and concept (aggregate sub-concepts for gap detection)
    for (student_id, concept), group in merged.groupby(["student_id", "concept"]):
        group = group.sort_values("created_at")
        
        total_attempts = len(group)
        total_errors = (~group["is_correct"]).sum()
        
        # Error breakdown
        error_breakdown = {}
        if total_errors > 0:
            error_types = group[~group["is_correct"]]["error_type"]
            error_breakdown = error_types.value_counts().to_dict()
        
        # Per-assessment error rates
        assessment_groups = group.groupby("assessment_id")
        error_rates = []
        assessment_dates = []
        assessments_with_errors = 0
        
        for assess_id, assess_group in assessment_groups:
            assess_errors = (~assess_group["is_correct"]).sum()
            assess_total = len(assess_group)
            error_rates.append(assess_errors / assess_total if assess_total > 0 else 0.0)
            assessment_dates.append(assess_group["created_at"].iloc[0])
            if assess_errors > 0:
                assessments_with_errors += 1
        
        # Dates
        error_dates = group[~group["is_correct"]]["created_at"]
        first_error_date = error_dates.min().isoformat() if len(error_dates) > 0 else None
        last_error_date = error_dates.max().isoformat() if len(error_dates) > 0 else None
        
        # Confidence and trend
        if len(error_rates) > 0:
            recency_weight = calculate_recency_weight(assessment_dates)
            confidence = calculate_confidence(
                total_errors=total_errors,
                total_attempts=total_attempts,
                assessments_with_errors=assessments_with_errors,
                total_assessments=len(error_rates),
                recency_weight=recency_weight
            )
            trend, _ = calculate_trend(error_rates, assessment_dates)
        else:
            confidence = 0.0
            trend = "stable"
        
        profile = ConceptProfile(
            student_id=student_id,
            concept=concept,
            sub_concept=None,  # Aggregated at concept level
            total_attempts=total_attempts,
            total_errors=int(total_errors),
            error_breakdown=error_breakdown,
            assessments_with_errors=assessments_with_errors,
            first_error_date=first_error_date,
            last_error_date=last_error_date,
            trend=trend,
            confidence=confidence,
            error_rates=error_rates,
            assessment_dates=[d.isoformat() for d in assessment_dates]
        )
        profiles.append(profile)
    
    return profiles


def detect_learning_gaps(profiles: List[ConceptProfile],
                         min_errors: int = 3,
                         min_assessments: int = 2,
                         min_confidence: float = 0.30) -> List[LearningGap]:
    """
    Detect learning gaps from concept profiles.
    
    Args:
        profiles: List of ConceptProfile objects
        min_errors: Minimum total errors required
        min_assessments: Minimum assessments with errors
        min_confidence: Minimum confidence threshold
    
    Returns:
        List of LearningGap objects
    """
    gaps = []
    
    for profile in profiles:
        if detect_learning_gap(
            total_errors=profile.total_errors,
            assessments_with_errors=profile.assessments_with_errors,
            confidence=profile.confidence,
            min_errors=min_errors,
            min_assessments=min_assessments,
            min_confidence=min_confidence
        ):
            # Determine dominant error type
            if profile.error_breakdown:
                dominant_error = max(profile.error_breakdown, key=profile.error_breakdown.get)
            else:
                dominant_error = "unknown"
            
            gap = LearningGap(
                student_id=profile.student_id,
                concept=profile.concept,
                sub_concept=profile.sub_concept,
                dominant_error=dominant_error,
                evidence_count=profile.total_errors,
                assessments_count=profile.assessments_with_errors,
                confidence=profile.confidence,
                trend=profile.trend,
                detected_at=datetime.now().isoformat()
            )
            gaps.append(gap)
    
    return gaps


def get_student_gaps(student_id: str, gaps: List[LearningGap]) -> List[LearningGap]:
    """Filter gaps for a specific student."""
    return [g for g in gaps if g.student_id == student_id]


def get_class_gaps(gaps: List[LearningGap], min_students: int = 1) -> Dict[str, int]:
    """Get concept-level gap counts for a class."""
    concept_counts = {}
    for gap in gaps:
        key = f"{gap.concept}:{gap.sub_concept}" if gap.sub_concept else gap.concept
        concept_counts[key] = concept_counts.get(key, 0) + 1
    
    # Filter by minimum students
    return {k: v for k, v in concept_counts.items() if v >= min_students}


def get_concept_difficulty(profiles: List[ConceptProfile]) -> Dict[str, float]:
    """Get class-level error rate per concept."""
    concept_stats = {}
    for profile in profiles:
        key = f"{profile.concept}:{profile.sub_concept}" if profile.sub_concept else profile.concept
        if key not in concept_stats:
            concept_stats[key] = {"errors": 0, "attempts": 0}
        concept_stats[key]["errors"] += profile.total_errors
        concept_stats[key]["attempts"] += profile.total_attempts
    
    return {
        k: v["errors"] / v["attempts"] if v["attempts"] > 0 else 0.0
        for k, v in concept_stats.items()
    }


if __name__ == "__main__":
    from app.data.loader import load_all_synthetic
    
    students, questions, concept_map, responses = load_all_synthetic()
    
    print("Building concept profiles...")
    profiles = build_concept_profiles(responses, questions)
    print(f"Built {len(profiles)} profiles")
    
    print("\nDetecting learning gaps...")
    gaps = detect_learning_gaps(profiles)
    print(f"Detected {len(gaps)} learning gaps")
    
    # Show sample gaps
    print("\nSample gaps:")
    for gap in gaps[:10]:
        print(f"  {gap.student_id}: {gap.concept}:{gap.sub_concept} "
              f"({gap.dominant_error}, {gap.evidence_count} errors, "
              f"{gap.assessments_count} assessments, conf={gap.confidence:.2f}, {gap.trend})")
    
    # Class-level insights
    print("\nClass concept difficulty:")
    difficulty = get_concept_difficulty(profiles)
    for concept, rate in sorted(difficulty.items(), key=lambda x: -x[1]):
        print(f"  {concept}: {rate:.1%}")
    
    print("\nCommon gaps (affecting 3+ students):")
    class_gaps = get_class_gaps(gaps, min_students=3)
    for concept, count in sorted(class_gaps.items(), key=lambda x: -x[1]):
        print(f"  {concept}: {count} students")
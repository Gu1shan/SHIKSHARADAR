"""
Confidence calculation for Shiksha Radar.
Implements Wilson score interval with recency weighting for learning gap confidence.
"""
import numpy as np
from scipy import stats
from typing import List, Tuple, Optional
from datetime import datetime, timedelta


def wilson_score_interval(successes: int, trials: int, confidence: float = 0.95) -> Tuple[float, float]:
    """
    Calculate Wilson score interval for a binomial proportion.
    
    Args:
        successes: Number of successes (errors in our case)
        trials: Total number of trials (attempts)
        confidence: Confidence level (default 0.95)
    
    Returns:
        (lower_bound, upper_bound) of the confidence interval
    """
    if trials == 0:
        return (0.0, 1.0)
    
    z = stats.norm.ppf(1 - (1 - confidence) / 2)
    p = successes / trials
    
    denominator = 1 + z**2 / trials
    centre = (p + z**2 / (2 * trials)) / denominator
    half_width = (z * np.sqrt(p * (1 - p) / trials + z**2 / (4 * trials**2))) / denominator
    
    lower = max(0.0, centre - half_width)
    upper = min(1.0, centre + half_width)
    
    return (lower, upper)


def wilson_lower_bound(successes: int, trials: int, confidence: float = 0.95) -> float:
    """Get just the lower bound of Wilson score interval."""
    return wilson_score_interval(successes, trials, confidence)[0]


def calculate_confidence(total_errors: int, total_attempts: int, 
                         assessments_with_errors: int, total_assessments: int,
                         recency_weight: float = 1.0) -> float:
    """
    Calculate calibrated confidence for a learning gap.
    
    Uses a simplified heuristic suitable for classroom-scale data:
    - Error frequency component: min(1.0, total_errors / 10)  (saturates at 10 errors)
    - Recurrence component: assessments_with_errors / total_assessments
    - Recency weight
    
    Formula: min(0.95, error_freq * recurrence * recency_weight)
    
    Args:
        total_errors: Total errors across all assessments
        total_attempts: Total attempts across all assessments
        assessments_with_errors: Number of assessments with at least 1 error
        total_assessments: Total number of assessments
        recency_weight: Weight for recency (1.0 = most recent, decays for older)
    
    Returns:
        Confidence score between 0 and 0.95
    """
    if total_attempts == 0 or total_errors == 0:
        return 0.0
    
    # Error frequency: saturates at 10 errors
    error_freq = min(1.0, total_errors / 10.0)
    
    # Recurrence factor: fraction of assessments showing errors
    recurrence_factor = assessments_with_errors / total_assessments if total_assessments > 0 else 0
    
    # Base confidence
    base_confidence = error_freq * recurrence_factor * recency_weight
    
    # Cap at 0.95
    return min(0.95, base_confidence)


def calculate_recency_weight(assessment_dates: List[datetime], 
                             current_date: datetime = None,
                             half_life_weeks: float = 8.0) -> float:
    """
    Calculate recency weight based on assessment dates.
    
    More recent assessments get higher weight.
    Uses exponential decay with configurable half-life.
    
    Args:
        assessment_dates: List of assessment dates
        current_date: Reference date (default: now)
        half_life_weeks: Half-life in weeks for decay
    
    Returns:
        Normalized recency weight (0-1)
    """
    if current_date is None:
        current_date = datetime.now()
    
    if not assessment_dates:
        return 0.0
    
    # Convert to weeks ago
    weeks_ago = [(current_date - d).days / 7.0 for d in assessment_dates]
    
    # Exponential decay weights
    decay_rate = np.log(2) / half_life_weeks
    weights = np.exp(-decay_rate * np.array(weeks_ago))
    
    # Normalize so most recent = 1.0
    if weights.max() > 0:
        weights = weights / weights.max()
    
    return float(weights.mean())


def calculate_trend(error_rates: List[float], assessment_dates: List[datetime] = None) -> Tuple[str, float]:
    """
    Calculate trend of error rates over time.
    
    Uses linear regression slope on error rates vs time.
    
    Args:
        error_rates: List of error rates per assessment (chronological)
        assessment_dates: Optional dates for each assessment
    
    Returns:
        (trend_direction, slope)
        trend_direction: "increasing", "decreasing", or "stable"
        slope: slope of the regression line
    """
    if len(error_rates) < 2:
        return "stable", 0.0
    
    if assessment_dates is not None:
        x = np.array([(d - assessment_dates[0]).days for d in assessment_dates])
    else:
        x = np.arange(len(error_rates))
    
    y = np.array(error_rates)
    
    # Linear regression
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
    
    # Determine trend direction
    if abs(slope) < 0.01:  # Very small slope
        trend = "stable"
    elif slope > 0:
        trend = "increasing"
    else:
        trend = "decreasing"
    
    return trend, float(slope)


def detect_learning_gap(total_errors: int, 
                        assessments_with_errors: int,
                        confidence: float,
                        min_errors: int = 3,
                        min_assessments: int = 2,
                        min_confidence: float = 0.30) -> bool:
    """
    Determine if a learning gap exists based on thresholds.
    
    Args:
        total_errors: Total errors for this concept
        assessments_with_errors: Number of assessments with errors
        confidence: Calculated confidence score
        min_errors: Minimum total errors required
        min_assessments: Minimum assessments with errors
        min_confidence: Minimum confidence threshold
    
    Returns:
        True if learning gap detected
    """
    return (total_errors >= min_errors and 
            assessments_with_errors >= min_assessments and
            confidence >= min_confidence)


if __name__ == "__main__":
    # Test Wilson score interval
    print("=== Wilson Score Interval Tests ===")
    test_cases = [
        (3, 10),   # 3 errors out of 10
        (5, 20),   # 5 errors out of 20
        (10, 30),  # 10 errors out of 30
        (1, 5),    # 1 error out of 5
        (0, 10),   # No errors
    ]
    
    for errors, attempts in test_cases:
        lb, ub = wilson_score_interval(errors, attempts)
        print(f"Errors: {errors}/{attempts} -> Wilson LB: {lb:.3f}, UB: {ub:.3f}")
    
    print("\n=== Confidence Calculation Tests ===")
    conf_cases = [
        (7, 20, 3, 6),   # 7 errors, 20 attempts, 3/6 assessments with errors
        (3, 15, 2, 5),   # 3 errors, 15 attempts, 2/5 assessments
        (15, 30, 5, 6),  # High errors
        (1, 10, 1, 3),   # Low errors
    ]
    
    for errors, attempts, with_err, total_assess in conf_cases:
        conf = calculate_confidence(errors, attempts, with_err, total_assess)
        print(f"Errors: {errors}/{attempts}, Assessments: {with_err}/{total_assess} -> Confidence: {conf:.3f}")
    
    print("\n=== Trend Tests ===")
    # Increasing trend
    rates_inc = [0.1, 0.15, 0.2, 0.25, 0.3]
    trend, slope = calculate_trend(rates_inc)
    print(f"Increasing: {rates_inc} -> {trend} (slope: {slope:.4f})")
    
    # Decreasing trend
    rates_dec = [0.3, 0.25, 0.2, 0.15, 0.1]
    trend, slope = calculate_trend(rates_dec)
    print(f"Decreasing: {rates_dec} -> {trend} (slope: {slope:.4f})")
    
    # Stable
    rates_stable = [0.2, 0.21, 0.19, 0.2, 0.2]
    trend, slope = calculate_trend(rates_stable)
    print(f"Stable: {rates_stable} -> {trend} (slope: {slope:.4f})")
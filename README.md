# Shiksha Radar

AI-powered early learning-support platform that helps teachers identify **which specific concepts** students struggle with, **why** (evidence from repeated error patterns), and **what targeted intervention** might help — before learning gaps become learning failures.

## Overview

Shiksha Radar converts raw assessment answers into **longitudinal concept-level error-pattern intelligence** with:
- **Mistake Fingerprinting**: Longitudinal, multi-assessment error pattern profiles per student per concept
- **Evidence-Based Interventions**: Specific remediation recommendations with practice sets
- **Closed Feedback Loop**: Detect → Intervene → Reassess → Compare → "Gap Closed" or "Persisted"
- **Teacher-Centric Dashboard**: Interactive heatmaps, student profiles, class insights
- **Privacy-First**: Pseudonymized IDs, no PII, DPDP Act 2023 compliant design

## Quick Start

```bash
# Clone and setup
git clone <repo>
cd shiksha-radar

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run dashboard
streamlit run app/ui/app.py
```

Then click **"Load Demo Data (Synthetic Class 5 Math)"** to explore with sample data.

## Project Structure

```
shiksha-radar/
├── app/
│   ├── data/
│   │   ├── loader.py         # CSV loading & validation
│   │   ├── validator.py      # Schema validation
│   │   ├── normalizer.py     # Answer normalization
│   │   └── synthetic.py      # Synthetic data generator
│   ├── analytics/
│   │   ├── classifier.py     # Rule-based error classification
│   │   ├── concept_mapper.py # Concept mapping (rules + embeddings)
│   │   ├── confidence.py     # Wilson score + trend + confidence
│   │   └── profiler.py       # Concept profiles + learning gaps
│   └── ui/
│       └── app.py            # Streamlit dashboard (4 views)
├── data/
│   ├── synthetic/            # Generated CSV datasets
│   │   ├── students.csv
│   │   ├── questions.csv
│   │   ├── responses.csv
│   │   └── concept_map.csv
│   └── schemas/
│       ├── assessment_schema.json
│       └── question_schema.json
├── scripts/
│   └── generate_synthetic.py # Synthetic data generator script
├── requirements.txt
└── README.md
```

## Data Schemas

### students.csv
| Column | Type | Description |
|--------|------|-------------|
| student_id | string | Pseudonymized ID (e.g., Student_001) |
| grade | integer | Grade level (e.g., 5) |
| section | string | Section (A, B, C, D) |

### questions.csv
| Column | Type | Description |
|--------|------|-------------|
| question_id | string | Unique question ID |
| text | string | Question text |
| concept | string | Main concept (Fractions, Algebra, etc.) |
| sub_concept | string | Sub-concept (denominator_handling, sign_error, etc.) |
| difficulty | integer | 1=easy, 2=medium, 3=hard |
| expected_answer | string | Correct answer |

### responses.csv
| Column | Type | Description |
|--------|------|-------------|
| response_id | string | Unique response ID |
| student_id | string | Links to students.csv |
| assessment_id | string | Assessment identifier (ASM001, etc.) |
| question_id | string | Links to questions.csv |
| student_answer | string | Student's response |
| is_correct | boolean | Correct/incorrect |
| error_type | string | Error taxonomy category |
| created_at | string | ISO 8601 timestamp |

### concept_map.csv
| Column | Type | Description |
|--------|------|-------------|
| question_id | string | Links to questions.csv |
| concept | string | Main concept |
| sub_concept | string | Sub-concept |

## Error Taxonomy

| Category | Error Types |
|----------|-------------|
| **Conceptual** | misconception, wrong_approach, formula_selection |
| **Procedural** | denominator_handling, sign_error, simplification, carry_borrow, decimal_placement, unit_conversion |
| **Calculation** | arithmetic, multiplication_fact, division_fact |
| **Careless** | incomplete, misread, copy_error, transcription |
| **Unknown** | ambiguous, blank |

## Architecture

### MVP (Weeks 1-4) - Current
- **Stack**: Python, Pandas, Streamlit, Plotly
- **Data**: CSV files
- **AI**: Rule-based error classification, statistical confidence
- **Deploy**: Streamlit Community Cloud

### SIH Prototype (Weeks 5-8)
- **Add**: SQLite persistence, LLM explanations (Groq/Gemini), PDF reports
- **Features**: Multi-assessment tracking, intervention engine, reassessment loop

### Production (Post-SIH)
- **Stack**: FastAPI, PostgreSQL + TimescaleDB, React PWA
- **Features**: Auth, multi-user, offline-first PWA, monitoring

## Dashboard Views

1. **Class Overview** - KPI cards, concept difficulty bars, assessment timeline
2. **Student × Concept Heatmap** - Interactive grid showing gap status per student
3. **Student Profile** - Deep dive with evidence, confidence, trend, error breakdown
4. **Class Insights** - Common gaps, assessment trends, intervention tracking

## Development

### Generate Synthetic Data
```bash
python scripts/generate_synthetic.py
```

### Run Tests
```bash
# Data validation
python -m app.data.validator

# Error classification
python -m app.analytics.classifier

# Confidence calculation
python -m app.analytics.confidence

# Profiling & gap detection
python -m app.analytics.profiler
```

## Privacy & Responsible AI

- **Pseudonymized IDs only** (Student_001, no names)
- **No PII** in analytics pipeline
- **DPDP Act 2023** compliant design
- **No negative labels** - uses "possible learning gap", "repeated error pattern", "may benefit from additional support"
- **Evidence citations required** - every recommendation references error count, assessment count, confidence
- **Teacher override mandatory** - interventions only assigned after teacher approval
- **Confidence calibration** - Wilson score interval + recency weighting, capped at 95%

## License

MIT License - See LICENSE file for details.

## Acknowledgments

- NIPUN Bharat Mission (MoE) - FLN mission alignment
- NDEAR/Saral - Assessment building blocks
- ASER Centre - Learning crisis evidence
- ASSISTments - Educational data mining benchmark
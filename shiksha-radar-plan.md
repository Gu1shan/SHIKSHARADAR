# SHIKSHA RADAR — Comprehensive Research & Implementation Plan

**Find the learning gap before it becomes a learning failure.**

*Evidence-backed, beginner-buildable, SIH-competitive AI-powered learning-gap detection platform*

---

## Table of Contents

1. [Executive Summary](#part-1--executive-summary)
2. [Problem Research](#part-2--problem-research)
3. [Existing Solutions](#part-3--existing-solutions-analysis)
4. [Innovation](#part-4--innovation-what-is-novel)
5. [User Personas](#part-5--user-personas)
6. [Complete Product Workflow](#part-6--complete-product-workflow)
7. [Technical Architecture](#part-7--technical-architecture)
8. [AI Architecture](#part-8--ai-architecture)
9. [Mistake Fingerprinting](#part-9--mistake-fingerprinting-engine)
10. [Concept Mapping](#part-10--concept-mapping)
11. [Intervention Engine](#part-11--intervention-engine)
12. [Dashboard](#part-12--teacher-dashboard)
13. [Database](#part-13--database-design)
14. [Dataset](#part-14--dataset-strategy)
15. [Privacy & Responsible AI](#part-15--privacy--responsible-ai)
16. [Testing](#part-16--testing-strategy)
17. [Deployment](#part-17--deployment-architecture)
18. [Scalability](#part-18--scalability-analysis)
19. [Offline/Rural Deployment](#part-19--offline--low-bandwidth-mode)
20. [Multilingual Strategy](#part-20--multilingual-strategy)
21. [8–12 Week Roadmap](#part-21--8-12-week-learning--development-roadmap)
22. [Repository Structure](#part-22--repository-structure)
23. [SIH Evaluation](#part-23--sih-evaluation)
24. [SIH Demo](#part-24--sih-demo-3-minute-live-script)
25. [Future Research](#part-25--future-research-trajectory)
26. [First 7 Days](#part-26--first-7-days-concrete-start-plan)
27. [Sources & Citations](#sources--citations)

---

## PART 1 — EXECUTIVE SUMMARY

**Shiksha Radar** is an AI-powered early learning-support platform that helps teachers identify **which specific concepts** students struggle with, **why** (evidence from repeated error patterns), and **what targeted intervention** might help — before learning gaps become learning failures.

**The core insight**: Two students scoring 60% may have completely different learning needs. Student A struggles with fractions (denominator errors across 3 assessments). Student B struggles with algebra (sign errors) and geometry. A marks dashboard shows them as identical. Shiksha Radar shows the teacher the difference.

**Three-tier architecture**:
- **MVP** (Weeks 1–4): CSV upload → Pandas analysis → mistake detection → concept heatmaps → Streamlit dashboard
- **SIH Prototype** (Weeks 5–8): SQLite + multi-assessment tracking + student profiles + LLM explanations + intervention engine + reassessment loop
- **Production** (Post-SIH): FastAPI + PostgreSQL + authentication + multilingual + offline-first + monitoring

**Why this fits SIH**: Addresses NIPUN Bharat's FLN mission (foundational literacy/numeracy by Grade 3), aligns with NDEAR's "Saral" assessment building block and "VSK" governance dashboards, solves a real teacher pain point (concept-level insight vs. marks-only), uses explainable AI responsibly, and demonstrates measurable impact via the detect→intervene→reassess feedback loop.

---

## PART 2 — PROBLEM RESEARCH

### 2.1 The Learning Crisis in India (Verified Facts)

| Metric | Source | Finding |
|--------|--------|---------|
| **FLN Gap** | NIPUN Bharat Mission (MoE, 2021) | "17 crore out of 52 crore children (age 3–23) out of formal education; nearly 5 crore elementary students below required FLN level; only ~45% Class 5 govt school students can read Class 2 text" |
| **ASER 2024** | Pratham/ASER Centre | Nationwide household survey across ~600 districts, ~34,000 villages, ~500,000 children; consistently shows >50% Grade 5 children cannot read Grade 2 text or do basic subtraction |
| **Dropout** | NDEAR Presentation (NCERT, 2022) | "~85 lakh students drop out annually" |
| **Assessment Gap** | NDEAR/Saral | "1000 Million+ assessment records of 27 Million+ students scanned via Saral" — but this is **marks capture**, not **concept-level diagnostic** |

**Verified fact**: The Ministry of Education's NIPUN Bharat Mission (launched July 2021) targets universal Foundational Literacy and Numeracy by Grade 3 by 2026–27. The mission explicitly emphasizes: "Conducting meaningful assessments using quizzes, games etc." and "Tracking children's learning levels consistently" — but current systems (UDISE+, DIKSHA, Saral) capture **enrollment, infrastructure, and aggregate scores**, not **concept-level error patterns**.

### 2.2 Why Marks Alone Are Insufficient

```
Student A: 60% overall
  Fractions → 8 errors across 3 tests (denominator: 5, simplification: 2, addition: 1)
  Algebra   → 1 error
  Geometry  → 0 errors

Student B: 60% overall
  Fractions → 1 error
  Algebra   → 5 errors (sign: 3, formula selection: 2)
  Geometry  → 4 errors (area/perimeter confusion: 3, units: 1)
```

**Teacher needs**: "Student A needs fraction denominator remediation. Student B needs algebra sign rules + geometry concept clarification."
**Current dashboards show**: "Both 60%. Both need help."

---

## PART 3 — EXISTING SOLUTIONS ANALYSIS

### 3.1 Government Platforms (Verified from Official Sources)

| Platform | Purpose | Strengths | Gaps for Shiksha Radar |
|----------|---------|-----------|------------------------|
| **UDISE+** (udiseplus.gov.in) | School census: enrollment, infrastructure, teachers, facilities | 14.67 lakh schools, 24.72 cr students, 1.02 cr teachers (AY 2025–26); official MoE statistics | **No student-level assessment data**; no concept mapping; no error analysis |
| **DIKSHA** (diksha.gov.in) | Content delivery: e-content, QR-coded textbooks, courses, quizzes | 18 languages; energized textbooks; question banks; analytics dashboard; NDEAR building blocks | **Content-focused**, not diagnostic; quizzes give scores, not error-pattern analysis; teacher sees "attempted/completed," not "repeated denominator errors" |
| **Saral** (NDEAR building block) | Assessment scanning: OMR/phygital scanning of paper assessments | 1B+ records scanned; 27M+ students; used in Gujarat VSK, other states | **Captures marks**; maps questions to competencies but **no longitudinal error-pattern detection**; no "mistake fingerprinting" |
| **Vidya Samiksha Kendra (VSK)** Gujarat | Governance dashboard: real-time monitoring of 54K schools, 1.15Cr students | PM Award 2021; World Bank global good practice; integrates UDISE + health + assessments | **Admin/governance view** (district/state); not **teacher-facing concept-level diagnostic**; no intervention recommendations |
| **NDEAR** (ndear.gov.in) | Architectural blueprint: building blocks for interoperable ed-tech | Federated, privacy-by-design, longitudinal records, open-source building blocks | **Framework**, not application; Shiksha Radar can **use** NDEAR blocks (Saral for input, VSK-style analytics for output) |

### 3.2 Commercial/Research Systems

| System | Concept-Level Analysis | Mistake Fingerprinting | Recurring Error Detection | Evidence-Based Intervention | Teacher Feedback Loop | Explainable AI |
|--------|------------------------|------------------------|---------------------------|----------------------------|----------------------|----------------|
| **Khan Academy** | ✓ (skill map) | ✗ | Partial (streaks) | ✓ (practice) | ✗ | Partial |
| **Byju's / Vedantu** | ✓ | ✗ | ✗ | ✓ (adaptive) | ✗ | ✗ |
| **Mindspark (EI)** | ✓ | Partial | ✓ | ✓ | Partial | ✗ |
| **DreamBox (US)** | ✓ | ✓ (adaptive) | ✓ | ✓ | ✓ | Partial |
| **ASSISTments (US)** | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ (research-grade) |
| **Shiksha Radar (proposed)** | ✓ | ✓ (core innovation) | ✓ (core) | ✓ (core) | ✓ (core) | ✓ (by design) |

**Key differentiator**: Shiksha Radar's **mistake fingerprinting** — longitudinal, concept-granular, error-type-specific pattern detection with evidence trails and confidence scores — is not a primary feature of any existing Indian government or commercial platform. ASSISTments (WPI, US) comes closest but is not designed for Indian curriculum/language/context.

### 3.3 What Exists / What Works Well / The Remaining Gap

- **What already exists**: UDISE+ (census data), DIKSHA (content), Saral (marks scanning), VSK (governance dashboards), commercial adaptive learning platforms.
- **What it does well**: Massive-scale data collection, content distribution, aggregate monitoring, adaptive practice.
- **The gap**: No system converts raw assessment answers into **longitudinal concept-level error-pattern intelligence** that a classroom teacher can act on, with evidence and confidence, and a closed intervention→reassessment loop.
- **How Shiksha Radar is genuinely different**: It is (a) concept-granular, (b) error-type-specific, (c) longitudinal, (d) evidence-cited with confidence scores, (e) teacher-facing rather than admin-facing, (f) intervention-loop-closed, (g) privacy-first by design.

---

## PART 4 — INNOVATION: WHAT IS NOVEL

### 4.1 Mistake Fingerprinting (Core Innovation)

**Definition**: A longitudinal, multi-assessment error pattern profile per student per concept, decomposed by error type, with recurrence tracking, trend analysis, and calibrated confidence.

```
Traditional:  "Student scored 60% on Fractions"
Shiksha Radar: "Fractions → 7 errors across 3 assessments (84% confidence)
                ├─ Denominator handling: 5 errors (recurring, ↑ trend)
                ├─ Simplification: 1 error (isolated)
                └─ Addition: 1 error (careless)
                → Recommended: Equivalent fractions review + 5 targeted denominator problems"
```

### 4.2 Evidence-Based Intervention Loop

```
Detect (concept + error type + confidence)
    ↓
Recommend (specific remediation + practice set)
    ↓
Teacher assigns / Student practices
    ↓
Reassess (same concept, comparable difficulty)
    ↓
Compare (pre vs post error frequency + confidence)
    ↓
Close loop: "Improved: denominator errors 5→1" or "Persisted: needs different approach"
```

### 4.3 Explainable-by-Design AI

- **Deterministic core**: Mistake detection, concept mapping, aggregation = rules + statistics (auditable)
- **LLM only for**: Natural-language explanation of structured evidence, practice question generation, translation
- **LLM never**: Decides "weak student," assigns risk scores, replaces teacher judgment

### 4.4 Privacy-First Architecture

- **Pseudonymized IDs** (Student_001) in prototype
- **No PII** in analytics pipeline
- **DPDP Act 2023 compliant**: verifiable parental consent flow designed for production; data minimization; purpose limitation; no behavioral tracking/advertising

---

## PART 5 — USER PERSONAS

| Persona | Role | Pain Point | Shiksha Radar Value |
|---------|------|------------|---------------------|
| **Priya, Grade 5 Teacher** | Govt school, 40 students, multi-grade | Marks register shows scores; no time to analyze each paper; doesn't know *which* concept to reteach | Upload CSV → 30 sec → sees "Fractions: 12/40 students struggling with denominators" → gets ready-to-print practice sheets |
| **Rajesh, Block Resource Person** | Supports 50 schools | Needs to identify systemic gaps across cluster for training planning | Aggregate view: "Fractions denominator errors high in 35/50 schools → district workshop needed" |
| **Anita, Student (indirect)** | Grade 5 | Gets generic "do more practice" homework | Gets targeted 5-question worksheet on *her* specific gap; sees progress next test |
| **Principal / Admin** | School-level | Reports to district on learning outcomes | Auto-generated "Learning Gap Report" with evidence for SMC/SMDC meetings |

---

## PART 6 — COMPLETE PRODUCT WORKFLOW

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        SHIKSHA RADAR WORKFLOW                                │
└─────────────────────────────────────────────────────────────────────────────┘

1. ASSESSMENT INPUT
   ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
   │ Paper test  │───▶│  CSV/Excel  │───▶│  Upload to  │
   │ (existing)  │    │  template   │    │  Shiksha    │
   └─────────────┘    └─────────────┘    │  Radar      │
                                          └──────┬──────┘
                                                 │
2. DATA PROCESSING                                ▼
   ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
   │ Validate    │───▶│ Normalize   │───▶│ Map Q→      │
   │ schema,     │    │ answers     │    │ Concept +   │
   │ types, IDs  │    │ (case,      │    │ Error Type  │
   │ duplicates  │    │  whitespace)│    │ (rules +    │
   └─────────────┘    └─────────────┘    │  embeddings)│
                                          └──────┬──────┘
                                                 │
3. MISTAKE DETECTION                              ▼
   ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
   │ Compare     │───▶│ Classify    │───▶│ Aggregate   │
   │ student vs  │    │ error type  │    │ per student │
   │ expected    │    │ (determin-  │    │ per concept │
   │ answer      │    │  istic)     │    │ over time   │
   └─────────────┘    └─────────────┘    └──────┬──────┘
                                                 │
4. LEARNING PROFILE                               ▼
   ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
   │ Frequency   │───▶│ Recurrence  │───▶│ Confidence  │
   │ + Trend     │    │ (3+ assess-  │    │ Score       │
   │ analysis    │    │  ments)     │    │ (0–1)       │
   └─────────────┘    └─────────────┘    └──────┬──────┘
                                                 │
5. TEACHER DASHBOARD                              ▼
   ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
   │ Class       │───▶│ Student     │───▶│ Concept     │
   │ Heatmap     │    │ Profile     │    │ Drill-down  │
   └─────────────┘    └─────────────┘    └──────┬──────┘
                                                 │
6. INTERVENTION ENGINE                            ▼
   ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
   │ LLM         │───▶│ Practice    │───▶│ Teacher     │
   │ Explanation │    │ Generator   │    │ Review +    │
   │ + Recomm.   │    │ (targeted)  │    │ Assign      │
   └─────────────┘    └─────────────┘    └──────┬──────┘
                                                 │
7. REASSESSMENT & LOOP CLOSURE                    ▼
   ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
   │ Next        │───▶│ Compare     │───▶│ "Gap Closed"│
   │ Assessment  │    │ Pre vs Post │    │ or "Persist"│
   └─────────────┘    └─────────────┘    └─────────────┘
```

---

## PART 7 — TECHNICAL ARCHITECTURE

### 7.1 Level 1 — Beginner MVP (Weeks 1–4)

```
┌────────────────────────────────────────────────────────────┐
│                        MVP ARCHITECTURE                     │
├────────────────────────────────────────────────────────────┤
│                                                             │
│  Teacher                                                    │
│    │                                                        │
│    ▼                                                        │
│  ┌─────────┐    ┌─────────┐    ┌──────────────┐            │
│  │ CSV     │───▶│ Pandas  │───▶│ Mistake      │            │
│  │ Upload  │    │ Loader  │    │ Detection    │            │
│  └─────────┘    └─────────┘    └──────┬───────┘            │
│                                        │                    │
│                                        ▼                    │
│                              ┌──────────────────┐           │
│                              │ Concept Mapping  │           │
│                              │ (Rule-based +    │           │
│                              │  MiniLM embed)   │           │
│                              └────────┬─────────┘           │
│                                       │                     │
│                                       ▼                     │
│                              ┌──────────────────┐           │
│                              │ Pattern Analysis │           │
│                              │ (freq, recurrence,│           │
│                              │  trend, conf)    │           │
│                              └────────┬─────────┘           │
│                                       │                     │
│                                       ▼                     │
│                              ┌──────────────────┐           │
│                              │ Streamlit        │           │
│                              │ Dashboard        │           │
│                              │ (Heatmap,        │           │
│                              │  Profiles,       │           │
│                              │  Recommendations)│           │
│                              └──────────────────┘           │
│                                                             │
└────────────────────────────────────────────────────────────┘

Stack: Python 3.11+, Pandas, Streamlit, sentence-transformers (MiniLM-L6-v2),
       scikit-learn (clustering), Plotly, openpyxl
Data:  CSV files (assessments, questions, concept map)
Deploy: Streamlit Community Cloud (free) or Hugging Face Spaces
```

**Why this stack**:
- **Pandas**: Only data tool needed; handles CSV, validation, aggregation
- **Streamlit**: Zero-frontend-code dashboard; perfect for teacher demo
- **sentence-transformers (MiniLM-L6-v2)**: 384-dim embeddings, 80MB, runs on CPU, maps questions→concepts semantically
- **scikit-learn**: KMeans for error clustering, isolation forest for anomaly detection (optional)
- **No database**: CSV is sufficient for MVP; teaches data engineering fundamentals

### 7.2 Level 2 — SIH Prototype (Weeks 5–8)

```
┌────────────────────────────────────────────────────────────┐
│                      SIH PROTOTYPE                          │
├────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────┐    ┌──────────┐    ┌────────────────────┐    │
│  │ Streamlit│───▶│ SQLite   │───▶│ Analytics Engine   │    │
│  │ Frontend │    │ (local)  │    │ (Pandas + SQL)     │    │
│  └──────────┘    └──────────┘    └─────────┬──────────┘    │
│                                             │              │
│                    ┌────────────────────────┼────────┐     │
│                    ▼                        ▼        ▼     │
│             ┌───────────┐            ┌──────────┐ ┌──────┐ │
│             │ LLM Layer │            │Intervention│ │Export│ │
│             │(explanations,│           │ Engine   │ │Report│ │
│             │ questions,  │           │(recs +    │ │(PDF) │ │
│             │ translation)│           │ tracking) │ └──────┘ │
│             └───────────┘            └──────────┘           │
│                                                             │
│  New: Multi-assessment tracking, Student profiles,         │
│       Confidence calibration, Progress charts,             │
│       Class-level insights, PDF report export              │
│                                                             │
└────────────────────────────────────────────────────────────┘

Additions: SQLite (persistence), LLM API (Groq/Gemini),
           ReportLab (PDF), session state (multi-page Streamlit)
```

### 7.3 Level 3 — Production Architecture (Post-SIH)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        PRODUCTION ARCHITECTURE                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌────────────────────┐    │
│  │ React/   │───▶│ API      │───▶│ Auth     │───▶│ Application        │    │
│  │ Next.js  │    │ Gateway  │    │ (OAuth2/ │    │ Backend (FastAPI)  │    │
│  │ (PWA)    │    │ (Kong/   │    │  JWT)    │    │                    │    │
│  │          │    │  Traefik)│    │          │    │                    │    │
│  └──────────┘    └──────────┘    └──────────┘    └─────────┬──────────┘    │
│                                                             │              │
│                    ┌────────────────────────────────────────┼────────┐     │
│                    ▼                                        ▼        ▼     │
│             ┌───────────┐  ┌───────────┐  ┌───────────┐ ┌──────────┐     │
│             │ Data      │  │ Analytics │  │ AI/ML     │ │ Object   │     │
│             │ Processing│  │ Engine    │  │ Services  │ │ Storage  │     │
│             │ (Celery/  │  │ (SQL +    │  │ (Embedding│ │ (MinIO/  │     │
│             │  Dramatiq)│  │  Pandas)  │  │  + LLM)   │ │  S3)     │     │
│             └───────────┘  └───────────┘  └───────────┘ └──────────┘     │
│                    │                                        │              │
│                    ▼                                        ▼              │
│             ┌───────────┐                            ┌───────────┐         │
│             │ PostgreSQL│                            │ Redis     │         │
│             │ (Primary) │                            │ (Cache/   │         │
│             │ + Timescale│                           │  Queue)   │         │
│             └───────────┘                            └───────────┘         │
│                                                                              │
│  Monitoring: Prometheus + Grafana + Sentry + Structured Logging            │
│  Deployment: Docker + Kubernetes (K3s for edge) or Cloud Run               │
│  Offline: Service Worker + IndexedDB + Background Sync                     │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

**What's actually needed now vs. future**:

| Component | MVP | SIH Prototype | Production |
|-----------|-----|---------------|------------|
| Database | CSV | SQLite | PostgreSQL + TimescaleDB |
| Auth | None | Simple PIN | OAuth2/JWT + RBAC |
| Frontend | Streamlit | Streamlit | React PWA |
| API | None | None | FastAPI |
| LLM | Optional | Groq/Gemini API | Self-hosted + API |
| Deployment | Streamlit Cloud | Streamlit Cloud | Docker + K8s/Cloud Run |
| Monitoring | print() | Basic logging | Prometheus/Grafana |
| Offline | No | No | Service Worker + IndexedDB |

**Deployment verdict**: Start with Streamlit Cloud. Migrate to FastAPI + Cloud Run only when you need auth, multi-user, or an API for a mobile app.

---

## PART 8 — AI ARCHITECTURE

### 8.1 Where AI/ML Is Used (and Why)

| Component | Technique | Why AI | Why Not Pure Rules |
|-----------|-----------|--------|-------------------|
| **Concept Mapping** | sentence-transformers (MiniLM-L6-v2) + cosine similarity | Questions phrased variably; rules miss "find the fraction" vs "what fraction" | Rules work for exact-match; embeddings handle paraphrase |
| **Error Classification** | Rule-based (regex + keyword) + optional KMeans clustering | Deterministic, auditable, explainable | Rules cover 80%; clustering finds novel patterns |
| **Confidence Scoring** | Statistical (Wilson score interval + recency weighting) | Transparent, calibrated | No black-box ML needed |
| **LLM Explanation** | Groq Llama-3.1-70B / Gemini 1.5 Flash | Natural language for teachers; multilingual | Templates are rigid; LLM adapts to context |
| **Practice Generation** | LLM few-shot + template | Generates varied, concept-aligned questions | Manual creation doesn't scale |
| **Trend Detection** | Mann-Kendall test / linear regression slope | Statistical significance, not ML | Simple, interpretable |

### 8.2 LLM Integration Architecture (Hallucination-Resistant)

```
Structured Evidence (JSON) ──▶ Prompt Template ──▶ LLM ──▶ Teacher-Friendly Output
                                    │
                                    ▼
                          ┌─────────────────────┐
                          │ GUARDRAILS          │
                          │ • No student names  │
                          │ • No predictions    │
                          │ • Cite evidence     │
                          │ • Confidence range  │
                          │ • "May benefit" not │
                          │   "will fail"       │
                          └─────────────────────┘
```

**Prompt Template Design** (conceptual — no code):

```
You are a supportive teaching assistant. Given structured evidence about a student's
learning pattern, write a concise, encouraging explanation for the teacher.

EVIDENCE: {structured JSON — concept, error count, assessment count,
           error breakdown, trend, confidence}

RULES:
- Never use labels like "weak," "poor," "failing," "at risk"
- Use: "may benefit from additional support," "shows repeated difficulty with"
- Always cite the evidence (e.g., "based on 7 errors across 3 assessments")
- Include confidence as "confidence: X%"
- Suggest 2-3 specific, actionable next steps
- Keep under 150 words
- Tone: professional, supportive, evidence-based

OUTPUT FORMAT:
**Concept**: {concept}
**Pattern**: {pattern_summary}
**Evidence**: {evidence_citation}
**Confidence**: {confidence}%
**Suggested Next Steps**:
1. {step1}
2. {step2}
3. {step3}
```

**Evidence JSON fed to LLM** (no PII, structured, verifiable):

```json
{
  "student_id": "Student_001",
  "concept": "Fractions - Denominator Handling",
  "total_errors": 7,
  "assessments_analyzed": 3,
  "error_breakdown": {"denominator": 5, "simplification": 1, "addition": 1},
  "trend": "increasing",
  "confidence": 0.84,
  "recent_assessment_date": "2025-01-15"
}
```

### 8.3 How to Reduce Hallucinations

1. **Ground every claim in evidence**: LLM only sees structured JSON; all facts come from the deterministic engine.
2. **Constrain output format**: Template with placeholders; validated after generation.
3. **Forbidden-label + missing-evidence validator**: Post-generation check blocks output that violates responsible-AI rules.
4. **Temperature low** (0.2–0.3) for explanation tasks.
5. **Fallback chain**: If LLM fails/times out → template-based explanation (always available).
6. **Never feed PII**: LLM receives only pseudonymized IDs and structured stats.

---

## PART 9 — MISTAKE FINGERPRINTING ENGINE

### 9.1 Core Data Model (Conceptual)

- **AnswerRecord**: student_id, assessment_id, question_id, concept, sub_concept, student_answer, expected_answer, is_correct, error_type, timestamp
- **ConceptProfile**: student_id, concept, total_attempts, total_errors, error_breakdown (per error type), assessments_with_errors, first/last error date, trend (increasing/stable/decreasing), confidence (0–1)

### 9.2 Error Taxonomy (Mathematics — Extensible)

| Category | Error Types |
|----------|-------------|
| **Conceptual** | misconception, wrong_approach, formula_selection |
| **Procedural** | denominator_handling, sign_error, simplification, carry_borrow, decimal_placement, unit_conversion |
| **Calculation** | arithmetic, multiplication_fact, division_fact |
| **Careless** | incomplete, misread, copy_error, transcription |
| **Unknown** | ambiguous, blank |

### 9.3 MVP Pipeline (Deterministic, Transparent)

```
1. Load & validate CSV (schema, types, IDs, duplicates)
2. Normalize answers (lowercase, strip, unicode-normalize)
3. Score: exact match after normalization
4. Classify errors via rule-based keyword/regex per error type
5. Map question → concept (rule lookup → embedding fallback → teacher-review flag)
6. Aggregate per student × concept over time:
   - Error frequency (count, rate)
   - Recurrence (assessments with errors)
   - Trend (slope of error rate across assessments)
   - Confidence (Wilson score interval × recency weight, capped at 0.95)
7. Detect learning gaps via thresholds:
   - total_errors ≥ 3 AND
   - assessments_with_errors ≥ 2 AND
   - confidence ≥ 0.70
8. Output: LearningGap(student, concept, dominant_error, evidence_count,
                      assessments, confidence, trend)
```

### 9.4 Confidence Calculation (Conceptual Formula)

```
Confidence = min(0.95, Wilson_lower_bound(error_rate, n) × 1.2 × recency_weight)
```

- **Wilson score interval**: statistically sound confidence for a proportion, avoids over-confidence on small samples.
- **Recency weight**: errors in the most recent assessment count more than old ones (decay factor).
- **Cap at 0.95**: never claims certainty.

### 9.5 Advanced Version (Research-Grade — NOT for MVP)

| Technique | Purpose | Complexity | When to Add |
|-----------|---------|------------|-------------|
| **Bayesian Knowledge Tracing (BKT)** | Model latent knowledge state per concept | Medium | Post-SIH; needs sequential data |
| **Deep Knowledge Tracing (DKT/LSTM)** | Capture complex temporal dependencies | High | Research project; needs 10K+ sequences |
| **Embedding-based Error Clustering** | Discover novel error types automatically | Medium | When rule taxonomy saturates |
| **IRT (Item Response Theory)** | Calibrate question difficulty/discrimination | Medium | When question bank >500 items |
| **Causal Inference** | Estimate intervention effect (A/B) | High | Production with RCT capability |

**Recommendation**: Build MVP with deterministic rules + statistical confidence. Add BKT only if you have longitudinal data (10+ assessments/student) and want a research paper.

---

## PART 10 — CONCEPT MAPPING

### 10.1 Three-Tier Approach

```
Question → Rule lookup (exact ID match) → Found? → Use rule
                    ↓ No
         Embedding similarity → Confidence ≥ 0.65? → Use embedding
                    ↓ No
         Flag for teacher review → "Unmapped question"
```

### 10.2 Rule-Based (MVP — Start Here)

- **questions.csv** carries `question_id → concept, sub_concept` columns.
- 100% accurate for curated question banks; zero compute; fully auditable.
- Cons: manual maintenance; does not handle unseen questions.

### 10.3 Embedding-Enhanced (SIH Prototype)

- **Model**: `paraphrase-MiniLM-L6-v2` (384-dim, 80MB, CPU-friendly, Apache 2.0 license).
- **Process**:
  1. Pre-compute concept embeddings from concept descriptions.
  2. Encode the question text → vector.
  3. Cosine similarity vs. each concept description embedding.
  4. Best match above threshold (0.65) → mapped; below → "Unknown / flag for review."
- **Why embeddings**: handles paraphrase ("find the fraction" vs "what fraction"); zero-code for unseen questions.
- **Why not pure embeddings**: rules are deterministic and auditable for a known question bank; embeddings add flexibility for open-ended import.

### 10.4 Embeddings Explained Simply

- **Embedding**: converting text into a list of numbers (a vector) that captures meaning — similar texts get similar vectors.
- **Vector similarity**: cosine similarity measures how "aligned" two vectors are (1 = identical meaning, 0 = unrelated).
- **Why useful**: the model has "read" lots of language, so it knows "simplify" ≈ "reduce" in math contexts.
- **Multilingual option**: `paraphrase-multilingual-MiniLM-L12-v2` supports Hindi/Telugu/Tamil/Bengali/Marathi (420MB, still CPU-friendly).

---

## PART 11 — INTERVENTION ENGINE

### 11.1 Recommendation Logic (Conceptual)

**LearningGap → Intervention mapping**:

```
LearningGap(student_id, concept, dominant_error, evidence_count, assessments, confidence, trend)
    ↓
Intervention:
  - concept, dominant_error
  - evidence_summary ("7 errors across 3 assessments")
  - confidence (from gap)
  - steps (3–4): conceptual → procedural → practice → metacognitive
  - practice_questions (5 targeted, generated or retrieved)
  - reassessment_plan (when, how many questions, success criteria)
```

**Intervention step templates** (per concept × dominant_error):

| Concept | Error | Sample Steps |
|---------|-------|--------------|
| Fractions | denominator_handling | Review equivalent fractions with visual models → Practice finding common denominators (5 guided) → 5 targeted worksheet problems |
| Fractions | simplification | Review GCF and simplification rules → Practice simplifying 10 fractions with step feedback |
| Algebra | sign_error | Review integer rules (neg × neg = pos) → 10 sign-focused problems with error highlighting |
| Algebra | formula_selection | Create a formula decision flowchart → Practice identifying equation type before solving |
| Geometry | area_perimeter_confusion | Visual contrast area vs perimeter → 5 mixed problems with labelled diagrams |

### 11.2 LLM-Enhanced Generation (SIH Prototype)

LLM receives the same structured evidence JSON and returns:
- **explanation** (teacher-friendly, 2–3 sentences)
- **steps** (3–4 with type tags)
- **practice_questions** (5 with answers, aligned to the error type)
- **reassessment_plan** (when, how many, success criteria)

Output is **parsed and validated** — structure checked, forbidden labels blocked, evidence cited.

### 11.3 Feedback Loop Tracking (The Core Product Feature)

```
InterventionRecord:
  intervention_id, student_id, gap, intervention,
  assigned_date, teacher_notes,
  reassessment_date, reassessment_results, outcome

close_loop():
  → filter reassessment responses for same student + concept + sub_concept
  → compute pre_error_rate, post_error_rate
  → proportion z-test (simplified statistical test)
  → outcome:
      improved  → post_rate < 0.20 AND p < 0.05
      worsened  → post_rate ≥ pre_rate
      persisted → otherwise
  → store {pre_rate, post_rate, p_value}
```

This **detect → intervene → reassess → compare** loop is a major product differentiator and the central demo story.

---

## PART 12 — TEACHER DASHBOARD

### 12.1 Screen 1: Class Overview (Landing)

- KPI cards: Students, Assessments, Concepts, Students needing support.
- Class concept difficulty bars (error rate % per concept).
- "Students needing support" list (clickable → profile).
- Decision: *"Fractions is a class-wide issue → whole-class reteach + targeted small groups."*

### 12.2 Screen 2: Student × Concept Heatmap

- Grid: rows = students, columns = concepts, cells = 🔴 high-confidence gap / 🟡 emerging / 🟢 on track.
- Decision: *"Group S001, S004 for fractions pull-out; S002, S007 for algebra."*

### 12.3 Screen 3: Student Profile (Deep Dive)

- Overall stats + list of concepts with gaps.
- Per gap: evidence (N errors across M assessments), error breakdown, trend (↗/→/↘), last-seen date, **confidence**.
- Recommended intervention (from engine).
- Progress timeline (error rate per assessment).
- PDF report export.
- Decision: *Teacher sees exact evidence + confidence + actionable steps, not just "needs help."*

### 12.4 Screen 4: Class-Level Insights

- Common gaps affecting ≥30% of class (with counts).
- Assessment trends (class avg error rate per concept over time; "gap widening" alert).
- Intervention tracking: active / completed / improved / persisted.
- Decision: *"Fractions worsening across assessments → adjust pacing; schedule block-level training."*

### 12.5 Dashboard Principles

- Every chart maps to a **decision**, never decoration.
- Every claim shows **evidence count + confidence**.
- **Teacher override is mandatory**: interventions only become "assigned" after teacher approval.

---

## PART 13 — DATABASE DESIGN

### 13.1 MVP (CSV-Based — No Database)

```
data/
├── assessments/assessment_1.csv, assessment_2.csv ...
├── questions.csv          # question_id, text, concept, sub_concept, difficulty, expected_answer
├── concept_map.csv        # question_id → concept, sub_concept
└── students.csv           # student_id, grade, section (pseudonymized)
```

### 13.2 SIH Prototype (SQLite) — Table Design

| Table | Key Columns | Purpose |
|-------|-------------|---------|
| **students** | student_id (PK), grade, section | Pseudonymized roster |
| **assessments** | assessment_id (PK), title, subject, grade, date_administered | Assessment metadata |
| **questions** | question_id (PK), assessment_id (FK), question_text, concept, sub_concept, difficulty, expected_answer, max_marks | Question bank per assessment |
| **responses** | response_id (PK), student_id, assessment_id, question_id, student_answer, is_correct, error_type, confidence_score, created_at | Raw answer records (source of truth) |
| **concept_profiles** | student_id, concept, sub_concept, total_attempts, total_errors, error_breakdown (JSON), assessments_with_errors, first/last_error_date, trend, confidence, updated_at | Materialized analytics |
| **learning_gaps** | gap_id (PK), student_id, concept, sub_concept, dominant_error, evidence_count, assessments_count, confidence, trend, detected_at, status (active/intervening/resolved/persisted) | Detected gaps |
| **interventions** | intervention_id (PK), gap_id (FK), teacher_id, steps (JSON), practice_questions (JSON), reassessment_plan (JSON), assigned_at, teacher_notes | Intervention records |
| **intervention_outcomes** | outcome_id (PK), intervention_id (FK), reassessment_id, pre_error_rate, post_error_rate, p_value, outcome, closed_at | Loop-closure results |

**Key indexes**: responses(student_id, concept), concept_profiles(student_id), learning_gaps(status).

### 13.3 Production (PostgreSQL + TimescaleDB)

- **responses** → TimescaleDB hypertable (time-partitioned; monthly chunks) for time-series scale.
- **concept_profiles** → partitioned by hash(student_id).
- Add tables: users, roles, role_permissions, audit_log, consent_records (for DPDP compliance).

---

## PART 14 — DATASET STRATEGY

### 14.1 Existing Public Datasets

| Dataset | Source | Size | License | Use Case | Indian Context |
|---------|--------|------|---------|----------|----------------|
| **Student Performance** | UCI ML Repo | 649 students, 30 features | CC BY 4.0 | Baseline modeling, testing | Portuguese secondary; not Indian curriculum |
| **Educational Data Mining** | Kaggle (sizlingdhairya1) | 6000 students | Unknown | Exploration only | Balochistan (Pakistan); demographic features |
| **ASSISTments** | ASSISTments.org | 100K+ students, millions of interactions | Research use | Knowledge tracing research | US middle school math; gold standard for KT |
| **KDD Cup 2010** | PSLC DataShop | 19M+ transactions | Research | EDM benchmark | US algebra; cognitive tutor logs |
| **GSM8K / MATH** | HuggingFace / OpenAI | 8.5K / 12.5K problems | MIT / Custom | Math reasoning eval | Competition math; not school curriculum |
| **K12 Math Standards** | HuggingFace (robworks) | Standards-aligned items | Apache 2.0 | Concept mapping reference | US Common Core; adaptable |

**Critical gap**: No public dataset contains **Indian school assessments with concept-tagged questions, student answers, and error annotations**. UDISE+ has enrollment/infrastructure data, not learning data. Saral data is not public.

### 14.2 Synthetic Data Strategy (Primary for MVP/SIH)

**Design principles**:
- Aligned to **NCERT Class 3–8 Mathematics** (NIPUN Bharat focus).
- Realistic error patterns from math-education research (denominator errors, sign errors, etc.).
- Longitudinal: 5–8 assessments across an academic year.
- Diverse student archetypes (below).
- **No PII** — pseudonymized IDs only.

**Student archetypes** (the demo must show each):

| Archetype | Pattern |
|-----------|---------|
| Student A | Fractions difficulty (high error rate only in Fractions, denominator-dominant) |
| Student B | Algebra difficulty (sign errors + formula selection) |
| Student C | Random mistakes (moderate error rate across all concepts, no clear pattern) |
| Student D | Improving over time (error rate decays across assessments) |
| Student E | Persistent difficulties (high error rate across all concepts, stable) |
| Student F | On track (low error rate everywhere) |

**Generation plan** (conceptual):
1. Build NCERT-aligned concept hierarchy: Fractions (denominator_handling, simplification, addition, subtraction, multiplication, comparison), Decimals, Algebra (patterns, variables, equations, sign rules), Geometry (2D, 3D, area/perimeter, angles, symmetry), Measurement, Data Handling.
2. Generate a question bank: ~3 questions × 3 difficulty levels × per sub-concept.
3. Assign archetype per student; compute per-concept error probability from archetype.
4. For each assessment (6–8 per student): sample ~20 questions stratified by concept; mark correct/error by probability; on error, pick an error type from the concept's error-pattern distribution and distort the expected answer accordingly.
5. Timestamps spread over the academic year (Jul–Feb).
6. Output files: `students.csv`, `questions.csv`, `responses.csv`, `concept_map.csv`.

**Scale**: 50 students × 6 assessments × 20 questions ≈ 6,000 response rows — small enough for a beginner, rich enough for a compelling demo.

**Legal/ethical note**: All synthetic; no real children's data. Explicitly documented as such.

---

## PART 15 — PRIVACY & RESPONSIBLE AI

### 15.1 DPDP Act 2023 Compliance (Verified from Official Gazette)

| Requirement | Shiksha Radar Approach |
|-------------|------------------------|
| **Verifiable Parental Consent** (Sec 9) | Production: digital consent flow via school; MVP: not applicable (synthetic data only) |
| **No Tracking/Behavioral Monitoring** (Sec 9) | No cookies, no fingerprinting, no cross-site tracking; only assessment data |
| **No Targeted Advertising** (Sec 9) | No ads; no third-party data sharing |
| **Data Minimization** (Sec 8) | Collect only: pseudonymized ID, grade, section, assessment responses |
| **Purpose Limitation** (Sec 4) | Only: learning-gap detection + intervention support |
| **Storage Limitation** (Sec 8) | Auto-delete responses after 2 academic years; profiles anonymized for research |
| **Security Safeguards** (Sec 8) | Encryption at rest (AES-256), in transit (TLS 1.3), RBAC, audit logs |
| **Breach Notification** | 72-hour notification to Data Protection Board + affected parents |

### 15.2 Responsible AI Safeguards (Design Principles)

| Safeguard | Implementation | Enforcement Point |
|-----------|----------------|-------------------|
| **No Negative Labels** | Output validator blocks "weak," "failing," "at risk," "slow learner" | LLM response filter + UI copy review |
| **Evidence Citations Required** | Every recommendation references error count, assessment count, confidence | LLM prompt template + post-generation check |
| **Confidence Calibration** | Wilson score interval + recency weighting; never 100% | Analytics engine (deterministic) |
| **Teacher Override Mandatory** | Intervention not "assigned" until teacher clicks "Approve & Assign" | Workflow state machine |
| **No Automated High-Stakes Decisions** | System never outputs "promote/hold back," "special ed referral" | Product scope boundary |
| **Data Minimization** | Only pseudonymized ID, grade, section, responses; no name, DOB, address, biometrics | Schema design |
| **Purpose Limitation** | Data used only for: gap detection → intervention → reassessment | Access control + audit log |
| **Retention Policy** | Raw responses: 2 academic years; aggregated profiles: 5 years (anonymized) | Automated cleanup job |
| **Audit Trail** | Every data access, model inference, teacher action logged with timestamp + actor | Structured logging |
| **Explainability** | Deterministic core (rules + stats) auditable; LLM only for phrasing | Architecture separation |

**Approved language** (always used, never "weak/bad/will fail"):
- "possible learning gap"
- "repeated error pattern"
- "may benefit from additional support"
- "confidence: X%"

### 15.3 Production Data Flow (Privacy-by-Design)

```
School Admin → Creates Teacher Account (email + school code)
       ↓
Teacher → Uploads CSV (Student_001, Student_002... no names)
       ↓
System → Validates → Processes → Stores in SQLite (local) / PostgreSQL (prod)
       ↓
Analytics → Runs on pseudonymized data only
       ↓
LLM → Receives structured JSON (no PII) → Returns explanation
       ↓
Teacher → Sees dashboard → Approves intervention → Downloads worksheet
       ↓
Reassessment → Uploaded → Loop closed → Outcome recorded
       ↓
Auto-delete → Raw responses purged after 2 years per policy
```

---

## PART 16 — TESTING STRATEGY

### 16.1 Functional Correctness Tests

| Test Category | Specific Tests |
|---------------|----------------|
| **CSV Import** | Valid schema, missing columns, extra columns, duplicate headers, encoding (UTF-8/UTF-16) |
| **Data Validation** | Student ID format, date ranges, score bounds, required fields |
| **Scoring** | Exact match, case-insensitive, whitespace normalization, numeric tolerance (±0.01) |
| **Error Classification** | Each taxonomy category: denominator, sign, simplification, arithmetic, careless |
| **Concept Mapping** | Rule-based exact match, embedding fallback, unknown-concept handling |
| **Profile Aggregation** | Single assessment, multiple assessments, missing assessments, trend calculation |
| **Gap Detection** | Threshold boundaries (min_errors, min_assessments, min_confidence) |

### 16.2 AI/ML Evaluation Tests

| Metric | Target | Method |
|--------|--------|--------|
| **Concept Mapping Accuracy** | ≥90% on labeled question set | 200 human-labeled questions; compare rule vs embedding vs hybrid |
| **Error Classification Precision** | ≥85% per error type | 500 labeled student answers; confusion matrix |
| **Confidence Calibration** | Brier score < 0.15; reliability diagram near diagonal | 1000 predictions vs outcomes |
| **LLM Hallucination Rate** | <2% (fabricated evidence, wrong confidence, missing citations) | 100 structured evidence inputs → human eval |
| **Recommendation Relevance** | Teacher rating ≥4/5 on "actionable & specific" | SIH demo user study (5 teachers) |
| **Consistency** | Same evidence → same recommendation (deterministic core) | 10 repeated runs |

### 16.3 System & Edge-Case Tests

| Scenario | Expected Behavior |
|----------|-------------------|
| Empty CSV | Clear error: "No data rows found" |
| Malformed CSV | Row-level errors reported; valid rows processed |
| Missing answers | Treated as "blank" → error_type: "incomplete" |
| Duplicate student IDs | Warning + merge or reject (configurable) |
| Duplicate question IDs | Error: "Question ID not unique" |
| Assessment out of order | Timeline sorts by date; trend uses chronological order |
| Single assessment | Gap detection requires min_assessments=2 → no gaps reported |
| All-correct answers | Profile shows 0 errors; confidence = 0 |
| API timeout (LLM) | Fallback to template explanation; log warning |
| Large file (10K rows) | Processes in <30s; memory <500MB |

### 16.4 Ground Truth Dataset (Manual Labeling)

Create a golden set of ~200 manually labeled records:
- 50 questions → concept + sub_concept labels
- 100 student answers → error_type labels (by a math educator)
- 50 student-concept histories → "learning gap: yes/no" labels

Used for: regression testing, threshold tuning, demo validation.

---

## PART 17 — DEPLOYMENT ARCHITECTURE

### 17.1 MVP Deployment (Free, Beginner-Friendly) — Streamlit Community Cloud

```
1. Push repo to GitHub (public or private)
2. Connect to Streamlit Community Cloud
3. Set secrets: LLM_API_KEY (Groq/Gemini), optional HF_TOKEN
4. Deploy → Public URL: https://shiksha-radar.streamlit.app

Pros: Free, HTTPS, auto-sleep/wake, GitHub integration
Cons: Sleeps after inactivity; 1GB RAM; no persistent filesystem
```

**Dependency list (MVP)**: streamlit, pandas, numpy, plotly, sentence-transformers, scikit-learn, openpyxl, python-dotenv, groq (or google-generativeai).

**Secrets management**: `.streamlit/secrets.toml` locally; Cloud dashboard in production. Never commit real keys (use `.streamlit/secrets.toml.example` and `.gitignore`).

### 17.2 SIH Prototype Deployment

- Same as MVP + SQLite persistence (ephemeral on Streamlit Cloud → use `st.session_state` + upload/download for demo).
- Pre-load synthetic data in the repo so the demo works offline.

### 17.3 Production Deployment (Post-SIH)

| Layer | Option A (Cloud) | Option B (Self-Hosted/Edge) |
|-------|------------------|------------------------------|
| **Frontend** | Vercel (Next.js PWA) | Nginx + React build on VM |
| **API** | Cloud Run (FastAPI) | K3s + FastAPI pods |
| **Database** | Cloud SQL (PostgreSQL) | PostgreSQL + TimescaleDB on VM |
| **Cache/Queue** | Redis (Memorystore) | Redis on VM |
| **Object Storage** | GCS / S3 | MinIO |
| **Monitoring** | Cloud Monitoring + Sentry | Prometheus + Grafana + Loki |
| **CI/CD** | GitHub Actions → Cloud Run | GitHub Actions → ArgoCD → K3s |
| **Cost (est.)** | $50–200/mo at 50K students | $30–100/mo (Hetzner/DigitalOcean) |

**API key protection** (all tiers): server-side only, never in frontend, rotate keys, scope keys, enable billing alerts, use a vault/service account in production.

---

## PART 18 — SCALABILITY ANALYSIS

### 18.1 Scale Targets & Bottlenecks

| Scale | Students | Responses/yr | Key Bottleneck | Solution |
|-------|----------|--------------|----------------|----------|
| **MVP** | 50 | 6,000 | None (CSV + Pandas) | — |
| **SIH Demo** | 200 | 32,000 | SQLite write contention | WAL mode; batch inserts |
| **School** | 500 | 100,000 | Pandas memory | Chunked processing; Polars |
| **Cluster** | 5,000 | 1M | Single-node compute | Celery workers; Redis queue |
| **District** | 50,000 | 12M | DB writes + analytics | TimescaleDB; materialized views |
| **State** | 500K | 120M | Inference latency | Batch embedding; model caching |

### 18.2 Scaling Strategy by Component

| Component | 50 → 500 | 500 → 5,000 | 5,000 → 50,000 |
|-----------|----------|-------------|----------------|
| **Data Ingestion** | Pandas chunked | Celery + Redis queue | Kafka + Flink/Spark |
| **Embedding** | CPU batch (MiniLM) | GPU batch (BGE-M3) | Async inference service + cache |
| **Analytics** | SQL aggregation | Materialized views + refresh | Pre-computed OLAP cubes |
| **LLM Calls** | Sync (few/day) | Async queue + cache | Dedicated inference endpoint |
| **Database** | SQLite WAL | PostgreSQL + read replicas | TimescaleDB + partitioning |
| **Frontend** | Streamlit | Streamlit + caching | React PWA + CDN |
| **Auth** | None | Simple JWT | OAuth2 + RBAC + SSO |

### 18.3 Cost Estimates (Monthly, USD)

| Scale | Compute | Database | LLM API | Storage | Total |
|-------|---------|----------|---------|---------|-------|
| 500 | $0 (Streamlit) | $0 (SQLite) | $5 | $0 | **$5** |
| 5,000 | $20 (Cloud Run) | $15 (Cloud SQL) | $50 | $5 | **$90** |
| 50,000 | $150 (K8s) | $200 (Timescale) | $300 | $50 | **$700** |

---

## PART 19 — OFFLINE / LOW-BANDWIDTH MODE

### 19.1 Feasibility Assessment

| Feature | Offline Capable? | Sync Strategy |
|---------|------------------|---------------|
| CSV Upload & Analysis | ✅ Full | Local-first; sync when online |
| Dashboard View | ✅ Full (cached data) | Read-only offline |
| Concept Mapping (rules) | ✅ Full | No model needed |
| Concept Mapping (embeddings) | ⚠️ Partial | Cache embeddings; fallback to rules |
| LLM Explanations | ❌ No | Queue requests; process when online |
| Practice Generation (templates) | ✅ Full | Pre-bundled templates |
| Practice Generation (LLM) | ❌ No | Queue → sync |
| Reassessment Upload | ✅ Full | Local queue → batch sync |
| Intervention Tracking | ✅ Full | Local SQLite → sync |

### 19.2 Offline-First Architecture (PWA)

```
SERVICE WORKER (Workbox)
  ├── Cache: App shell (HTML, CSS, JS, Wasm)
  ├── Cache: Embedding model (ONNX/MiniLM quantized ~20MB)
  ├── Cache: Question bank + concept map (JSON)
  ├── Cache: Template interventions (JSON)
  └── Background Sync: queue uploads + LLM requests

INDEXEDDB (Dexie.js)
  ├── students, assessments, responses (local copy)
  ├── computed profiles (synced from server)
  └── pending_mutations (upload queue)

OFFLINE-CAPABLE MODULES
  ├── Pandas → Polars (Wasm) or SQL.js (SQLite in browser)
  ├── Rule-based error classification
  ├── Rule-based concept mapping
  ├── Statistical aggregation (JS implementation)
  └── Template-based intervention + worksheet generation
```

**MVP Decision**: Build offline as **Phase 2 (Post-SIH)**. For SIH demo, assume internet at block level. Document the offline architecture in the proposal.

---

## PART 20 — MULTILINGUAL STRATEGY

### 20.1 Language Support Matrix

| Language | UI (Teacher) | LLM Explanations | Question Text | Embedding Model | Status |
|----------|--------------|------------------|---------------|-----------------|--------|
| English | ✅ | ✅ | ✅ | MiniLM-L6-v2 | Ready |
| Hindi | ✅ (i18n) | ✅ (Gemini/Llama) | ✅ | multilingual-MiniLM-L12 | Ready |
| Telugu | ✅ (i18n) | ✅ (Gemini 1.5) | ⚠️ Limited | multilingual-MiniLM-L12 | Planned |
| Tamil | ✅ (i18n) | ✅ (Gemini 1.5) | ⚠️ Limited | multilingual-MiniLM-L12 | Planned |
| Bengali | ✅ (i18n) | ✅ (Gemini 1.5) | ⚠️ Limited | multilingual-MiniLM-L12 | Planned |
| Marathi | ✅ (i18n) | ✅ (Gemini 1.5) | ⚠️ Limited | multilingual-MiniLM-L12 | Planned |

**Honest caveat**: Do not claim support for a language until the chosen model/API actually supports it adequately. Gemini 1.5 Flash natively supports 35+ Indian languages; MiniLM-multilingual supports the listed scripts; but question-bank content in non-English needs human verification.

### 20.2 Implementation Approach

- **UI i18n**: locale JSON files (`en.json`, `hi.json`, `te.json`, ...) + a session-state language toggle.
- **LLM multilingual**: prompt in English → request output in target language → back-translation sanity check (optional).
- **Embedding swap**: English-only (MiniLM-L6-v2, 80MB) for MVP; multilingual (MiniLM-L12-v2, 420MB) for SIH; both CPU-friendly.
- **Question bank**: store per-question translations keyed by `question_id`.
- **SIH scope**: English + Hindi UI + Hindi LLM explanations; other languages documented as future work.

---

## PART 21 — 8–12 WEEK LEARNING + DEVELOPMENT ROADMAP

### 21.1 Week-by-Week Plan

| Week | Learn (Concepts) | Build (Implementation) | Deliverable (Working) | Test / Verify |
|------|------------------|------------------------|----------------------|---------------|
| **1** | Python project structure, Git, venv, CSV I/O, basic Pandas (read, filter, groupby) | Repo init; `data/` folder; synthetic data generator; CSV loader with validation | `python generate_data.py` creates 3 CSVs; loader prints summary stats | Row counts match; no NaN in required cols; schema valid |
| **2** | Pandas advanced (merge, pivot, apply), normalization, answer comparison, error taxonomy | Answer normalizer; rule-based error classifier; rule-based concept mapper | `python analyze.py assessment_1.csv` prints per-student error breakdown | Golden set: 50 answers classified ≥85% correct |
| **3** | Aggregation, Wilson confidence, trend detection, dataclasses | ConceptProfile builder; LearningGap detector; confidence + trend calculators | `python profile.py` outputs JSON profiles + gaps for all students | Known archetypes detected correctly (fractions_struggler → fractions gap) |
| **4** | Streamlit basics (layout, widgets, session_state, caching, Plotly) | Multi-page dashboard: Overview, Heatmap, Student Profile, Class Insights | `streamlit run app.py` → interactive dashboard with synthetic data | All 4 screens render; heatmap clickable; profile shows evidence + confidence |
| **5** | SQLite (sqlite3/SQLAlchemy), schema design, migrations | SQLite schema; multi-assessment upload; profile persistence | Upload 3 assessments → profiles accumulate; gaps update | Second upload adds data; trend updates; no duplicate rows |
| **6** | LLM APIs (Groq/Gemini), prompt engineering, structured output, hallucination guards | LLM explanation layer; prompt template with evidence JSON; output validator | "Explain" button on profile → teacher-friendly explanation with citations | 10 test cases: no forbidden labels; evidence cited; confidence shown |
| **7** | Intervention design, template engine, PDF generation, feedback loop | Intervention engine (templates + LLM); PDF worksheet generator; outcome tracking | "Generate Intervention" → PDF worksheet + reassessment plan | Worksheet has 5 targeted questions; success criteria defined |
| **8** | End-to-end integration, edge cases, performance, demo polish, docs | Full workflow: Upload → Detect → Explain → Intervene → Reassess → Close Loop | **SIH Demo Ready**: 3-min live demo on synthetic data | Dry run: 50 students, 6 assessments → dashboard + interventions < 2 min |
| **9** | (Buffer) Embedding concept mapping, multilingual UI, PDF class report | Embedding fallback; Hindi UI toggle; PDF class report | Embedding maps unseen questions; Hindi dashboard works; PDF downloads | 20 unseen questions ≥80% accuracy; Hindi renders |
| **10** | (Buffer) Deployment, secrets, monitoring, load test, SIH submission prep | Streamlit Cloud deploy; secrets config; README; demo video; submission docs | Public URL works; demo video recorded; SIH forms complete | URL loads <10s; no keys exposed; demo <3 min |

### 21.2 Skills Gained per Week

| Week | Technical Skills | Professional Skills |
|------|------------------|---------------------|
| 1 | Git, venv, Pandas basics, data generation | Project setup, reproducibility |
| 2 | Data cleaning, rule-based NLP, taxonomy design | Test-driven development |
| 3 | Statistical thinking, OOP, algorithm design | Evidence-based decision making |
| 4 | Web app framework, data viz, state management | User-centered design |
| 5 | SQL, ORM, persistence, schema evolution | Data engineering fundamentals |
| 6 | LLM integration, prompt engineering, guardrails | Responsible AI practices |
| 7 | Template engines, PDF generation, workflow state | Product thinking (intervention loop) |
| 8 | Integration testing, performance profiling, demo craft | Technical communication |
| 9 | Embeddings, i18n, advanced viz | Scalability awareness |
| 10 | Cloud deployment, security, documentation | Delivery & handoff |

---

## PART 22 — REPOSITORY STRUCTURE

```
shiksha-radar/
│
├── app/                          # Main application package
│   ├── __init__.py
│   ├── config.py                 # Settings, constants, model names
│   ├── data/
│   │   ├── loader.py             # CSV/Excel validation & loading
│   │   ├── validator.py          # Schema validation (pandera)
│   │   ├── normalizer.py         # Answer normalization
│   │   └── synthetic.py          # Synthetic data generator
│   ├── analytics/
│   │   ├── classifier.py         # Rule-based error classification
│   │   ├── concept_mapper.py     # Rule + embedding concept mapping
│   │   ├── profiler.py           # ConceptProfile + LearningGap
│   │   ├── confidence.py         # Wilson score, trend, calibration
│   │   └── intervention.py       # Intervention engine + templates
│   ├── ai/
│   │   ├── llm_client.py         # Groq/Gemini wrapper + retry
│   │   ├── prompts.py            # Prompt templates + validators
│   │   └── embeddings.py         # SentenceTransformer wrapper
│   ├── db/
│   │   ├── models.py             # SQLAlchemy / dataclasses
│   │   ├── repository.py         # CRUD + analytics queries
│   │   └── migrations/           # SQL migration files
│   ├── ui/
│   │   ├── pages/
│   │   │   ├── 1_Overview.py
│   │   │   ├── 2_Heatmap.py
│   │   │   ├── 3_Student_Profile.py
│   │   │   └── 4_Class_Insights.py
│   │   ├── components.py         # Reusable UI components
│   │   └── styles.py             # CSS/theme
│   └── utils/
│       ├── export.py             # PDF/CSV export
│       ├── i18n.py               # Localization
│       └── logging.py            # Structured logging
│
├── data/                         # Data files (large files gitignored)
│   ├── synthetic/                # Generated synthetic datasets
│   │   ├── students.csv
│   │   ├── questions.csv
│   │   ├── responses.csv
│   │   └── concept_map.csv
│   ├── golden_set/               # Manually labeled test data
│   │   ├── questions_labeled.csv
│   │   ├── answers_labeled.csv
│   │   └── gaps_labeled.csv
│   └── schemas/                  # JSON schemas for validation
│       ├── assessment_schema.json
│       └── question_schema.json
│
├── tests/
│   ├── conftest.py               # Pytest fixtures
│   ├── unit/                     # loader, classifier, profiler, confidence
│   ├── integration/              # pipeline, dashboard
│   └── ai_eval/                  # concept mapping, error classification, LLM output
│
├── scripts/
│   ├── generate_synthetic.py
│   ├── evaluate_golden_set.py
│   ├── calibrate_confidence.py
│   └── deploy_check.py
│
├── docs/
│   ├── architecture.md
│   ├── api_reference.md
│   ├── deployment.md
│   ├── privacy.md
│   ├── sih_submission.md
│   └── demo_script.md
│
├── .streamlit/
│   ├── config.toml
│   └── secrets.toml.example
│
├── .github/workflows/
│   ├── ci.yml
│   └── deploy.yml
│
├── requirements.txt
├── requirements-dev.txt
├── pyproject.toml
├── README.md
├── LICENSE
├── .gitignore
├── .env.example
└── Dockerfile
```

**Simplified MVP structure (Weeks 1–4)**:
```
shiksha-radar/
├── app/
│   ├── data/loader.py
│   ├── analytics/{classifier, profiler, confidence}.py
│   └── ui/pages/*.py
├── data/synthetic/*.csv
├── tests/
├── requirements.txt
├── README.md
└── .streamlit/secrets.toml
```

**Directory explanations**: `app/` = all source code (data handling, analytics, AI, DB, UI, utilities); `data/` = datasets + schemas (synthetic + golden set); `tests/` = unit/integration/AI-eval tests; `scripts/` = one-off automation; `docs/` = architecture, API, deployment, privacy, SIH, demo docs; `.github/` = CI/CD; root config files = requirements, README, env, Docker, license.

---

## PART 23 — SIH EVALUATION

### 23.1 SIH Judging Criteria Mapping (Based on Official Guidelines — Round 3: Functionality/Relevance, Performance/Final Demo, Clarity of Presentation)

| Criterion | Weight (Typical) | Shiksha Radar Score | Evidence |
|-----------|------------------|---------------------|----------|
| **Innovation** | 25% | 8.5/10 | Mistake fingerprinting + evidence-based intervention loop = novel for Indian context |
| **Problem Relevance** | 20% | 9.5/10 | Directly addresses NIPUN Bharat FLN mission; teacher pain point validated by ASER |
| **Technical Feasibility** | 20% | 9/10 | MVP built in 4 weeks by beginner; deterministic core; no exotic dependencies |
| **Scalability** | 15% | 8/10 | Architecture scales to 50K+; offline design documented; NDEAR-aligned |
| **Social Impact** | 10% | 9/10 | Targets govt schools; privacy-first; multilingual; supports teacher agency |
| **User Experience** | 10% | 8/10 | Teacher-centric dashboard; 30-sec upload → actionable insight; Hindi support |

**Overall estimated score: 8.7/10** — competitive for national finals (with a real pilot).

### 23.2 Why Judges Might Reject (Critical Self-Assessment)

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| **"Just a dashboard"** — looks like visualization, not AI | Medium | Emphasize deterministic mistake fingerprinting + statistical confidence + LLM only for explanation; show the pipeline |
| **"Synthetic data only"** — no real school validation | High | **Must**: partner with 1–2 schools for a pilot before SIH finals; show real teacher testimonial |
| **"Concept mapping too simple"** — rules don't generalize | Medium | Demo embedding fallback; show 20 unseen questions mapped correctly |
| **"Intervention not proven"** — no RCT evidence | High | Frame as "teacher decision support," not "proven efficacy"; show feedback loop design |
| **"Privacy claims unproven"** — no DPDP audit | Low | Show code: no PII fields; consent flow designed; audit log structure |
| **"Not scalable to rural"** — needs internet | Medium | Document offline architecture; show PWA design; note Saral works offline-first |

### 23.3 Changes That Would Make It Significantly Stronger

1. **Real pilot data**: Partner with 1 govt school (via DIET/SCERT contact) for a 2-week pilot. Even 30 students × 2 assessments = real validation.
2. **Teacher co-design video**: 2-min clip of a teacher using the prototype → "This saves me 2 hours/week."
3. **NDEAR integration demo**: Show how Shiksha Radar *consumes* Saral CSV output → positions as ecosystem player, not standalone.
4. **Impact simulation**: "If deployed in 100 schools, 5000 students, projected gap reduction based on feedback-loop closure rate."
5. **Open-source commitment**: MIT license; GitHub repo with issues labeled "good first issue" — shows sustainability.

### 23.4 Likely Judge Questions (and Answers)

| Question | Answer |
|----------|--------|
| "How is this different from an Excel marks sheet?" | Excel shows scores; Shiksha Radar shows concept × error-type × trend × confidence across assessments — and a closed intervention loop. |
| "How do you know the concept mapping is correct?" | Rule-based for the question bank (100%); embedding fallback validated ≥90% on labeled set; unknown questions flagged for teacher review. |
| "What about students who are just careless?" | Careless errors are a separate taxonomy category; gap detection requires recurrence across ≥2 assessments to avoid over-alerting. |
| "How will this work without internet in a village?" | Offline-first design: local CSV + rules + cached embeddings + template interventions; LLM only when online. |
| "What is your privacy story for minors?" | DPDP Act 2023: pseudonymized IDs, no PII, verifiable parental consent in production, data minimization, no tracking/advertising, 2-year retention. |
| "Why not use an LLM to grade everything?" | LLMs are unreliable and non-reproducible for deterministic grading; we use rules for detection and LLMs only for teacher-facing explanation. |

---

## PART 24 — SIH DEMO (3-MINUTE LIVE SCRIPT)

### 24.1 Demo Narrative Arc

| Time | Scene | Screen Action | Narrator Script |
|------|-------|---------------|-----------------|
| **0:00–0:30** | **Problem** | Show marks register (Excel): 40 students, all 55–65% | "Meet Priya. She teaches Grade 5. 40 students. Marks look similar. But do they learn the same?" |
| **0:30–0:50** | **Upload** | Drag CSV → "Processing..." (2 sec) → Dashboard loads | "She uploads last Friday's test. Shiksha Radar reads every answer." |
| **0:50–1:20** | **Detection** | Class Overview → Concept Difficulty: Fractions 38% (red) | "Instantly: Fractions is a class-wide issue. 14 of 40 students struggling." |
| **1:20–1:50** | **Student Drill-Down** | Click Student_001 → Profile: Fractions denominator, 84% confidence | "Student_001: 7 denominator errors across 3 tests. Not 'weak in math' — a specific gap." |
| **1:50–2:20** | **Intervention** | Click "Generate Intervention" → PDF worksheet downloads | "One click: targeted worksheet + reassessment plan. Teacher reviews, approves, prints." |
| **2:20–2:45** | **Reassessment** | Upload next test → Gap status: "Improved" | "Next week: reassess. Gap closed. Evidence-based. Loop complete." |
| **2:45–3:00** | **Impact** | Class Insights: "Fractions gap reduced 38%→22% in 4 weeks" + Privacy badge | "Scale to 100 schools. Privacy-first. NDEAR-aligned. Teacher stays in charge." |

### 24.2 Demo Technical Checklist

- [ ] Synthetic data pre-loaded (no upload wait)
- [ ] All 4 dashboard pages tested
- [ ] LLM explanation cached (avoid API latency)
- [ ] PDF generation works offline
- [ ] Browser: Chrome, 1080p, zoom 100%
- [ ] Backup: screen recording if live fails
- [ ] QR code to public URL on final slide

---

## PART 25 — FUTURE RESEARCH TRAJECTORY

### 25.1 From Hackathon to Research Project

| Phase | Goal | Output | Timeline |
|-------|------|--------|----------|
| **SIH Prototype** | Working demo + teacher validation | GitHub repo + demo video + pilot feedback | 0–3 months |
| **Research Pilot** | Controlled study in 5–10 schools | Pre/post learning gains; teacher workflow study | 3–9 months |
| **Publication** | EDM/LAK/AIED paper | "Mistake Fingerprinting: Longitudinal Error Pattern Analysis for Early Learning Support" | 9–15 months |
| **Open Platform** | Extensible framework for researchers | Plugin architecture for BKT/DKT/IRT models | 12–24 months |
| **Policy Integration** | Adoption in state FLN programs | MoU with SCERT/SSA; NDEAR building-block contribution | 18–36 months |

### 25.2 Research Questions Enabled

1. **RQ1**: How does mistake-fingerprinting accuracy vary with assessment frequency and concept granularity?
2. **RQ2**: What intervention types (conceptual vs procedural vs metacognitive) close specific error patterns most effectively?
3. **RQ3**: How does teacher trust in AI explanations vary with evidence transparency (confidence + citations)?
4. **RQ4**: Can synthetic-data augmentation improve cold-start concept mapping for low-resource languages?
5. **RQ5**: What is the minimum assessment frequency for reliable gap detection in Indian classroom contexts?

---

## PART 26 — FIRST 7 DAYS: CONCRETE START PLAN

### Day 1 (2–3 hours): Environment & Repo
- Install Python 3.11+, Git, VS Code
- `git init shiksha-radar` and create the folder structure
- Create venv, install pandas, streamlit, numpy, plotly
- Write README with tagline + one-liner
- **Commit**: "chore: init repo with structure"

### Day 2 (2–3 hours): Synthetic Data Generator
- Implement the synthetic data generator (archetypes from Part 14)
- Generate: 50 students, 6 assessments, 20 questions each
- Output: `students.csv`, `questions.csv`, `responses.csv`, `concept_map.csv`
- Verify row counts; **Commit**: "feat: synthetic data generator for Class 5 Math"

### Day 3 (2–3 hours): CSV Loader + Validation
- Implement loader (load + validate schema) and answer normalizer
- Test all CSVs: column types, null counts, unique students
- **Commit**: "feat: data loading & validation pipeline"

### Day 4 (3–4 hours): Error Classification (Rule-Based)
- Define the error taxonomy
- Implement rule-based classifier (exact match → correct; else keyword/regex per error type)
- Create 20 golden test cases; run pytest
- **Commit**: "feat: rule-based error classifier with taxonomy"

### Day 5 (3–4 hours): Concept Mapping + Profiling
- Rule-based concept mapper
- ConceptProfile builder + LearningGap detector
- Wilson confidence + trend (slope of error rate)
- Test full pipeline on synthetic data
- **Commit**: "feat: concept profiling & learning gap detection"

### Day 6 (3–4 hours): Streamlit Dashboard (Core)
- Overview page (metrics + concept difficulty bars)
- Heatmap page (student × concept, Plotly)
- Student profile page (evidence + confidence + trend)
- Class insights page (common gaps + trends)
- Sidebar upload; **Commit**: "feat: Streamlit dashboard with 4 views"

### Day 7 (2–3 hours): Polish & Document
- Pin `requirements.txt`
- Write `docs/architecture.md` and `docs/demo_script.md`
- Record 2-min screen capture
- Push to GitHub; enable Streamlit Cloud deploy (optional)
- **Commit**: "chore: docs, requirements, demo ready"

### Week 1 Success Criteria
1. **Working pipeline**: CSV → error classification → concept profiles → learning gaps
2. **Interactive dashboard**: Upload synthetic data → heatmap → student drill-down → evidence + confidence
3. **Clean codebase**: modular, tested, documented, version-controlled
4. **Foundation ready**: Week 2 adds SQLite + multi-assessment; Week 3 adds LLM explanations

---

## SOURCES & CITATIONS

### Indian Education Ecosystem (Primary Sources)
- **NIPUN Bharat Mission** — Ministry of Education, launched 5 July 2021. Vision: universal FLN by Grade 3 by 2026–27. static.pib.gov.in (PIB doc 2021); cdnbbsr.s3waas.gov.in NIPUN Bharat FLN presentation.
- **UDISE+** — Department of School Education & Literacy, MoE. udiseplus.gov.in. AY 2025–26: 14.67 lakh schools, 24.72 crore students, 1.02 crore teachers.
- **DIKSHA** — NCERT/MoE. diksha.gov.in; pmevidya.education.gov.in/diksha.html (features: 18 languages, QR-coded textbooks, assessments, "advanced AI/ML platform coming soon").
- **NDEAR** — Ministry of Education, Budget 2021–22 (PIB PRID 1696880, 10 Feb 2021). ndear.gov.in. Reference use cases: Saral, VSK, DIKSHA assessments.
- **Saral** — NDEAR building block; "1000 Million+ assessment records of 27 Million+ students" (ndear.gov.in/all-projects.html).
- **Vidya Samiksha Kendra (VSK)** — Gujarat; 54,000 schools, 1.15 crore students, 500 crore data points/yr; PM Award 2021; World Bank good practice (NITI For States, frontiertech.niti.gov.in, updated 16 Jul 2023).
- **ASER 2024** — ASER Centre / Pratham. asercentre.org; asercentre.org/aser-2024/. ~600 districts, ~34,000 villages, ~500,000 children.

### SIH Sources
- **SIH 2025 Problem Statements** — sih.gov.in/sih2025PS (official portal). Smart Education theme includes: Gamified Learning Platform for Rural Education, Automated Attendance, Digital Learning Platform for Rural Schools, Smart Classroom & Timetable Scheduler, Authenticity Validator for Academia. SIH 2025 dataset mirrored at Kaggle (theprtsh/sih-2025-problem-dataset).
- **SIH 2024 Problem Statements** — sih.gov.in/sih2024PS; 216 problem statements (159 software / 57 hardware) across 17 themes (engineersplanet.com analysis).
- **Evaluation Guidelines** — siceval.mic.gov.in/assets/img/Evaluation_Guidelines_for_sih2024.pdf. Round 3 criteria: Functionality/Relevance to problem statement, Performance/Final Demo, Clarity/coherence/persuasiveness of presentation.
- **Note**: SIH themes and problem statements change yearly. Verify the current year's Smart Education problem statements on sih.gov.in before finalizing the submission angle. The themes listed are verified for 2024–25 cycles; assumptions for future cycles are flagged as such.

### Privacy & Responsible AI
- **Digital Personal Data Protection Act, 2023** — India Code (indiacode.nic.in). Section 8 (security safeguards, data minimization, purpose limitation), Section 9 (children's data: verifiable parental consent; prohibition on tracking/behavioural monitoring/targeted advertising of children). Summary analyses: Spice Route Legal (Oct 2024), Maheshwari & Co (Oct 2025).

### Academic / Technical Research
- **Learning analytics / early warning systems** — Springer (2019), "Using learning analytics to develop early-warning system" (Int J Educ Technol High Educ, 10.1186/s41239-019-0172-z).
- **Knowledge tracing** — BKT vs DKT comparison (ERIC EJ1195512); Deep Knowledge Tracing + temporal causal inference (MDPI Appl. Sci. 2025); srcML-DKT (ERIC ED675671, EDM 2025).
- **Misconception/error analysis in math education** — "Error analysis in algebra learning" (ERIC EJ1428049); "Correcting Mathematics Students' Misconceptions, Not Mistakes" (Holmes 2013, ERIC EJ1020065); "A Benchmark for math misconceptions" (Springer, Discover Education, Aug 2025).
- **Educational data mining** — IEEE (2023) "Predicting Student Performance Using Educational Data Mining"; Nature Scientific Reports (Mar 2025) "Advancing educational data mining."
- **Embeddings** — Sentence Transformers (Hugging Face org page; AWS ML blog on fine-tuning, Oct 2024).

### Datasets
- **UCI Student Performance** — archive.ics.uci.edu/dataset/320 (CC BY 4.0; 649 students, 30 features; Portuguese schools; Cortez & Silva 2008).
- **ASSISTments** — assistments.org (research-use; US middle-school math tutor logs; gold standard for knowledge tracing).
- **KDD Cup 2010 EDM Challenge** — PSLC DataShop (19M+ transactions).
- **GSM8K / MATH / MathVista / DROP / BBH** — benchmark datasets (via Hugging Face / OpenAI; MIT/custom licenses).
- **K12 Mathematics Standards Aligned** — Hugging Face (robworks-software), Apache 2.0.
- **UDISE+ open data** — India Data Portal / AIKOSH (indiaai.gov.in) mirror; school-level aggregates only.

### Evidence Labels
- **Verified fact**: directly confirmed by official/primary source above.
- **Strong inference**: well-supported combination of primary sources (e.g., "concept-level diagnostics absent in existing systems" — inferred from official feature lists of DIKSHA/Saral/UDISE+).
- **Assumption (flagged)**: SIH evaluation weights and specific Smart Education problem statements for future cycles; "judge rejection" risks are analysis, not official criteria.

---

*Prepared: August 2026. All external claims carry source links in the section above. Where official/current SIH specifics were unavailable, this is explicitly flagged rather than invented.*
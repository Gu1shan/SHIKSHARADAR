# SHIKSHA RADAR — AI Build Prompts

## How to Use

1. Feed the **Preamble** + one module's prompt to the AI in a single message.
2. Approve modules one at a time, in dependency order (M1 → M2 → …).
3. Before approving the next module, run that module's `VERIFY` step and confirm it passes.
4. Never let the AI skip a `VERIFY` step or exceed the module's scope.

---

## PREAMBLE (feed with every prompt)

```
You are building "Shiksha Radar", a teacher-facing learning-gap detection platform for
Indian schools (Smart India Hackathon project). Full spec: shiksha-radar-plan.md.
Module breakdown + dependency graph: MODULES.md and MODULES_DIAGRAM.md.

Stack: Python 3.11+, Pandas, Streamlit, SQLite, plotly, sentence-transformers
(MiniLM-L6-v2), scikit-learn, pytest.

Non-negotiable conventions:
- Deterministic & auditable core (rules + statistics). LLM only for teacher-facing
  explanation. Never use labels like "weak", "poor", "failing", "at risk".
- Privacy-first: pseudonymized IDs only (Student_001). No PII anywhere.
- Beginner-readable code, no unnecessary abstractions, no comments unless asked.
- Match the repository structure in shiksha-radar-plan.md §22.
- Every module ends with its VERIFY step passing and exactly the given commit message.
```

---

## MODULE 1 — Synthetic Data Generator (subdivided into M1.0–M1.4)

### M1.0 — Schemas & folder scaffold

```
TASK (M1.0): Create the data folder structure and CSV schema specs.
CONTEXT: data/synthetic will hold 4 CSVs; data/schemas holds JSON validation schemas.
FILES:
  - data/synthetic/          (dir, keep a .gitkeep)
  - data/schemas/assessment_schema.json
  - data/schemas/question_schema.json
SPEC — exact CSV columns (document in the JSON schemas):
  students.csv:      student_id, grade, section
  questions.csv:     question_id, text, concept, sub_concept, difficulty, expected_answer
  responses.csv:     response_id, student_id, assessment_id, question_id,
                     student_answer, is_correct, error_type, created_at
  concept_map.csv:   question_id, concept, sub_concept
VERIFY: schemas are valid JSON and list exactly these columns with types.
COMMIT: "chore: data schemas and folder scaffold"
```

### M1.1 — Concept hierarchy + question bank

```
TASK (M1.1): Build the NCERT Class 5 Mathematics concept hierarchy and question bank.
CONTEXT: §14.2 — NCERT Class 3–8 focus, use Class 5.
SPEC:
  - Concepts: Fractions, Decimals, Algebra, Geometry, Measurement, Data Handling.
  - Sub-concepts: Fractions(denominator_handling, simplification, addition,
    subtraction, multiplication, comparison); Decimals(place_value, addition,
    comparison); Algebra(patterns, variables, equations, sign_rules);
    Geometry(2d_shapes, 3d_shapes, area_perimeter, angles, symmetry);
    Measurement(units, conversion); Data_Handling(reading_tables, averages).
  - ~3 questions per difficulty (easy/medium/hard) per sub-concept → ~150 questions.
  - expected_answer must be a numeric string or canonical text; keep it simple.
  - question_id format: Q{concept}_{sub_concept}_{n}.
  - Write to data/synthetic/questions.csv and data/synthetic/concept_map.csv.
VERIFY: every sub-concept has 9 questions; every row maps to a valid concept/sub_concept.
COMMIT: "feat: NCERT Class 5 question bank"
```

### M1.2 — Student roster + archetype engine

```
TASK (M1.2): Generate 50 pseudonymized students with archetype-driven error profiles.
CONTEXT: §14.2 archetypes table. No PII. Deterministic seed.
SPEC:
  - app/data/synthetic.py: function assign_archetypes(n_students=50, seed=42).
  - Archetypes (each ~8 students, Student_F 10):
      A Fractions struggler   → high error prob ONLY in Fractions (denominator-dominant)
      B Algebra struggler     → high error prob in Algebra (sign_errors, formula_selection)
      C Random mistakes       → moderate error prob across ALL concepts, no pattern
      D Improving over time   → error prob decays across the 6 assessments
      E Persistent struggles  → high error prob across all concepts, stable
      F On track              → low error prob everywhere
  - Student ID: Student_001 … Student_050. Grade 5. Section A/B split.
  - Output: data/synthetic/students.csv
VERIFY: 50 rows, unique IDs, expected count per archetype.
COMMIT: "feat: student roster with 6 archetypes"
```

### M1.3 — Assessments, responses & answer distortion

```
TASK (M1.3): Generate 6 assessments × 20 questions per student with realistic errors.
CONTEXT: §9.2 error taxonomy, §14.2 generation plan.
SPEC:
  - app/data/synthetic.py: function generate_responses(seed=42).
  - 6 assessments, dated Jul–Feb (academic year), ~monthly.
  - Per assessment: sample 20 questions stratified by concept (~3–4 per concept).
  - Per (student, question): use archetype error probability; if error:
      - pick error_type from the concept's error-pattern distribution
        (Fractions→denominator_handling/simplification/addition; Algebra→sign_error/
        formula_selection; Geometry→area_perimeter_confusion; else arithmetic/careless)
      - distort expected_answer to a plausible wrong answer
  - D archetype: error prob × decay factor per assessment index.
  - is_correct = 0 on error, else 1. error_type = "" when correct.
  - Output: data/synthetic/responses.csv (~6000 rows)
VERIFY: row count ≈ 50×6×20; each archetype's signature is visible in the data
        (A: fractions errors ≫ algebra; B: algebra errors ≫ fractions).
COMMIT: "feat: longitudinal response generator"
```

### M1.4 — CLI + end-to-end verification

```
TASK (M1.4): Wire it into a CLI and verify the whole pipeline.
FILES: scripts/generate_synthetic.py, app/data/synthetic.py
SPEC:
  - CLI: python scripts/generate_synthetic.py --students 50 --assessments 6 --seed 42
  - Prints: row counts per CSV, unique students, per-archetype error-rate summary,
    per-concept error counts.
  - Deterministic: same seed → byte-identical output.
VERIFY: run twice with seed 42 → identical checksums; all 4 CSVs validate against
        M1.0 schemas; no NaN in required columns.
COMMIT: "feat: synthetic data generator CLI (M1 complete)"
```

---

## MODULE 2 — Loader, Validator, Normalizer

```
TASK (M2): CSV loading + validation + answer normalization.
FILES: app/data/loader.py, app/data/validator.py, app/data/normalizer.py
SPEC: load 4 CSVs with schema checks (columns, types, required fields); validate
  student_id format, date ranges, score bounds, duplicate detection; normalize answers
  (lowercase, strip whitespace, unicode-NFKC). Handles §16.3 edge cases.
VERIFY: pytest cases for empty CSV, malformed rows, missing answers (→ "incomplete"),
  duplicate student_id, duplicate question_id, encoding.
COMMIT: "feat: data loading & validation pipeline"
```

## MODULE 3 — Rule-based Error Classifier

```
TASK (M3): Classify wrong answers into error types from §9.2 taxonomy.
FILES: app/analytics/classifier.py, app/analytics/taxonomy.py
SPEC: exact-match → correct; else keyword/regex per error type across the 5 categories
  (conceptual, procedural, calculation, careless, unknown). Deterministic, auditable.
VERIFY: ≥85% accuracy on 50 labeled answers (data/golden_set/answers_labeled.csv).
COMMIT: "feat: rule-based error classifier"
```

## MODULE 4 — Concept Mapper (rule → embedding)

```
TASK (M4): Map question → concept using rule lookup then embedding fallback.
FILES: app/analytics/concept_mapper.py, app/ai/embeddings.py
SPEC: exact question_id lookup first; else paraphrase-MiniLM-L6-v2 cosine similarity
  vs concept descriptions, accept ≥0.65; else flag "unmapped" for teacher review.
VERIFY: 100% on curated bank; ≥90% on 20 unseen questions.
COMMIT: "feat: concept mapping with embedding fallback"
```

## MODULE 5 — Profiling & Gap Detection

```
TASK (M5): Build ConceptProfile + LearningGap with Wilson confidence and trend.
FILES: app/analytics/profiler.py, app/analytics/confidence.py
SPEC: aggregate per student×concept: attempts, errors, error_breakdown (per error type),
  assessments_with_errors, first/last error date, trend (linear slope of error rate),
  confidence = min(0.95, Wilson_lower_bound × 1.2 × recency_weight). Gap if
  total_errors ≥ 3 AND assessments_with_errors ≥ 2 AND confidence ≥ 0.70.
VERIFY: archetypes A, B, D detected correctly; F produces no gaps.
COMMIT: "feat: concept profiling & gap detection"
```

## MODULE 6 — Streamlit Dashboard (4 views)

```
TASK (M6): Teacher dashboard with 4 pages (§12).
FILES: app/ui/pages/{1_Overview,2_Heatmap,3_Student_Profile,4_Class_Insights}.py,
  app/ui/components.py
SPEC: Overview KPIs + concept-difficulty bars; Student×Concept heatmap (🔴/🟡/🟢,
  clickable); Student profile with evidence count, error breakdown, trend, confidence,
  intervention button; Class insights with common gaps + trends. Every claim shows
  evidence + confidence.
VERIFY: streamlit run app.py renders all 4 pages on synthetic data.
COMMIT: "feat: Streamlit dashboard with 4 views"
```

## MODULE 7 — SQLite Persistence

```
TASK (M7): Persistent storage + multi-assessment accumulation (§13.2).
FILES: app/db/models.py, app/db/repository.py, app/db/migrations/
SPEC: tables students, assessments, questions, responses, concept_profiles,
  learning_gaps, interventions, intervention_outcomes; indexes per §13.2.
  Uploading a 2nd assessment accumulates profiles and updates gaps.
VERIFY: upload assessment_1 then assessment_2 → profiles grow, trends update, no dupes.
COMMIT: "feat: SQLite persistence layer"
```

## MODULE 8 — LLM Explanation Layer

```
TASK (M8): Evidence-cited, hallucination-guarded teacher explanations (§8).
FILES: app/ai/llm_client.py, app/ai/prompts.py
SPEC: send structured evidence JSON (no PII) with the §8.2 prompt template; temperature
  0.2–0.3; output validator blocks forbidden labels and missing evidence citations;
  fallback template explanation on timeout/failure.
VERIFY: 10 cases → no forbidden labels, evidence cited, confidence shown, fallback works.
COMMIT: "feat: LLM explanation layer with guardrails"
```

## MODULE 9 — Intervention Engine + PDF Export

```
TASK (M9): LearningGap → targeted intervention + printable worksheet (§11).
FILES: app/analytics/intervention.py, app/utils/export.py
SPEC: map gap → 3–4 steps (conceptual → procedural → practice → metacognitive) + 5
  practice questions (template or LLM) + reassessment plan; teacher must approve before
  "assigned"; export worksheet as PDF.
VERIFY: generated PDF has exactly 5 targeted questions + success criteria.
COMMIT: "feat: intervention engine with PDF worksheets"
```

## MODULE 10 — Feedback Loop Closure

```
TASK (M10): Reassessment → pre/post comparison → outcome (§11.3).
FILES: app/analytics/intervention.py (outcome logic)
SPEC: close_loop() computes pre/post error rates, proportion z-test, outcome:
  improved (post_rate < 0.20 AND p < 0.05), worsened (post ≥ pre), persisted (else).
  Stores {pre_rate, post_rate, p_value}.
VERIFY: unit tests for improved/persisted/worsened paths.
COMMIT: "feat: intervention feedback loop"
```

## MODULE 11 — Testing & Golden Set

```
TASK (M11): Build golden set + eval scripts + CI (§16, §22).
FILES: data/golden_set/*.csv, scripts/evaluate_golden_set.py,
  tests/{unit,integration,ai_eval}/, .github/workflows/ci.yml
SPEC: 50 labeled questions, 100 labeled answers, 50 gap labels; eval scripts for
  concept-mapping accuracy, error-classification precision, confidence Brier score.
VERIFY: pytest green; §16.2 targets met; CI passes.
COMMIT: "test: golden set evaluation and CI"
```

## MODULE 12 — Deployment & Docs

```
TASK (M12): Streamlit Cloud deploy + docs (§17, §22 docs/).
FILES: .streamlit/secrets.toml.example, .github/workflows/deploy.yml, README.md,
  docs/{architecture,deployment,privacy,sih_submission,demo_script}.md
SPEC: pin requirements; secrets never committed; README with quickstart; demo script.
VERIFY: public URL loads; no keys in repo.
COMMIT: "chore: deployment config and docs"
```

## MODULE 13 — Enhancements (optional)

```
TASK (M13): Hindi UI toggle, class-level PDF report, embedding fallback (§20, §12.4).
FILES: app/utils/i18n.py, app/utils/export.py, app/analytics/concept_mapper.py
SPEC: en/hi locale JSON + session-state toggle; class gap report PDF; embedding fallback
  path live in mapper.
VERIFY: Hindi toggle renders; class report downloads; 20 unseen questions mapped.
COMMIT: "feat: i18n, class report, embedding fallback"
```
# SHIKSHA RADAR — Module Breakdown

**Each module is a 2–4 hour work block, independently buildable and verifiable, ending in a passing check + commit.**

## Module Dependencies

```
M0 Scaffolding
  └─► M1 Data Gen ──► M2 Loader ──┬─► M3 Classifier ─┐
                                   └─► M4 ConceptMap ─┤
                                                       ▼
M1 ───────────────────────────────────────────► M5 Profile/Gap ──► M6 Dashboard
                                                                   │
                                                                   ▼
                                                          M7 SQLite
                                                             │
                                                             ▼
                                                     M8 LLM Layer
                                                             │
                                                             ▼
                                                     M9 Intervention
                                                             │
                                                             ▼
                                                     M10 Feedback Loop
                                                             │
                                                             ▼
                                                     M11 Tests (grows with every module; CI)
                                                             │
                                                             ▼
                                                     M12 Deploy/Docs
                                                             │
                                                             ▼
                                                     M13 Enhancements
```

## The 13 Modules

| # | Module | Est. | Files | Depends on | Do → Verify → Commit |
|---|--------|------|-------|-----------|----------------------|
| **M0** | Project scaffolding | 2–3h | repo init, venv, `requirements.txt`, `app/config.py` | — | `pip install` clean; package imports; commit "chore: init repo" |
| **M1** | Synthetic data generator | 2–3h | `app/data/synthetic.py`, `scripts/generate_synthetic.py`, `data/synthetic/*.csv` | M0 | 50 students × 6 assessments × 20 Q = ~6,000 rows; 6 archetypes (§14.2); commit |
| **M2** | Loader + validator + normalizer | 2–3h | `app/data/{loader,validator,normalizer}.py`, `data/schemas/*.json` | M0, M1 | Edge cases pass (§16.3); commit |
| **M3** | Rule-based error classifier | 3–4h | `app/analytics/classifier.py` | M2 | ≥85% on 50 labeled answers; commit |
| **M4** | Concept mapper (rule → embedding) | 3–4h | `app/analytics/concept_mapper.py`, `app/ai/embeddings.py` | M2 | 100% curated bank, ≥90% unseen; commit |
| **M5** | Profiling + gap detection | 3–4h | `app/analytics/{profiler,confidence}.py` | M3, M4 | Wilson confidence + trend; archetypes detected; commit |
| **M6** | Streamlit dashboard (4 views) | 3–4h | `app/ui/pages/*.py`, `components.py` | M5 | 4 screens render; heatmap clickable; evidence+confidence shown; commit |
| **M7** | SQLite persistence | 3–4h | `app/db/{models,repository}.py`, migrations | M5 | 2nd upload accumulates; no dupes; commit |
| **M8** | LLM explanation layer | 3–4h | `app/ai/{llm_client,prompts}.py` | M7 | 10 cases: no forbidden labels, evidence cited, timeout fallback; commit |
| **M9** | Intervention engine + PDF | 3–4h | `app/analytics/intervention.py`, `app/utils/export.py` | M8 | Worksheet = 5 targeted Q + reassessment plan; commit |
| **M10** | Feedback loop closure | 2–3h | `app/analytics/intervention.py` (outcomes) | M9 | improved/persisted/worsened correct (§11.3); commit |
| **M11** | Testing + golden set | ongoing | `tests/{unit,integration,ai_eval}/`, `data/golden_set/`, `scripts/evaluate_golden_set.py` | all | §16.2 targets met; CI green |
| **M12** | Deployment + docs | 2–3h | `.streamlit/`, `.github/workflows/`, `docs/*`, README | M11 | Public URL; secrets hidden; demo <3 min; commit |
| **M13** | Enhancements (optional) | 2–4h | i18n, class PDF report, embedding fallback | M12 | Hindi toggle works; class report PDF |

## Milestones

- **M0–M6** = MVP (Weeks 1–4)
- **M7–M10** = SIH Prototype (Weeks 5–8)
- **M11–M12** = Weeks 9–10
- **M13** = Post-SIH

Each module equals one §26 Day-block, ends in a passing verification + commit, and is blocked only by its listed dependencies, so work can proceed in parallel where the dependency graph forks.

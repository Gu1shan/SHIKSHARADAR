# SHIKSHA RADAR — Project Modularity

## Dependency Graph

```mermaid
flowchart TB
    subgraph P1["PHASE 1 · MVP (Weeks 1–4)"]
        direction TB
        M0["M0 Scaffolding"] --> M1["M1 Synthetic Data Gen"]
        M1 --> M2["M2 Loader · Validator · Normalizer"]
        M2 --> M3["M3 Error Classifier"]
        M2 --> M4["M4 Concept Mapper"]
        M3 --> M5["M5 Profiling + Gap Detection"]
        M4 --> M5
        M1 -. feed data to .-> M5
        M5 --> M6["M6 Streamlit Dashboard"]
    end

    subgraph P2["PHASE 2 · SIH Prototype (Weeks 5–8)"]
        direction TB
        M7["M7 SQLite Persistence"] --> M8["M8 LLM Explanation Layer"]
        M8 --> M9["M9 Intervention Engine + PDF"]
        M9 --> M10["M10 Feedback Loop Closure"]
    end

    subgraph P3["PHASE 3 · Hardening (Weeks 9–10)"]
        direction TB
        M11["M11 Testing + Golden Set"] --> M12["M12 Deploy + Docs"]
    end

    M6 --> M7
    M10 --> M11

    M13["M13 Enhancements (optional)"]
    M12 --> M13

    classDef data fill:#e8f0fe,stroke:#4285f4
    classDef analytics fill:#e6f4ea,stroke:#34a853
    classDef ai fill:#fce8e6,stroke:#ea4335
    classDef db fill:#fef7e0,stroke:#f9ab00
    classDef ui fill:#f3e8fd,stroke:#a142f4
    classDef infra fill:#e0f7fa,stroke:#00acc1
    classDef phase fill:#fafafa,stroke:#bbb

    class M0 infra
    class M1,M2 data
    class M3,M4,M5,M9,M10 analytics
    class M8,M13 ai
    class M7 db
    class M6 ui
    class M11,M12 infra
    class P1,P2,P3 phase
```

## Rules of Modularity

1. **One module = one work block (2–4 h)** → one verifiable check → one commit.
2. **Dependency only**: a module may use only the modules it depends on (edge in graph) — nothing else.
3. **Fork = parallel**: `M3` and `M4` both branch from `M2` and can be built by different people in parallel.
4. **Phase boundary = milestone**: finish Phase 1 → you have a working MVP demo; Phase 2 → SIH-ready prototype; Phase 3 → deployable.
5. **M11 rides along**: tests are written *with* every module, not after.

## Quick Reference

| Module | What it does | Produces | Phase |
|--------|--------------|----------|-------|
| M0 | Repo, venv, config | runnable skeleton | 1 |
| M1 | NCERT-aligned fake student data | 4 CSVs, 6 archetypes | 1 |
| M2 | CSV import + validation + answer cleanup | clean DataFrames | 1 |
| M3 | Rule-based error type classification | error_type per answer | 1 |
| M4 | Question → concept mapping (rule + embedding) | concept per question | 1 |
| M5 | Wilson confidence, trends, learning gaps | ConceptProfile + LearningGap | 1 |
| M6 | 4-view teacher dashboard | interactive app | 1 |
| M7 | Persistent storage + multi-assessment | SQLite DB | 2 |
| M8 | Evidence-cited, hallucination-guarded explanations | teacher-friendly text | 2 |
| M9 | Targeted worksheets + PDF export | intervention PDF | 2 |
| M10 | Reassess → compare → improved/persisted | closed loop | 2 |
| M11 | Golden set + eval + CI | green test suite | 3 |
| M12 | Streamlit Cloud deploy + docs | public URL | 3 |
| M13 | i18n, class report, embedding fallback | extras | post-SIH |

## ASCII Fallback

```
P1 MVP ──────────────── P2 SIH Prototype ──────── P3 Hardening
M0 → M1 → M2 ┬→ M3 ─┐
             └→ M4 ─┤→ M5 → M6 → M7 → M8 → M9 → M10 → M11 → M12 → M13
                  (M3/M4 run in parallel)
```

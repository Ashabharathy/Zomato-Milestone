# Phase 3 Implementation Guide

This implementation covers **Phase 3: Rule-Based Candidate Retrieval** from `Docs/phase-wise-architecture.md`.

## What It Does

- Loads cleaned restaurant data from Phase 1.
- Loads standardized user preferences from Phase 2.
- Applies rule-based filtering:
  - location
  - budget tier
  - minimum rating
  - cuisine match
- Applies basic ranking pre-processing using weighted scoring.
- Selects Top-N candidates for LLM prompt context.
- Includes a relaxed fallback filter when strict filtering returns zero candidates.

## Phase-Wise Folders

- Source code: `src/phase3/`
- Execution script: `scripts/run_phase3.py`
- Output data: `phase3/data/`

## How To Run

1. Ensure Phase 1 and Phase 2 outputs exist:
   - `phase1/data/restaurants_query_ready.parquet`
   - `phase2/data/user_preferences.json`
2. Execute Phase 3:
   - `python scripts/run_phase3.py`

## Optional arguments

- `--restaurants-path` (default: `phase1/data/restaurants_query_ready.parquet`)
- `--preferences-path` (default: `phase2/data/user_preferences.json`)
- `--output-dir` (default: `phase3/data`)
- `--top-n` (default: `15`)

## Expected Outputs

Generated under `phase3/data/`:
- `shortlisted_candidates.csv`
- `shortlisted_candidates.json`
- `phase3_report.json`

# Phase 1 Implementation Guide

This implementation covers **Phase 1: Foundation and Data Setup** from `Docs/phase-wise-architecture.md`.

## What It Does

- Loads Zomato dataset from Hugging Face.
- Maps varying source fields to a canonical schema:
  - `restaurant_name`
  - `location`
  - `cuisine`
  - `estimated_cost`
  - `rating`
- Cleans and normalizes text and numeric values.
- Deduplicates restaurants by `(restaurant_name, location)`.
- Applies quality filters for completeness and valid ranges.
- Extracts query-ready features:
  - `cuisine_tokens`
  - `budget_tier`
  - `rating_bucket`
- Writes processed artifacts to `phase1/data`.

## Phase-Wise Folders

- Source code: `src/phase1/`
- Execution script: `scripts/run_phase1.py`
- Output data: `phase1/data/`

## How To Run

1. Install dependencies:
   - `pip install -r requirements.txt`
2. Execute pipeline:
   - `python scripts/run_phase1.py`

Optional arguments:
- `--dataset-id` (default: `ManikaSaini/zomato-restaurant-recommendation`)
- `--split` (default: `train`)
- `--output-dir` (default: `phase1/data`)
- `--min-completeness-ratio` (default: `0.6`)

## Expected Outputs

Generated under `phase1/data/`:
- `restaurants_query_ready.csv`
- `restaurants_query_ready.parquet`
- `schema_mapping.json`
- `phase1_report.json`

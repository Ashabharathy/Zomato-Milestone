# Phase 2 Implementation Guide

This implementation covers **Phase 2: User Preference Capture Layer** from `Docs/phase-wise-architecture.md`.

## What It Does

- Uses a **basic Web UI** as the primary source of user input.
- Current implementation supports input ingestion via:
  - CLI arguments, or
  - a JSON payload file
- Validates required fields:
  - `location` (required)
  - `budget` (required: `low`, `medium`, `high`)
  - `cuisine` (required: one or more)
  - `min_rating` (optional, defaults to `3.5`, valid range `0-5`)
  - `optional_preferences` (optional)
- Normalizes user intent into a standardized schema:
  - Location alias mapping (for example, `blr` -> `bangalore`)
  - Cuisine normalization and de-duplication
  - Lowercase, whitespace-cleaned values
- Writes structured output for downstream phases.

## Phase-Wise Folders

- Source code: `src/phase2/`
- Execution script: `scripts/run_phase2.py`
- Output data: `phase2/data/`

## How To Run

The commands below are for the current backend validation pipeline.  
The Web UI layer will submit the same payload structure to this Phase 2 module.

### Option A: CLI input

`python scripts/run_phase2.py --location "Delhi NCR" --budget medium --cuisine "North Indian, Chinese" --min-rating 4.0 --optional-preferences "family-friendly, quick service"`

### Option B: JSON input

1. Create input file (example):

```json
{
  "location": "blr",
  "budget": "high",
  "cuisine": ["Italian", "Pan Asian"],
  "min_rating": 4.2,
  "optional_preferences": ["rooftop", "romantic"]
}
```

2. Run:

`python scripts/run_phase2.py --input-json phase2/input/preferences.json`

## Optional arguments

- `--output-dir` (default: `phase2/data`)

## Expected Outputs

Generated under `phase2/data/`:
- `user_preferences.json` (standardized preference object)
- `phase2_report.json` (status + output metadata)

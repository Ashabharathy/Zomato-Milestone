# Edge Cases: AI-Powered Restaurant Recommendation System

This document lists detailed edge cases for the project defined in:
- `Docs/problemstatement.md`
- `Docs/phase-wise-architecture.md`

It is organized phase-wise to align directly with the system architecture.

## Phase 1: Foundation and Data Setup

### 1) Dataset source unavailable
- **Scenario:** Hugging Face dataset URL is down, moved, or rate-limited.
- **Risk:** Data pipeline fails at startup.
- **Expected Handling:** Fail gracefully with actionable error message and retry policy.
- **Mitigation:** Add retries with backoff, optional local cache fallback, and startup health checks.

### 2) Schema drift in dataset
- **Scenario:** Column names or formats change (for example, `cost_for_two` renamed).
- **Risk:** Parsing and feature extraction break silently or produce wrong fields.
- **Expected Handling:** Schema validation should fail fast before loading into downstream steps.
- **Mitigation:** Maintain schema contract checks and versioned mapping logic.

### 3) Missing critical fields
- **Scenario:** `location`, `cuisine`, or `rating` is null for many rows.
- **Risk:** Weak filtering, poor recommendations, or empty outputs.
- **Expected Handling:** Impute or drop rows based on configurable thresholds.
- **Mitigation:** Data quality rules (minimum completeness) and quality report after ingestion.

### 4) Duplicate restaurants with inconsistent values
- **Scenario:** Same restaurant appears multiple times with different ratings/costs.
- **Risk:** Duplicate recommendations and ranking bias.
- **Expected Handling:** Deduplicate using stable keys and conflict resolution strategy.
- **Mitigation:** Canonicalization pipeline (name normalization + location-based merge).

### 5) Non-standard text formats
- **Scenario:** Cuisine values like `North Indian,Chinese` or mixed casing/spacing.
- **Risk:** Filter misses valid matches.
- **Expected Handling:** Normalize strings consistently before indexing/filtering.
- **Mitigation:** Tokenization, casing cleanup, delimiter normalization, synonym maps.

### 6) Outlier or invalid numeric values
- **Scenario:** Ratings above max range, negative costs, or text in numeric fields.
- **Risk:** Sorting and scoring errors.
- **Expected Handling:** Validate ranges and quarantine invalid rows.
- **Mitigation:** Type casting with strict validation and anomaly logging.

### 7) Large dataset memory pressure
- **Scenario:** Dataset grows and in-memory operations become slow.
- **Risk:** Timeout and degraded response times.
- **Expected Handling:** Streaming/chunked preprocessing and indexed storage.
- **Mitigation:** Move to DB-backed queries and precomputed indexes.

## Phase 2: User Preference Capture Layer

### 1) Ambiguous location input
- **Scenario:** User enters `Delhi NCR`, `blr`, or misspelled city names.
- **Risk:** No match despite valid intent.
- **Expected Handling:** Suggest nearest supported location or ask confirmation.
- **Mitigation:** Fuzzy matching and city alias dictionary.

### 2) Budget not aligned with stored cost format
- **Scenario:** User chooses `medium`, but dataset stores absolute numeric cost.
- **Risk:** Incorrect filtering boundaries.
- **Expected Handling:** Convert budget tiers into dynamic numeric bands by city.
- **Mitigation:** Per-city budget mapping (percentiles) instead of hardcoded ranges.

### 3) Conflicting user constraints
- **Scenario:** Very low budget + very high rating + niche cuisine in small area.
- **Risk:** Zero candidates.
- **Expected Handling:** Return "no exact match" with relaxed alternatives.
- **Mitigation:** Progressive relaxation strategy (location radius -> rating -> cuisine strictness).

### 4) Missing optional preferences
- **Scenario:** User provides only location and cuisine.
- **Risk:** Overly broad candidate set.
- **Expected Handling:** Use sensible defaults (for example, minimum rating baseline).
- **Mitigation:** Default policy plus transparent explanation of assumptions.

### 5) Free-form unsafe text
- **Scenario:** Input contains prompt-injection or script-like content in preferences.
- **Risk:** LLM prompt contamination or security issue.
- **Expected Handling:** Sanitize text and isolate user text from instruction blocks.
- **Mitigation:** Input sanitization, escaping, and strict prompt templating.

### 6) Unsupported cuisine vocabulary
- **Scenario:** User asks for `pan-asian vegan fusion`, not present in taxonomy.
- **Risk:** Zero matches due to strict literal filtering.
- **Expected Handling:** Map to nearest known cuisines and show interpreted filters.
- **Mitigation:** Cuisine ontology and synonym mapping.

## Phase 3: Rule-Based Candidate Retrieval

### 1) No candidates after strict filtering
- **Scenario:** Filter pipeline returns empty list.
- **Risk:** LLM has no context to recommend from.
- **Expected Handling:** Trigger fallback retrieval with relaxed constraints.
- **Mitigation:** Multi-pass retrieval strategy with traceable relaxation steps.

### 2) Too many candidates for prompt context
- **Scenario:** Thousands of rows match broad preferences.
- **Risk:** Prompt exceeds token limit; slower and more expensive inference.
- **Expected Handling:** Pre-rank and send only top-N diverse candidates.
- **Mitigation:** Deterministic shortlist policy (quality + diversity + proximity).

### 3) Bias toward popular restaurants only
- **Scenario:** Simple sort by rating overexposes mainstream options.
- **Risk:** Low novelty and repeated suggestions.
- **Expected Handling:** Balanced ranking with diversity constraints.
- **Mitigation:** Add exploration factor (cuisine variety, price spread, locality spread).

### 4) Sorting instability with ties
- **Scenario:** Many restaurants have same rating/cost.
- **Risk:** Non-deterministic recommendations across identical queries.
- **Expected Handling:** Apply stable tie-breakers.
- **Mitigation:** Deterministic ordering keys (rating, reviews count, normalized name).

### 5) Stale preprocessed data
- **Scenario:** Updated dataset not reflected in candidate index.
- **Risk:** Serving outdated recommendations.
- **Expected Handling:** Version checks between data store and retrieval layer.
- **Mitigation:** Data versioning and refresh triggers.

## Phase 4: LLM Recommendation and Reasoning Layer

### 1) Prompt overflow
- **Scenario:** Candidate metadata plus instructions exceed context window.
- **Risk:** Truncated or failed response.
- **Expected Handling:** Prompt compaction and candidate count reduction.
- **Mitigation:** Token budget manager before model invocation.

### 2) Hallucinated restaurant details
- **Scenario:** LLM invents cuisines, ratings, or services not in input data.
- **Risk:** Trust and accuracy issues.
- **Expected Handling:** Constrain output to provided fields only and validate post-response.
- **Mitigation:** Structured output schema + response verifier.

### 3) Non-parseable model output
- **Scenario:** LLM returns prose when JSON is expected.
- **Risk:** Downstream formatter breaks.
- **Expected Handling:** Retry with correction prompt or fallback formatter.
- **Mitigation:** Schema-first prompting and parser with repair logic.

### 4) Prompt injection from data fields
- **Scenario:** A restaurant name or user text contains malicious prompt instructions.
- **Risk:** Model ignores system instructions.
- **Expected Handling:** Treat data as plain text, never as executable instructions.
- **Mitigation:** Escape data blocks and strict role separation in prompts.

### 5) Model latency spikes/timeouts
- **Scenario:** External LLM API delays under load.
- **Risk:** Poor user experience.
- **Expected Handling:** Timeout + graceful fallback to rule-based ranking.
- **Mitigation:** Circuit breaker, retries, and cached recommendations for common queries.

### 6) Inconsistent ranking logic
- **Scenario:** Same input produces different top results frequently.
- **Risk:** Perceived instability.
- **Expected Handling:** Keep deterministic pre-ranking and controlled prompt randomness.
- **Mitigation:** Low temperature, fixed prompt template, and optional output caching.

## Phase 5: Response Assembly and Presentation

### 1) Missing fields in final response
- **Scenario:** One or more records lack cost/rating in output payload.
- **Risk:** UI rendering issues or broken cards.
- **Expected Handling:** Fill with explicit `Not available` placeholders.
- **Mitigation:** Response schema enforcement at formatter layer.

### 2) Contradictory explanation
- **Scenario:** Explanation says "budget-friendly" while cost is high.
- **Risk:** User distrust.
- **Expected Handling:** Consistency check between structured values and text explanation.
- **Mitigation:** Post-generation rule checks and explanation rewrite pass.

### 3) Overly verbose recommendations
- **Scenario:** Model generates long explanations for each option.
- **Risk:** Poor readability on mobile/web.
- **Expected Handling:** Enforce concise explanation length limits.
- **Mitigation:** Max token and sentence constraints in response template.

### 4) Unsafe or inappropriate output text
- **Scenario:** LLM response includes harmful or irrelevant language.
- **Risk:** Policy and user-safety violation.
- **Expected Handling:** Safety filter before display.
- **Mitigation:** Moderation API or regex/policy filters in presentation layer.

### 5) UI/API contract mismatch
- **Scenario:** Backend changes field names without frontend update.
- **Risk:** Runtime rendering failures.
- **Expected Handling:** Versioned API contracts with contract tests.
- **Mitigation:** Shared schema definitions and integration tests.

## Phase 6: Feedback, Evaluation, and Improvement Loop

### 1) Low feedback volume
- **Scenario:** Few users rate recommendations.
- **Risk:** Weak signal for model improvement.
- **Expected Handling:** Collect implicit feedback (clicks, dwell time, selections).
- **Mitigation:** Hybrid feedback strategy (explicit + implicit).

### 2) Feedback bias
- **Scenario:** Only extreme positive/negative users provide feedback.
- **Risk:** Skewed optimization.
- **Expected Handling:** Use debiasing in evaluation and weighting.
- **Mitigation:** Segment metrics by cohort and sample balancing.

### 3) Metric gaming
- **Scenario:** Optimizing for click-through hurts long-term satisfaction.
- **Risk:** Short-term gains, long-term quality drop.
- **Expected Handling:** Track multi-objective metrics.
- **Mitigation:** Use composite KPI (relevance, satisfaction, repeat usage, latency).

### 4) Prompt experiment regressions
- **Scenario:** New prompt improves one segment but harms others.
- **Risk:** Silent quality degradation.
- **Expected Handling:** Controlled rollout with rollback criteria.
- **Mitigation:** A/B testing guardrails and canary release process.

### 5) Monitoring blind spots
- **Scenario:** Failures occur without alerts (parse errors, empty recommendation rates).
- **Risk:** Production incidents persist unnoticed.
- **Expected Handling:** Alerting for quality and operational thresholds.
- **Mitigation:** Dashboards for no-result rate, timeout rate, hallucination checks, and latency.

## Cross-Cutting Edge Cases

### 1) Cold start users
- **Issue:** No historical preferences.
- **Handling:** Use stated preferences + popular diverse defaults by location.

### 2) Multi-language or mixed-language input
- **Issue:** User enters Hinglish or mixed scripts.
- **Handling:** Language normalization/translation before filtering and prompting.

### 3) Fairness and representation
- **Issue:** Recommendations consistently favor premium/locality-biased options.
- **Handling:** Add fairness constraints (price diversity, locality diversity).

### 4) Privacy and logging safety
- **Issue:** User-provided text may include personal data.
- **Handling:** Mask PII in logs and store only required fields.

### 5) Cost control under scale
- **Issue:** LLM costs increase with traffic and large prompts.
- **Handling:** Cache repeated queries, optimize prompt length, and use fallback models.

## Minimum Edge-Case Test Checklist

- Validate behavior when filtered candidates are `0`, `1`, and `>N`.
- Verify schema drift detection fails fast during ingestion.
- Confirm LLM output parser handles malformed responses.
- Ensure fallback path works when LLM API times out.
- Verify deterministic tie-breaking for repeated identical queries.
- Confirm explanations never reference fields absent in source data.
- Test safe handling of prompt-injection-like user input.
- Check UI output contracts for missing fields and null values.

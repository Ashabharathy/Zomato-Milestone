from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pandas as pd


@dataclass
class Phase3Config:
    restaurants_path: Path = Path("phase1/data/restaurants_query_ready.parquet")
    preferences_path: Path = Path("phase2/data/user_preferences.json")
    output_dir: Path = Path("phase3/data")
    top_n: int = 15


class Phase3Pipeline:
    def __init__(self, config: Phase3Config) -> None:
        self.config = config
        self.config.output_dir.mkdir(parents=True, exist_ok=True)

    def run(self) -> dict[str, Any]:
        restaurants = self._load_restaurants()
        preferences = self._load_preferences()

        strict = self._filter_candidates(restaurants, preferences, relaxed=False)
        relaxed_used = False
        if strict.empty:
            strict = self._filter_candidates(restaurants, preferences, relaxed=True)
            relaxed_used = True

        ranked = self._rank_candidates(strict, preferences)
        shortlisted = ranked.head(self.config.top_n).copy()
        output_files = self._persist(shortlisted)

        report = {
            "status": "ok",
            "input_rows": int(len(restaurants)),
            "candidate_rows": int(len(strict)),
            "shortlisted_rows": int(len(shortlisted)),
            "relaxed_filter_used": relaxed_used,
            "output_files": output_files,
        }
        self._write_json(self.config.output_dir / "phase3_report.json", report)
        return report

    def _load_restaurants(self) -> pd.DataFrame:
        path = self.config.restaurants_path
        if not path.exists():
            raise FileNotFoundError(f"Restaurants dataset not found: {path}")

        if path.suffix.lower() == ".parquet":
            data = pd.read_parquet(path)
        elif path.suffix.lower() == ".csv":
            data = pd.read_csv(path)
        else:
            raise ValueError("Unsupported restaurants file type. Use .parquet or .csv.")

        if data.empty:
            raise ValueError("Phase 1 dataset is empty. Run/fix Phase 1 before Phase 3.")
        return data

    def _load_preferences(self) -> dict[str, Any]:
        path = self.config.preferences_path
        if not path.exists():
            raise FileNotFoundError(f"Preference file not found: {path}")
        return json.loads(path.read_text(encoding="utf-8"))

    def _filter_candidates(
        self,
        restaurants: pd.DataFrame,
        preferences: dict[str, Any],
        relaxed: bool,
    ) -> pd.DataFrame:
        frame = restaurants.copy()

        location = str(preferences.get("location", "")).strip().lower()
        budget = str(preferences.get("budget", "")).strip().lower()
        min_rating = float(preferences.get("min_rating", 0))
        cuisines = [str(x).strip().lower() for x in preferences.get("cuisines", [])]

        if location:
            frame = frame[frame["location"].fillna("").str.lower() == location]

        if budget and "budget_tier" in frame.columns:
            frame = frame[frame["budget_tier"].fillna("").str.lower() == budget]

        rating_threshold = max(min_rating - 0.5, 0.0) if relaxed else min_rating
        frame = frame[frame["rating"].fillna(-1) >= rating_threshold]

        if cuisines:
            cuisine_pattern = "|".join(cuisines)
            source_col = "cuisine_tokens" if "cuisine_tokens" in frame.columns else "cuisine"
            frame = frame[frame[source_col].fillna("").str.lower().str.contains(cuisine_pattern, regex=True)]

        return frame

    def _rank_candidates(self, candidates: pd.DataFrame, preferences: dict[str, Any]) -> pd.DataFrame:
        if candidates.empty:
            return candidates

        working = candidates.copy()
        min_rating = float(preferences.get("min_rating", 0))
        requested_cuisines = set(str(x).strip().lower() for x in preferences.get("cuisines", []))

        working["rating_score"] = working["rating"].fillna(0.0)
        working["budget_match_score"] = (working["budget_tier"].fillna("") == preferences.get("budget", "")).astype(int)

        def cuisine_match_score(value: Any) -> int:
            tokens = set(str(value).split(","))
            return 1 if tokens.intersection(requested_cuisines) else 0

        source_col = "cuisine_tokens" if "cuisine_tokens" in working.columns else "cuisine"
        working["cuisine_match_score"] = working[source_col].fillna("").apply(cuisine_match_score)
        working["rating_margin_score"] = (working["rating"].fillna(0.0) - min_rating).clip(lower=0)

        working["overall_score"] = (
            (working["rating_score"] * 2.0)
            + (working["cuisine_match_score"] * 2.0)
            + (working["budget_match_score"] * 1.0)
            + (working["rating_margin_score"] * 0.5)
        )

        return working.sort_values(
            by=["overall_score", "rating", "restaurant_name"],
            ascending=[False, False, True],
        )

    def _persist(self, shortlisted: pd.DataFrame) -> dict[str, str]:
        csv_path = self.config.output_dir / "shortlisted_candidates.csv"
        json_path = self.config.output_dir / "shortlisted_candidates.json"
        shortlisted.to_csv(csv_path, index=False)
        json_path.write_text(shortlisted.to_json(orient="records", indent=2), encoding="utf-8")
        return {"csv": str(csv_path), "json": str(json_path)}

    @staticmethod
    def _write_json(path: Path, payload: dict[str, Any]) -> None:
        path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run Phase 3 rule-based candidate retrieval pipeline.")
    parser.add_argument("--restaurants-path", default=str(Phase3Config.restaurants_path))
    parser.add_argument("--preferences-path", default=str(Phase3Config.preferences_path))
    parser.add_argument("--output-dir", default=str(Phase3Config.output_dir))
    parser.add_argument("--top-n", type=int, default=Phase3Config.top_n)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    config = Phase3Config(
        restaurants_path=Path(args.restaurants_path),
        preferences_path=Path(args.preferences_path),
        output_dir=Path(args.output_dir),
        top_n=args.top_n,
    )
    report = Phase3Pipeline(config).run()
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pandas as pd
from datasets import load_dataset


FIELD_ALIASES: dict[str, list[str]] = {
    "restaurant_name": ["restaurant_name", "name", "restaurant", "restaurantName", "title"],
    "location": ["location", "city", "locality", "area", "address"],
    "cuisine": ["cuisine", "cuisines", "food_type", "food", "category"],
    "estimated_cost": ["estimated_cost", "cost_for_two", "average_cost", "price", "cost"],
    "rating": ["rating", "aggregate_rating", "user_rating", "stars", "score"],
}


@dataclass
class Phase1Config:
    dataset_id: str = "ManikaSaini/zomato-restaurant-recommendation"
    split: str = "train"
    output_dir: Path = Path("phase1/data")
    min_completeness_ratio: float = 0.6
    dedupe_on: tuple[str, ...] = ("restaurant_name", "location")


class Phase1Pipeline:
    def __init__(self, config: Phase1Config) -> None:
        self.config = config
        self.config.output_dir.mkdir(parents=True, exist_ok=True)

    def run(self) -> dict[str, Any]:
        raw_df = self._load_dataset()
        canonical_df = self._map_to_canonical_schema(raw_df)
        cleaned_df = self._clean_and_normalize(canonical_df)
        quality_df = self._apply_quality_filters(cleaned_df)
        features_df = self._extract_features(quality_df)
        self._persist_outputs(features_df)
        return self._build_report(raw_df, cleaned_df, features_df)

    def _load_dataset(self) -> pd.DataFrame:
        dataset = load_dataset(self.config.dataset_id, split=self.config.split)
        df = dataset.to_pandas()
        if df.empty:
            raise ValueError("Loaded dataset is empty. Cannot continue with Phase 1 pipeline.")
        return df

    def _map_to_canonical_schema(self, df: pd.DataFrame) -> pd.DataFrame:
        mapped = pd.DataFrame()
        matched_columns: dict[str, str | None] = {}
        for canonical_name, aliases in FIELD_ALIASES.items():
            matched_col = next((candidate for candidate in aliases if candidate in df.columns), None)
            matched_columns[canonical_name] = matched_col
            mapped[canonical_name] = df[matched_col] if matched_col else pd.NA
        self._write_json(self.config.output_dir / "schema_mapping.json", matched_columns)
        return mapped

    def _clean_and_normalize(self, df: pd.DataFrame) -> pd.DataFrame:
        working = df.copy()
        for col in ["restaurant_name", "location", "cuisine"]:
            working[col] = (
                working[col]
                .astype(str)
                .str.replace(r"\s+", " ", regex=True)
                .str.strip()
                .str.lower()
            )
            working[col] = working[col].replace({"": pd.NA, "nan": pd.NA, "none": pd.NA})

        working["estimated_cost"] = working["estimated_cost"].apply(self._parse_cost)
        working["rating"] = working["rating"].apply(self._parse_rating)
        before_dedupe = len(working)
        working = working.drop_duplicates(subset=list(self.config.dedupe_on), keep="first")
        working.attrs["deduped_rows"] = before_dedupe - len(working)
        return working

    def _apply_quality_filters(self, df: pd.DataFrame) -> pd.DataFrame:
        required = ["restaurant_name", "location", "cuisine", "estimated_cost", "rating"]
        completeness = df[required].notna().sum(axis=1) / len(required)
        filtered = df[completeness >= self.config.min_completeness_ratio].copy()
        filtered = filtered[(filtered["estimated_cost"] >= 0) & (filtered["rating"].between(0, 5))]
        return filtered

    def _extract_features(self, df: pd.DataFrame) -> pd.DataFrame:
        features = df.copy()
        features["cuisine_tokens"] = features["cuisine"].fillna("").apply(self._tokenize_cuisines)
        features["budget_tier"] = features["estimated_cost"].apply(self._cost_to_tier)
        features["rating_bucket"] = pd.cut(
            features["rating"],
            bins=[0, 2.5, 3.5, 4.2, 5.0],
            labels=["low", "average", "good", "excellent"],
            include_lowest=True,
        )
        return features

    def _persist_outputs(self, df: pd.DataFrame) -> None:
        df.to_csv(self.config.output_dir / "restaurants_query_ready.csv", index=False)
        df.to_parquet(self.config.output_dir / "restaurants_query_ready.parquet", index=False)

    def _build_report(self, raw_df: pd.DataFrame, cleaned_df: pd.DataFrame, final_df: pd.DataFrame) -> dict[str, Any]:
        report = {
            "raw_rows": int(len(raw_df)),
            "rows_after_cleaning": int(len(cleaned_df)),
            "rows_query_ready": int(len(final_df)),
            "rows_removed_in_cleaning": int(len(raw_df) - len(cleaned_df)),
            "rows_removed_by_quality_filter": int(len(cleaned_df) - len(final_df)),
            "deduplicated_rows": int(cleaned_df.attrs.get("deduped_rows", 0)),
            "output_files": {
                "csv": str(self.config.output_dir / "restaurants_query_ready.csv"),
                "parquet": str(self.config.output_dir / "restaurants_query_ready.parquet"),
                "schema_mapping": str(self.config.output_dir / "schema_mapping.json"),
            },
        }
        self._write_json(self.config.output_dir / "phase1_report.json", report)
        return report

    @staticmethod
    def _tokenize_cuisines(cuisine_value: str) -> str:
        parts = re.split(r"[,/|]+", cuisine_value.lower())
        normalized = sorted({p.strip() for p in parts if p.strip()})
        return ",".join(normalized)

    @staticmethod
    def _cost_to_tier(value: float) -> str:
        if pd.isna(value):
            return "unknown"
        if value <= 500:
            return "low"
        if value <= 1500:
            return "medium"
        return "high"

    @staticmethod
    def _parse_cost(value: Any) -> float:
        if pd.isna(value):
            return float("nan")
        if isinstance(value, (int, float)):
            return float(value)
        digits = re.findall(r"\d+(?:\.\d+)?", str(value).replace(",", ""))
        return float(digits[0]) if digits else float("nan")

    @staticmethod
    def _parse_rating(value: Any) -> float:
        if pd.isna(value):
            return float("nan")
        if isinstance(value, (int, float)):
            return float(value)
        matches = re.findall(r"\d+(?:\.\d+)?", str(value))
        return float(matches[0]) if matches else float("nan")

    @staticmethod
    def _write_json(path: Path, payload: dict[str, Any]) -> None:
        path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run Phase 1 data setup pipeline.")
    parser.add_argument("--dataset-id", default=Phase1Config.dataset_id)
    parser.add_argument("--split", default=Phase1Config.split)
    parser.add_argument("--output-dir", default=str(Phase1Config.output_dir))
    parser.add_argument("--min-completeness-ratio", type=float, default=Phase1Config.min_completeness_ratio)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    config = Phase1Config(
        dataset_id=args.dataset_id,
        split=args.split,
        output_dir=Path(args.output_dir),
        min_completeness_ratio=args.min_completeness_ratio,
    )
    report = Phase1Pipeline(config).run()
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()

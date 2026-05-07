from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


ALLOWED_BUDGETS = {"low", "medium", "high"}

LOCATION_ALIASES = {
    "blr": "bangalore",
    "bengaluru": "bangalore",
    "delhi ncr": "delhi",
    "new delhi": "delhi",
    "bombay": "mumbai",
}

CUISINE_ALIASES = {
    "north indian": "north indian",
    "south indian": "south indian",
    "indo chinese": "chinese",
    "pan asian": "asian",
    "italian cuisine": "italian",
}


@dataclass
class Phase2Config:
    output_dir: Path = Path("phase2/data")


@dataclass
class StandardizedPreferences:
    location: str
    budget: str
    cuisines: list[str]
    min_rating: float
    optional_preferences: list[str]


class PreferenceValidationError(ValueError):
    """Raised when user preferences fail validation."""


class Phase2Pipeline:
    def __init__(self, config: Phase2Config) -> None:
        self.config = config
        self.config.output_dir.mkdir(parents=True, exist_ok=True)

    def run(self, payload: dict[str, Any]) -> dict[str, Any]:
        standardized = self._validate_and_map(payload)
        output_path = self.config.output_dir / "user_preferences.json"
        output_path.write_text(
            json.dumps(asdict(standardized), indent=2),
            encoding="utf-8",
        )
        response = {
            "status": "ok",
            "output_file": str(output_path),
            "standardized_preferences": asdict(standardized),
        }
        report_path = self.config.output_dir / "phase2_report.json"
        report_path.write_text(json.dumps(response, indent=2), encoding="utf-8")
        return response

    def _validate_and_map(self, payload: dict[str, Any]) -> StandardizedPreferences:
        location = self._normalize_location(payload.get("location"))
        budget = self._normalize_budget(payload.get("budget"))
        cuisines = self._normalize_cuisines(payload.get("cuisine"))
        min_rating = self._normalize_rating(payload.get("min_rating"))
        optional_preferences = self._normalize_optional_preferences(payload.get("optional_preferences"))
        return StandardizedPreferences(
            location=location,
            budget=budget,
            cuisines=cuisines,
            min_rating=min_rating,
            optional_preferences=optional_preferences,
        )

    def _normalize_location(self, value: Any) -> str:
        if value is None:
            raise PreferenceValidationError("`location` is required.")
        normalized = self._normalize_text(str(value))
        if not normalized:
            raise PreferenceValidationError("`location` cannot be empty.")
        return LOCATION_ALIASES.get(normalized, normalized)

    def _normalize_budget(self, value: Any) -> str:
        if value is None:
            raise PreferenceValidationError("`budget` is required. Use one of: low, medium, high.")
        normalized = self._normalize_text(str(value))
        if normalized not in ALLOWED_BUDGETS:
            raise PreferenceValidationError("Invalid `budget`. Allowed values: low, medium, high.")
        return normalized

    def _normalize_cuisines(self, value: Any) -> list[str]:
        if value is None:
            raise PreferenceValidationError("`cuisine` is required.")

        if isinstance(value, list):
            raw_items = [str(v) for v in value]
        else:
            raw_items = re.split(r"[,/|]+", str(value))

        normalized_items: list[str] = []
        for item in raw_items:
            normalized = self._normalize_text(item)
            if not normalized:
                continue
            normalized_items.append(CUISINE_ALIASES.get(normalized, normalized))

        unique_items = sorted(set(normalized_items))
        if not unique_items:
            raise PreferenceValidationError("`cuisine` must contain at least one valid value.")
        return unique_items

    def _normalize_rating(self, value: Any) -> float:
        if value is None or str(value).strip() == "":
            return 3.5
        try:
            rating = float(value)
        except (TypeError, ValueError) as exc:
            raise PreferenceValidationError("`min_rating` must be a numeric value between 0 and 5.") from exc
        if rating < 0 or rating > 5:
            raise PreferenceValidationError("`min_rating` must be between 0 and 5.")
        return round(rating, 1)

    def _normalize_optional_preferences(self, value: Any) -> list[str]:
        if value is None:
            return []
        if isinstance(value, list):
            raw_items = [str(v) for v in value]
        else:
            raw_items = re.split(r"[,/|]+", str(value))

        cleaned: list[str] = []
        for item in raw_items:
            normalized = self._normalize_text(item)
            if normalized:
                cleaned.append(normalized)
        return sorted(set(cleaned))

    @staticmethod
    def _normalize_text(value: str) -> str:
        return re.sub(r"\s+", " ", value).strip().lower()


def _load_payload_from_json(path: str) -> dict[str, Any]:
    payload_path = Path(path)
    if not payload_path.exists():
        raise FileNotFoundError(f"Input file not found: {payload_path}")
    return json.loads(payload_path.read_text(encoding="utf-8"))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run Phase 2 preference capture and validation pipeline.")
    parser.add_argument("--location", help="User location (e.g., Delhi, Bangalore)")
    parser.add_argument("--budget", help="Budget tier: low, medium, or high")
    parser.add_argument("--cuisine", help="Cuisine(s), comma-separated or single value")
    parser.add_argument("--min-rating", type=float, help="Minimum rating between 0 and 5")
    parser.add_argument(
        "--optional-preferences",
        default="",
        help="Optional preferences as comma-separated values",
    )
    parser.add_argument(
        "--input-json",
        help="Path to JSON payload. If provided, CLI args are ignored.",
    )
    parser.add_argument("--output-dir", default=str(Phase2Config.output_dir))
    return parser


def _build_payload_from_args(args: argparse.Namespace) -> dict[str, Any]:
    return {
        "location": args.location,
        "budget": args.budget,
        "cuisine": args.cuisine,
        "min_rating": args.min_rating,
        "optional_preferences": args.optional_preferences,
    }


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.input_json:
        payload = _load_payload_from_json(args.input_json)
    else:
        payload = _build_payload_from_args(args)

    pipeline = Phase2Pipeline(Phase2Config(output_dir=Path(args.output_dir)))
    result = pipeline.run(payload)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

"""Cosmic Nexus experimental core.

A small, self-contained research engine connecting the project's existing ideas:
observations, object data, events, scoring, and an explainable decision layer.

This is intentionally dependency-free so the repository can run it with plain
Python. It is a foundation for turning the old documentation-driven architecture
into executable systems.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime, timezone
import json
import math
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class CosmicObject:
    name: str
    kind: str
    distance_ly: float
    interest: float
    tags: tuple[str, ...] = ()


@dataclass(frozen=True)
class Observation:
    object_name: str
    signal_strength: float
    novelty: float
    timestamp: str


@dataclass(frozen=True)
class ResearchDecision:
    target: str
    priority: float
    reason: str


class CosmicEngine:
    """Coordinates a tiny executable Cosmic Nexus research loop."""

    def __init__(self) -> None:
        self.objects: dict[str, CosmicObject] = {}
        self.observations: list[Observation] = []

    def register(self, obj: CosmicObject) -> None:
        if obj.distance_ly < 0:
            raise ValueError("distance_ly cannot be negative")
        if not 0 <= obj.interest <= 1:
            raise ValueError("interest must be between 0 and 1")
        self.objects[obj.name.lower()] = obj

    def observe(self, object_name: str, signal_strength: float, novelty: float) -> Observation:
        key = object_name.lower()
        if key not in self.objects:
            raise KeyError(f"Unknown cosmic object: {object_name}")
        if not 0 <= signal_strength <= 1 or not 0 <= novelty <= 1:
            raise ValueError("signal_strength and novelty must be between 0 and 1")

        observation = Observation(
            object_name=self.objects[key].name,
            signal_strength=signal_strength,
            novelty=novelty,
            timestamp=datetime.now(timezone.utc).isoformat(),
        )
        self.observations.append(observation)
        return observation

    def prioritize(self) -> list[ResearchDecision]:
        """Rank observed targets with a transparent, explainable score."""
        latest: dict[str, Observation] = {}
        for observation in self.observations:
            latest[observation.object_name.lower()] = observation

        decisions: list[ResearchDecision] = []
        for key, observation in latest.items():
            obj = self.objects[key]
            distance_factor = 1 / (1 + math.log10(max(obj.distance_ly, 1)))
            priority = (
                0.40 * observation.novelty
                + 0.30 * observation.signal_strength
                + 0.20 * obj.interest
                + 0.10 * distance_factor
            )
            reason = (
                f"novelty={observation.novelty:.2f}, "
                f"signal={observation.signal_strength:.2f}, "
                f"interest={obj.interest:.2f}"
            )
            decisions.append(ResearchDecision(obj.name, round(priority, 4), reason))

        return sorted(decisions, key=lambda item: item.priority, reverse=True)

    def export_state(self, path: str | Path) -> None:
        payload = {
            "objects": [asdict(obj) for obj in self.objects.values()],
            "observations": [asdict(obs) for obs in self.observations],
            "priorities": [asdict(item) for item in self.prioritize()],
        }
        Path(path).write_text(json.dumps(payload, indent=2), encoding="utf-8")


def demo_objects() -> Iterable[CosmicObject]:
    yield CosmicObject("Sun", "star", 0.0000158, 0.35, ("solar-system", "star"))
    yield CosmicObject("Andromeda Galaxy", "galaxy", 2_537_000, 0.95, ("galaxy", "local-group"))
    yield CosmicObject("TON 618", "quasar", 18_200_000_000, 0.99, ("quasar", "black-hole"))
    yield CosmicObject("Fast Radio Burst", "transient", 1_000_000_000, 0.92, ("radio", "transient"))


def main() -> None:
    engine = CosmicEngine()
    for obj in demo_objects():
        engine.register(obj)

    engine.observe("Andromeda Galaxy", signal_strength=0.72, novelty=0.61)
    engine.observe("TON 618", signal_strength=0.88, novelty=0.93)
    engine.observe("Fast Radio Burst", signal_strength=0.67, novelty=0.97)

    print("=== COSMIC NEXUS RESEARCH ENGINE ===")
    for decision in engine.prioritize():
        print(f"{decision.priority:.4f} | {decision.target} | {decision.reason}")

    output = Path(__file__).with_name("cosmic_state.json")
    engine.export_state(output)
    print(f"State exported to: {output}")


if __name__ == "__main__":
    main()

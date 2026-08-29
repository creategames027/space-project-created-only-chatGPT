"""Observation Network — resurrected experimental system.

This is a dependency-free prototype that turns observations into a small,
queryable event stream. It is intentionally simple so it can later be connected
to the Cosmic Nexus engine and the portal.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime, timezone
import json
from pathlib import Path


@dataclass(frozen=True)
class ObservationEvent:
    target: str
    signal: float
    novelty: float
    timestamp: str


class ObservationNetwork:
    def __init__(self) -> None:
        self.events: list[ObservationEvent] = []

    def record(self, target: str, signal: float, novelty: float) -> ObservationEvent:
        if not target.strip():
            raise ValueError("target cannot be empty")
        if not 0 <= signal <= 1 or not 0 <= novelty <= 1:
            raise ValueError("signal and novelty must be between 0 and 1")

        event = ObservationEvent(
            target=target.strip(),
            signal=signal,
            novelty=novelty,
            timestamp=datetime.now(timezone.utc).isoformat(),
        )
        self.events.append(event)
        return event

    def interesting(self, threshold: float = 0.75) -> list[ObservationEvent]:
        """Return observations whose combined signal/novelty is noteworthy."""
        if not 0 <= threshold <= 1:
            raise ValueError("threshold must be between 0 and 1")
        return [
            event for event in self.events
            if (event.signal + event.novelty) / 2 >= threshold
        ]

    def save(self, path: str | Path) -> None:
        Path(path).write_text(
            json.dumps([asdict(event) for event in self.events], indent=2),
            encoding="utf-8",
        )


def main() -> None:
    network = ObservationNetwork()
    network.record("Andromeda Galaxy", 0.72, 0.61)
    network.record("TON 618", 0.88, 0.93)
    network.record("Fast Radio Burst", 0.67, 0.97)

    print("=== OBSERVATION NETWORK ===")
    for event in network.interesting():
        print(f"[INTERESTING] {event.target}: signal={event.signal:.2f}, novelty={event.novelty:.2f}")

    output = Path(__file__).with_name("observation_events.json")
    network.save(output)
    print(f"Saved {len(network.events)} observations to {output}")


if __name__ == "__main__":
    main()

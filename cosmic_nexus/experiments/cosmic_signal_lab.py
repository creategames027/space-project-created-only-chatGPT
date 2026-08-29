"""A tiny random cosmic-signal experiment for the Cosmic Nexus.

No external data is used: this is a deterministic playground for testing how
an observation could be classified before real telescope data is connected.
"""

from __future__ import annotations

from dataclasses import dataclass
import random


@dataclass(frozen=True)
class Signal:
    frequency_mhz: float
    strength: float
    repeat_count: int

    @property
    def score(self) -> float:
        repetition = min(self.repeat_count / 5, 1.0)
        return round(0.45 * self.strength + 0.35 * repetition + 0.20 * self.frequency_factor, 3)

    @property
    def frequency_factor(self) -> float:
        return 1.0 - min(abs(self.frequency_mhz - 1420.0) / 1420.0, 1.0)


def generate_signal(rng: random.Random) -> Signal:
    return Signal(
        frequency_mhz=round(rng.uniform(100, 3000), 2),
        strength=round(rng.random(), 3),
        repeat_count=rng.randint(0, 8),
    )


def classify(signal: Signal) -> str:
    if signal.score >= 0.72:
        return "HIGH_INTEREST"
    if signal.score >= 0.45:
        return "WATCH"
    return "BACKGROUND"


def run(seed: int = 42, samples: int = 12) -> list[Signal]:
    rng = random.Random(seed)
    signals = [generate_signal(rng) for _ in range(samples)]
    signals.sort(key=lambda item: item.score, reverse=True)

    print("=== COSMIC SIGNAL LAB ===")
    for index, signal in enumerate(signals, 1):
        print(
            f"#{index:02d} {classify(signal):12} "
            f"freq={signal.frequency_mhz:7.2f} MHz "
            f"strength={signal.strength:.3f} "
            f"repeat={signal.repeat_count} score={signal.score:.3f}"
        )
    return signals


if __name__ == "__main__":
    run()

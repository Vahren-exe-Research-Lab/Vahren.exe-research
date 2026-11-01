"""Bounded native CRT RNG subset (static evidence, not gameplay replay).

Vahren target uses MSVC LCG in T031. Seed timing is controlled explicitly by
callers: startup, scene resets, map-local window and map exit may all reseed.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import TypeVar, Sequence

T=TypeVar("T")

@dataclass(slots=True)
class LegacyRng:
    state: int
    last_reseed_reason: str = "explicit initial seed"
    draws_since_reseed: int = 0
    lifetime_draws: int = 0

    def __post_init__(self) -> None:
        self.state &= 0xFFFFFFFF

    def reseed(self, seed: int, *, reason: str) -> None:
        if not reason:
            raise ValueError("reason is mandatory to trace legacy reseeds")
        self.state = seed & 0xFFFFFFFF
        self.last_reseed_reason = reason
        self.draws_since_reseed = 0

    def rand15(self) -> int:
        self.state = (self.state * 0x343FD + 0x269EC3) & 0xFFFFFFFF
        self.draws_since_reseed += 1
        self.lifetime_draws += 1
        return (self.state >> 16) & 0x7FFF

    def random_below(self, upper: int) -> int:
        """Exact familiar 0..upper-1 conversion for positive bounded ranges."""
        if not (1 <= upper <= 32768):
            raise ValueError("validated range: upper must be 1..32768")
        draw = self.rand15()
        return (draw * upper) // 32768

    def random_between(self, lower: int, upper: int) -> int:
        """Native floor(rand/32768*(upper-lower))+lower for upper>lower."""
        width = upper - lower
        if not (1 <= width <= 32768):
            raise ValueError("only positive bounded native intervals are implemented")
        return lower + self.random_below(width)

    def shuffle_forward(self, items: Sequence[T]) -> list[T]:
        """T031 forward Fisher-Yates, one CRT draw per step for N<=32767.

        The native selection uses modulo (i+1), not random_below().
        We deliberately forbid the unverified large-vector extension here.
        """
        out = list(items)
        if len(out) > 32767:
            raise ValueError("native large-vector random extension not implemented")
        for i in range(1, len(out)):
            j = self.rand15() % (i + 1)
            out[i], out[j] = out[j], out[i]
        return out

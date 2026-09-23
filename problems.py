from dataclasses import dataclass

import numpy as np

DEFAULT_SEED = 42
DEFAULT_NUM_PROBLEMS = 10_000
DEFAULT_NUM_ITEMS = 100
DEFAULT_MAX_CAPACITY = 100
DEFAULT_MIN_ITEM = 1
DEFAULT_MAX_ITEM = 49


@dataclass(frozen=True)
class ProblemSet:
    # Both are int32 so they can be handed to a GPU buffer without a copy.
    items: np.ndarray  # shape (num_problems, num_items)
    capacities: np.ndarray  # shape (num_problems,)

    @property
    def num_problems(self) -> int:
        return int(self.items.shape[0])

    @property
    def num_items(self) -> int:
        return int(self.items.shape[1])

    @property
    def max_capacity(self) -> int:
        """Widest capacity in the set, needed for a DP table to know its max capacity."""
        return int(self.capacities.max())


def generate(
    num_problems: int = DEFAULT_NUM_PROBLEMS,
    num_items: int = DEFAULT_NUM_ITEMS,
    max_capacity: int = DEFAULT_MAX_CAPACITY,
    min_item: int = DEFAULT_MIN_ITEM,
    max_item: int = DEFAULT_MAX_ITEM,
    seed: int = DEFAULT_SEED,
) -> ProblemSet:
    if num_problems < 1:
        raise ValueError(f"num_problems must be at least 1, got {num_problems}")
    if num_items < 1:
        raise ValueError(f"num_items must be at least 1, got {num_items}")
    if min_item < 1:
        raise ValueError(f"min_item must be at least 1, got {min_item}")
    if max_item < min_item:
        raise ValueError(f"max_item {max_item} is below min_item {min_item}")
    if max_capacity < 1:
        raise ValueError(f"max_capacity must be at least 1, got {max_capacity}")

    rng = np.random.default_rng(seed)
    items = rng.integers(
        min_item, max_item + 1, size=(num_problems, num_items), dtype=np.int32
    )
    capacities = rng.integers(1, max_capacity + 1, size=num_problems, dtype=np.int32)
    return ProblemSet(items=items, capacities=capacities)

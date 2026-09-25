from dataclasses import dataclass

import numpy as np

DEFAULT_SEED = 42
DEFAULT_NUM_PROBLEMS = 10_000
DEFAULT_NUM_ITEMS = 16
DEFAULT_MAX_CAPACITY = 2000
DEFAULT_MIN_ITEM = 1
DEFAULT_MAX_ITEM = 999


# This is some pretty dense code, but it's just using an array of bits to
# track what total amounts are reachable by taking or not taking each item
def best_total(items: np.ndarray, capacity: int) -> int:
    reachable = 1 # First bit of reachable is the index for 0
    mask = (1 << (capacity + 1)) - 1 # Set a mask of all totals bits from 0 to capacity (for dropping overshoots)
    for item in items:
        # Set reachable total bits for all totals reachable via the current item
        reachable |= reachable << int(item)
        reachable &= mask # Drop any totals that have overshot the capacity
    return reachable.bit_length() - 1 # The highest bit still set is the largest reachable total


def _hits_capacity(items: np.ndarray, capacity: int) -> bool:
    return best_total(items, capacity) == capacity

# Some examples:
# items=[3, 5]  capacity=7
#         bit index: 7 6 5 4 3 2 1 0
#             start: 0 0 0 0 0 0 0 1   totals reachable: [0]
#          after +3: 0 0 0 0 1 0 0 1   totals reachable: [0, 3]
#          after +5: 0 0 1 0 1 0 0 1   totals reachable: [0, 3, 5]
#    bit 7 set? False
#
# items=[3, 5]  capacity=8
#         bit index: 8 7 6 5 4 3 2 1 0
#             start: 0 0 0 0 0 0 0 0 1   totals reachable: [0]
#          after +3: 0 0 0 0 0 1 0 0 1   totals reachable: [0, 3]
#          after +5: 1 0 0 1 0 1 0 0 1   totals reachable: [0, 3, 5, 8]
#    bit 8 set? True
#
# items=[2, 3, 4]  capacity=9
#         bit index: 9 8 7 6 5 4 3 2 1 0
#             start: 0 0 0 0 0 0 0 0 0 1   totals reachable: [0]
#          after +2: 0 0 0 0 0 0 0 1 0 1   totals reachable: [0, 2]
#          after +3: 0 0 0 0 1 0 1 1 0 1   totals reachable: [0, 2, 3, 5]
#          after +4: 1 0 1 1 1 1 1 1 0 1   totals reachable: [0, 2, 3, 4, 5, 6, 7, 9]
#    bit 9 set? True


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

    def analyze(self) -> float:
        """Print, and return, the proportion of problems that can hit their capacity exactly."""
        exact = sum(
            _hits_capacity(items, int(capacity))
            for items, capacity in zip(self.items, self.capacities)
        )
        proportion = exact / self.num_problems
        print(
            f"{exact}/{self.num_problems} problems ({proportion:.1%}) have a subset "
            f"that sums to the capacity exactly; the rest fall short of it"
        )
        return proportion


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

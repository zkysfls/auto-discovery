"""Deterministic 16-point construction for minimizing_max_min_dist in 2D."""

from __future__ import annotations

import numpy as np

N_POINTS = 16
DIMENSION = 2

# Numerically polished point set with diameter 1 and strong minimum spacing.
POINTS = np.array(
    [
        [0.16944442, -0.15974677],
        [0.19201328, 0.11789928],
        [-0.06414708, 0.22690450],
        [-0.23818858, 0.01372582],
        [-0.09888479, -0.22358460],
        [0.50386882, -0.02384037],
        [0.43452293, 0.25152498],
        [0.22426877, 0.44489890],
        [-0.05558168, 0.50220254],
        [-0.30855917, 0.39197690],
        [-0.46842426, 0.16673866],
        [-0.48936677, -0.10886628],
        [-0.34395954, -0.36180025],
        [-0.07293035, -0.49764696],
        [0.19992209, -0.45575135],
        [0.41600189, -0.28463499],
    ],
    dtype=np.float64,
)


def min_max_dist_dim2_16() -> np.ndarray:
    return POINTS.copy()


if __name__ == "__main__":
    print(min_max_dist_dim2_16())

import numpy as np
from Functions.FxDistanceMatrix import distanceMatrix


def test_distanceMatrix():
    Mx = np.array([0, 0, 0], dtype=np.float64)
    My = np.array([0, 0, 0], dtype=np.float64)
    Mz = np.array([0, 0, 0], dtype=np.float64)
    Md = distanceMatrix(Mx, My, Mz, 10)
    assert np.allclose(Md, np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]]))

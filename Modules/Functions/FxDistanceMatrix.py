import numpy as np
import numpy.typing as npt


def distanceMatrix(
    x: npt.NDArray[np.float64],
    y: npt.NDArray[np.float64],
    z: npt.NDArray[np.float64],
    size: float,
) -> npt.NDArray[np.float64]:
    def matrixModulo(
        distanceArray: npt.NDArray[np.float64], atomicSystemSize: float
    ) -> npt.NDArray[np.float64]:
        distanceArray = np.where(
            distanceArray > (atomicSystemSize / 2),
            atomicSystemSize - distanceArray,
            distanceArray,
        )
        return distanceArray

    def getDistanceArray(array: npt.NDArray[np.float64]) -> npt.NDArray[np.float64]:
        return abs(array[:, None] - array[None, :])

    # _, x, y, z = self._numpyArrays

    dx = getDistanceArray(x)
    dx = matrixModulo(dx, size)

    dy = getDistanceArray(y)
    dy = matrixModulo(dy, size)

    dz = getDistanceArray(z)
    dz = matrixModulo(dz, size)

    return (dx**2 + dy**2 + dz**2) ** (1 / 2)

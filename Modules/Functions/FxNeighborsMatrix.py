import globalConfigs
import numpy as np
import numpy.typing as npt


def neighborsMatrix(
    distanceMatrix: npt.NDArray[np.float64], isOneIndexed: bool = False
) -> npt.NDArray[np.float64]:
    neighborsMatrix = np.where(
        distanceMatrix < globalConfigs.cutOff, float(1), float(0)
    )
    neighborsMatrix[neighborsMatrix == 0] = ["NaN"]

    # Multiplying each col by its index, thus transforming 1 -> index
    neighborsMatrix[:] *= range(len(distanceMatrix[0]))

    if isOneIndexed is True:
        neighborsMatrix[:] += 1

    return neighborsMatrix

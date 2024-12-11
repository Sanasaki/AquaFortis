import globalConfigs
import numpy as np
import numpy.typing as npt
from Chemistry.Atom import Atom


def neighborsPerAtom(
    distanceMatrix: npt.NDArray[np.float64], atoms: list["Atom"]
) -> dict[Atom, list[Atom]]:
    def getNeighbors(
        distanceMatrix: npt.NDArray[np.float64], isOneIndexed: bool = False
    ) -> npt.NDArray[np.int64]:
        neighborsMatrix = np.where(distanceMatrix < globalConfigs.cutOff, 1, np.nan)

        # Multiplying each col by its index, thus transforming 1 -> index
        neighborsMatrix[:] *= range(len(distanceMatrix[0]))

        if isOneIndexed is True:
            neighborsMatrix[:] += 1

        return neighborsMatrix

    neighborsMatrix = getNeighbors(distanceMatrix)
    atomToNeighborsMap: dict[Atom, list[Atom]] = {}

    for atomIndex, atom in enumerate(atoms):
        neighborIndexes: list[int] = (
            (neighborsMatrix[atomIndex, :])[~np.isnan(neighborsMatrix[atomIndex, :])]
        ).tolist()

        for neighborIndex in neighborIndexes:
            neighbor = atoms[int(neighborIndex)]
            atomToNeighborsMap[atom] = atomToNeighborsMap.get(atom, []) + [neighbor]

    return atomToNeighborsMap

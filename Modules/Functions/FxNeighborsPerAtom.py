import numpy as np
import numpy.typing as npt
from Chemistry.Atom import Atom


def neighborsPerAtom(
    neighborsMatrix: npt.NDArray[np.float64], atoms: list["Atom"]
) -> dict[Atom, list[Atom]]:
    # Zip function is very slow, so it should be replaced with a dict update here
    # neighbors = {}
    # this atom neighbor = {i : self.atoms[int(j)]}
    # neighbors.update(this atom neighbor)
    neighbors: list[list[Atom]] = []

    for i in range(len(neighborsMatrix)):
        listOfIndex = (
            (neighborsMatrix[i, :])[~np.isnan(neighborsMatrix[i, :])]
        ).tolist()
        iNeighbors: list[Atom] = []
        for j in listOfIndex:
            iNeighbors.append(atoms[int(j)])
        neighbors.append(iNeighbors)

    return {atom: neighbors for atom, neighbors in zip(atoms, neighbors)}

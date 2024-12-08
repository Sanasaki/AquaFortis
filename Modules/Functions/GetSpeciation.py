import numpy as np
import numpy.typing as npt
from Classes.AtomicSystem import AtomicSystem


def distanceMatrix(self) -> npt.NDArray[np.float64]:
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

    _, x, y, z = self._numpyArrays

    dx = getDistanceArray(x)
    dx = matrixModulo(dx, self.size)

    dy = getDistanceArray(y)
    dy = matrixModulo(dy, self.size)

    dz = getDistanceArray(z)
    dz = matrixModulo(dz, self.size)

    return (dx**2 + dy**2 + dz**2) ** (1 / 2)


def neighborsMatrix(self, isOneIndexed: bool = False) -> npt.NDArray[np.float64]:
    neighborsMatrix = np.where(
        self.distanceMatrix < AtomicSystem.cutoffRadii, float(1), float(0)
    )
    neighborsMatrix[neighborsMatrix == 0] = ["NaN"]
    # Multiplying each col by its index, thus transforming 1 -> index
    neighborsMatrix[:] *= range(len(self.distanceMatrix[0]))
    if isOneIndexed is True:
        neighborsMatrix[:] += 1

    return neighborsMatrix


def neighborsPerAtom(self) -> dict[Atom, list[Atom]]:
    # Zip function is very slow, so it should be replaced with a dict update here
    # neighbors = {}
    # this atom neighbor = {i : self.atoms[int(j)]}
    # neighbors.update(this atom neighbor)
    neighbors: list[list[Atom]] = []

    for i in range(len(self.neighborsMatrix)):
        listOfIndex = (
            (self.neighborsMatrix[i, :])[~np.isnan(self.neighborsMatrix[i, :])]
        ).tolist()
        iNeighbors: list[Atom] = []
        for j in listOfIndex:
            iNeighbors.append(self.atoms[int(j)])
        neighbors.append(iNeighbors)

    return {atom: neighbors for atom, neighbors in zip(self.atoms, neighbors)}


def molecules(self) -> list[Molecule]:
    molecules: list[Molecule] = []

    def parseNeighbors(parsedAtoms: dict[Atom, bool], atom: Atom) -> None:
        if not parsedAtoms.get(atom, False):
            parsedAtoms[atom] = True
            for neighborAtom in self.neighborsPerAtom[atom]:
                parseNeighbors(parsedAtoms, neighborAtom)

    totalParsedAtoms: dict[Atom, bool] = {}

    for atom in self.neighborsPerAtom.keys():
        if not totalParsedAtoms.get(atom, False):
            newMoleculeAtoms: dict[Atom, bool] = {}
            parseNeighbors(newMoleculeAtoms, atom)
            totalParsedAtoms.update(newMoleculeAtoms)
            # is this one-liner understandable?
            molecules.append(Molecule([atom for atom in newMoleculeAtoms.keys()]))

    return molecules


def speciation(self):
    return Speciation.fromList(self.molecules)

from functools import cached_property

import globalConfigs
import numpy as np
import numpy.typing as npt
from Classes.Chemistry.Atom import Atom
from Classes.Chemistry.Molecule import Molecule
from Classes.Speciation import Speciation
from matplotlib import pyplot as plt


class AtomicSystem:
    cutoffRadii = globalConfigs.cutOff

    def __init__(
        self,
        atoms: list[Atom],
        numpyArrays: tuple[
            list[str],
            npt.NDArray[np.float64],
            npt.NDArray[np.float64],
            npt.NDArray[np.float64],
        ],
        size: float,
    ):
        self.size = size
        self.atoms = atoms
        self._numpyArrays = numpyArrays

    @cached_property
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

    @cached_property
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

    @cached_property
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

    @cached_property
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

    @cached_property
    def speciation(self):
        return Speciation.fromList(self.molecules)

    # def write(self, path) -> None:
    #     with open(path, "w") as f:
    #         f.write(f"{len(self.atoms)}\n")
    #         f.write(f"# system size (angstrom) =\t{float(self.size):.10f}\n")
    #         f.writelines(
    #             f"{atom.chemSymbol}\t{float(atom.x):.10f}\t{float(atom.y):.10f}\t{float(atom.z):.10f}\n"
    #             for atom in self.__iter__()
    #         )

    def __iter__(self) -> "AtomicSystemIterator":
        return AtomicSystemIterator(self)

    def __repr__(self) -> str:
        return f"Frame with {len(self.atoms)} atoms"

    def plot(self) -> None:
        fig: plt.Figure = plt.figure()
        ax = fig.add_subplot(projection="3d")
        ax.set_xlim(0, Molecule.atomicSystemSize)
        ax.set_ylim(0, Molecule.atomicSystemSize)
        ax.set_zlim(0, Molecule.atomicSystemSize)

        colorList = [globalConfigs.colorAtom[atom.chemSymbol] for atom in self.atoms]
        x = [atom.x + Molecule.atomicSystemSize / 2 for atom in self.atoms]
        y = [atom.y + Molecule.atomicSystemSize / 2 for atom in self.atoms]
        z = [atom.z + Molecule.atomicSystemSize / 2 for atom in self.atoms]
        ax.scatter3D(x, y, z, c=colorList, s=100)
        plt.show()

    # @property
    # def children(self):
    #     return self.molecules


class AtomicSystemIterator:
    def __init__(self, atomicSystem: AtomicSystem):
        self.atoms = atomicSystem.atoms
        self.index = 0

    def __iter__(self) -> "AtomicSystemIterator":
        return self

    def __next__(self) -> "Atom":
        self.index += 1
        try:
            return self.atoms[self.index - 1]
        except IndexError:
            self.index = 0
            raise StopIteration

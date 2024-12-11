from collections.abc import Iterable
from functools import cached_property

import globalConfigs
import matplotlib.pyplot as plt
import numpy as np
import numpy.typing as npt
from Chemistry.Atom import Atom
from Systems.AtomicSystem import AtomicSystem


class SimulationCell:
    cutoffRadii = globalConfigs.cutOff

    def __init__(
        self,
        system: AtomicSystem,
        cellSize: float,
        numpyArrays: tuple[
            list[str],
            npt.NDArray[np.float64],
            npt.NDArray[np.float64],
            npt.NDArray[np.float64],
        ],
    ) -> None:
        self.system = system
        self.cellSize = cellSize
        self._data = numpyArrays

    @cached_property
    def numpyArrays(self):
        return self._data

    def plot(self) -> None:
        fig: plt.Figure = plt.figure()
        ax = fig.add_subplot(projection="3d")
        ax.set_xlim(0, self.cellSize)
        ax.set_ylim(0, self.cellSize)
        ax.set_zlim(0, self.cellSize)

        colorList = [globalConfigs.colorAtom[atom.chemSymbol] for atom in self.system]
        x = [atom.x + self.cellSize / 2 for atom in self.system]
        y = [atom.y + self.cellSize / 2 for atom in self.system]
        z = [atom.z + self.cellSize / 2 for atom in self.system]
        ax.scatter3D(x, y, z, c=colorList, s=100)
        plt.show()

    @classmethod
    def fromIterable(
        cls, atomIterable: Iterable[str], size: float = None
    ) -> "SimulationCell":
        atoms: list["Atom"] = []
        atomSymbols: list[str] = []
        xCoordinates: list[float] = []
        yCoordinates: list[float] = []
        zCoordinates: list[float] = []

        for atomLine in atomIterable:
            atom = Atom.fromStr(atomLine)
            atoms.append(atom)
            atomSymbols.append(atom.chemSymbol)
            xCoordinates.append(float(atom.x))
            yCoordinates.append(float(atom.y))
            zCoordinates.append(float(atom.z))

        xArray = np.array(xCoordinates, dtype=float)
        yArray = np.array(yCoordinates, dtype=float)
        zArray = np.array(zCoordinates, dtype=float)
        atomicSystem = AtomicSystem(atoms=atoms)
        numpyArrays = (atomSymbols, xArray, yArray, zArray)
        return cls(atomicSystem, numpyArrays=numpyArrays, cellSize=size)

from typing import Iterable

import numpy as np
from Classes.AtomicSystem import AtomicSystem
from Classes.Chemistry.Atom import Atom


def AtomicSystemFromIterable(atomIterable: Iterable[str], size: float= None) -> 'AtomicSystem':
        atoms:          list['Atom'] = []
        atomSymbols:    list[str]   = []
        xCoordinates:   list[float] = []
        yCoordinates:   list[float] = []
        zCoordinates:   list[float] = []

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
        numpyArrays = (atomSymbols, xArray, yArray, zArray)
        return AtomicSystem(atoms, numpyArrays, size)
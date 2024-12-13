import re
from typing import Any

import globalConfigs
from matplotlib import pyplot as plt

from Packages.Chemistry.AbstractSystem import System
from Packages.Chemistry.Atom import Atom


class Molecule(System[Atom]):
    atomicSystemSize: float = 30
    __slots__ = "atoms", "formula"
    # , "label", "formula"

    # @property
    # def atoms(self) -> list[Atom]:
    #     return self.components

    def __init__(self, atomList: list[Atom]):
        super().__init__(atomList)
        self.atoms = self.components

        self.label = self.inferFormula(atomList)
        self.formula = self.label
        # self.formula = self.label

    def __repr__(self):
        return f"{self.label}: {self.atoms}"

    def __hash__(self):
        return hash(self.label)

    def __eq__(self, other: Any) -> bool:
        return self.__hash__() == other.__hash__()

    def plot(self, printPositions: bool = False):
        fig = plt.figure()
        ax = fig.add_subplot(projection="3d")
        ax.set_xlim(0, Molecule.atomicSystemSize)
        ax.set_ylim(0, Molecule.atomicSystemSize)
        ax.set_zlim(0, Molecule.atomicSystemSize)

        colorList = [globalConfigs.colorAtom[atom.label] for atom in self.atoms]
        x = [atom.x + Molecule.atomicSystemSize / 2 for atom in self.atoms]
        y = [atom.y + Molecule.atomicSystemSize / 2 for atom in self.atoms]
        z = [atom.z + Molecule.atomicSystemSize / 2 for atom in self.atoms]
        if printPositions:
            print(f"{self}")
            for atom in self.atoms:
                print(atom.label, atom.x, atom.y, atom.z)
        ax.scatter3D(x, y, z, c=colorList, s=100)
        plt.show()

    # @classmethod
    # def fromAtoms(cls, atoms: list["Atom"]) -> "Molecule":
    #     try:
    #         atoms[-1].chemSymbol
    #     except AttributeError:
    #         raise ValueError("Input is not a list of Atom objects")
    #     return cls(atoms)

    @classmethod
    def fromChemicalFormula(cls, chemicalFormula: str) -> "Molecule":
        atomicElementPattern = r"([A-Z][a-z]*)(\d*)"
        atomicMatches: list[tuple[str, str]] = re.findall(
            atomicElementPattern, chemicalFormula
        )
        atomicComposition: list[Atom] = []
        for elementSymbol, elementCount in atomicMatches:
            if elementCount == "":
                elementCount = 1
            element = Atom(chemSymbol=elementSymbol)
            atomicComposition += [element] * int(elementCount)
        return Molecule(atomicComposition)

    @classmethod
    def inferFormula(cls, listOfAtoms: list["Atom"]) -> str:
        countH: int = 0
        countN: int = 0
        countO: int = 0
        for child in listOfAtoms:
            if child.__repr__() == "H":
                countH += 1
            if child.__repr__() == "N":
                countN += 1
            if child.__repr__() == "O":
                countO += 1

        if countH == 0:
            strH: str = ""
        elif countH == 1:
            strH: str = "H"
        else:
            strH: str = f"H{countH}"

        if countN == 0:
            strN: str = ""
        elif countN == 1:
            strN: str = "N"
        else:
            strN: str = f"N{countN}"

        if countO == 0:
            strO: str = ""
        elif countO == 1:
            strO: str = "O"
        else:
            strO: str = f"O{countO}"

        name: str = f"{''.join([strH, strN, strO])}"
        return name


def main():
    hydrogen = Atom(chemSymbol="H", x=1.0, y=1.0, z=1.0)
    oxygen = Atom(chemSymbol="O", x=9.0, y=9.0, z=9.0)
    someList = [hydrogen, oxygen]

    newMolecule = Molecule(someList)
    someOtherMolecule = Molecule.fromChemicalFormula("HNO3")
    print(newMolecule)
    print(someOtherMolecule)
    # print(isinstance(newMolecule, Vector))


if __name__ == "__main__":
    main()

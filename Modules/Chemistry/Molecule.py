import re
from typing import Any

import globalConfigs
from Chemistry.Atom import Atom
from Classes.ChemicalFormula import ChemicalFormula
from Classes.Vector import Vector
from matplotlib import pyplot as plt


class Molecule(Vector):
    atomicSystemSize: float = 30

    def __init__(self, atomList: list[Atom]):
        self.atoms = atomList
        self.chemicalFormula = ChemicalFormula.fromAtoms(self.atoms)

    def __repr__(self):
        return f"{self.chemicalFormula}: {self.atoms}"

    def __hash__(self):
        return hash(self.chemicalFormula)

    def __eq__(self, other: Any) -> bool:
        return self.__hash__() == other.__hash__()

    def plot(self, printPositions: bool = False):
        fig = plt.figure()
        ax = fig.add_subplot(projection="3d")
        ax.set_xlim(0, Molecule.atomicSystemSize)
        ax.set_ylim(0, Molecule.atomicSystemSize)
        ax.set_zlim(0, Molecule.atomicSystemSize)

        colorList = [globalConfigs.colorAtom[atom.chemSymbol] for atom in self.atoms]
        x = [atom.x + Molecule.atomicSystemSize / 2 for atom in self.atoms]
        y = [atom.y + Molecule.atomicSystemSize / 2 for atom in self.atoms]
        z = [atom.z + Molecule.atomicSystemSize / 2 for atom in self.atoms]
        if printPositions:
            print(f"{self}")
            for atom in self.atoms:
                print(atom.chemSymbol, atom.x, atom.y, atom.z)
        ax.scatter3D(x, y, z, c=colorList, s=100)
        plt.show()

    @classmethod
    def fromAtoms(cls, atoms: list["Atom"]) -> "Molecule":
        try:
            atoms[-1].chemSymbol
        except AttributeError:
            raise ValueError("Input is not a list of Atom objects")
        return cls(atoms)

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


def main():
    hydrogen = Atom("H", 1.0, 1.0, 1.0)
    oxygen = Atom("O", 9.0, 9.0, 9.0)
    someList = [hydrogen, oxygen]

    newMolecule = Molecule.fromAtoms(someList)
    someOtherMolecule = Molecule.fromChemicalFormula("HNO3")
    print(newMolecule)
    print(someOtherMolecule)


if __name__ == "__main__":
    main()

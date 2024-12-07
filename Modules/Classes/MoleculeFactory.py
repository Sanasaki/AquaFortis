import re

from Classes.Chemistry.Atom import Atom
from Classes.Chemistry.Molecule import Molecule


def MoleculeFromAtoms(atoms: list["Atom"]) -> "Molecule":
    try:
        atoms[-1].chemSymbol
    except AttributeError:
        raise ValueError("Input is not a list of Atom objects")
    return Molecule(atoms)


def MoleculeFromChemicalFormula(chemicalFormula: str) -> "Molecule":
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

    newMolecule = MoleculeFromAtoms(someList)
    someOtherMolecule = MoleculeFromChemicalFormula("HNO3")
    print(newMolecule)
    print(someOtherMolecule)


if __name__ == "__main__":
    main()

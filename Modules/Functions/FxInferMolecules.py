from Chemistry.Atom import Atom
from Chemistry.Molecule import Molecule


def inferMolecules(neighborsPerAtom: dict[Atom, list[Atom]]) -> list["Molecule"]:
    molecules: list[Molecule] = []

    def parseNeighbors(parsedAtoms: dict[Atom, bool], atom: Atom) -> None:
        if not parsedAtoms.get(atom, False):
            parsedAtoms[atom] = True
            for neighborAtom in neighborsPerAtom[atom]:
                parseNeighbors(parsedAtoms, neighborAtom)

    totalParsedAtoms: dict[Atom, bool] = {}

    for atom in neighborsPerAtom.keys():
        if not totalParsedAtoms.get(atom, False):
            newMoleculeAtoms: dict[Atom, bool] = {}
            parseNeighbors(newMoleculeAtoms, atom)
            totalParsedAtoms.update(newMoleculeAtoms)
            # is this one-liner understandable?
            molecules.append(Molecule([atom for atom in newMoleculeAtoms.keys()]))

    return molecules

from dataclasses import dataclass

from Chemistry.Molecule import Molecule
from Scripts.LammpsFactoryComponent.LammpsScriptComponent import LammpsScriptComponent
from Systems.Speciation import MolecularSystem


@dataclass
class LammpsRegion(LammpsScriptComponent):
    boundary: str
    name: str
    size: float

    def write(self, append: str = "", indent: int = 0) -> str:
        # super().write(indent)
        content: str = ""
        content += f"{'\t'*indent}"
        content += f"boundary\t{self.boundary}\n"

        content += f"{'\t'*indent}"
        content += f"region\t{self.name}\tblock "

        xlo: float = -self.size / 2
        xhi: float = self.size / 2
        ylo: float = -self.size / 2
        yhi: float = self.size / 2
        zlo: float = -self.size / 2
        zhi: float = self.size / 2
        content += f"{xlo} {xhi} {ylo} {yhi} {zlo} {zhi}\n"
        return content


@dataclass
class DefaultRegion(LammpsRegion):
    boundary: str = "p p p"
    name: str = "system"
    size: float = 10.0


@dataclass
class RegionPart(LammpsScriptComponent):
    """Needs to be part of a Region"""

    region: LammpsRegion


class Malloc(RegionPart):
    def __init__(self, region: LammpsRegion):
        super().__init__(region=region)
        self.numberOfAtomTypes: int = 0
        self.mallocDict: dict[str, int] = {}

    # bond_types: int = 0
    # angle_types: int = 0
    # dihedral_types: int = 0
    # improper_types: int = 0
    # extra_bond_per_atom: int = 0
    # extra_angle_per_atom: int = 0
    # extra_special_per_atom: int = 0
    # extra_dihedral_per_atom: int = 0
    # extra_improper_per_atom: int = 0

    def write(self, append: str = "", indent: int = 0) -> str:
        content: str = (
            f"create_box {self.mallocDict["numberOfAtomTypes"]} {self.region.name} &\n"
        )
        content += f"bond/types {self.mallocDict['bond/types']} &\n"
        content += f"angle/types {self.mallocDict['angle/types']} &\n"
        content += f"dihedral/types {self.mallocDict['dihedral/types']} &\n"
        content += f"improper/types {self.mallocDict['improper/types']} &\n"
        content += f"extra/bond/per/atom {self.mallocDict['extra/bond/per/atom']} &\n"
        content += f"extra/angle/per/atom {self.mallocDict['extra/angle/per/atom']} &\n"
        content += (
            f"extra/special/per/atom {self.mallocDict['extra/special/per/atom']} &\n"
        )
        content += (
            f"extra/dihedral/per/atom {self.mallocDict['extra/dihedral/per/atom']} &\n"
        )
        content += (
            f"extra/improper/per/atom {self.mallocDict['extra/improper/per/atom']}\n"
        )
        return content


Nitric = {
    "numberOfAtomTypes": 4,
    "bond/types": 2,
    "angle/types": 4,
    "dihedral/types": 1,
    "improper/types": 1,
    "extra/bond/per/atom": 2,
    "extra/angle/per/atom": 2,
    "extra/special/per/atom": 0,
    "extra/dihedral/per/atom": 1,
    "extra/improper/per/atom": 1,
}

HardCodedAtoms: str = "labelmap atom &\n\
    1 H[Nitric] &\n\
    2 N[Nitric] &\n\
    3 O1[Nitric] &\n\
    4 O2[Nitric] &\n\
    5 O[Water] &\n\
    6 H[Water] &\n\
    7 N[Nitrate] &\n\
    8 O[Nitrate] &\n\
    9 H[Hydronium] &\n\
    10 O[Hydronium]\n"

HardCodedBonds: str = "labelmap bond &\n\
    1 OH[Nitric] &\n\
    2 NO[Nitric] &\n\
    3 OH[Water] &\n\
    4 NO[Nitrate] &\n\
    5 OH[Hydronium]\n"

HardCodedAngles: str = "labelmap angle &\n\
    1 NOH[Nitric] &\n\
    2 ONO_1[Nitric] &\n\
    3 ONO_2[Nitric] &\n\
    4 ONO_3[Nitric] &\n\
    5 HOH[Water] &\n\
    6 ONO[Nitrate] &\n\
    7 HOH[Hydronium]\n"

Water = {
    "numberOfAtomTypes": 2,
    "bond/types": 1,
    "angle/types": 1,
    "dihedral/types": 0,
    "improper/types": 0,
    "extra/bond/per/atom": 1,
    "extra/angle/per/atom": 1,
    "extra/special/per/atom": 3,
    "extra/dihedral/per/atom": 0,
    "extra/improper/per/atom": 0,
}

Nitrate = {
    "numberOfAtomTypes": 2,
    "bond/types": 1,
    "angle/types": 1,
    "dihedral/types": 0,
    "improper/types": 0,
    "extra/bond/per/atom": 0,
    "extra/angle/per/atom": 0,
    "extra/special/per/atom": 0,
    "extra/dihedral/per/atom": 0,
    "extra/improper/per/atom": 0,
}


Hydronium = {
    "numberOfAtomTypes": 2,
    "bond/types": 1,
    "angle/types": 1,
    "dihedral/types": 0,
    "improper/types": 0,
    "extra/bond/per/atom": 0,
    "extra/angle/per/atom": 0,
    "extra/special/per/atom": 0,
    "extra/dihedral/per/atom": 0,
    "extra/improper/per/atom": 0,
}


@dataclass
class LammpsMolecules(RegionPart, LammpsScriptComponent):
    rng: int = 123456
    overlap: float = 1.2
    path: str = "./input/molecules/"

    def __init__(self, region: LammpsRegion):
        super().__init__(region=region)
        self.particles: dict[str, int] = {}
        self.malloc: Malloc = Malloc(region=region)

    def write(self, append: str = "", indent: int = 0) -> str:
        content = self.malloc.write(indent=indent)
        content += "\n"
        content += HardCodedAtoms
        content += HardCodedBonds
        content += HardCodedAngles
        content += "\n"
        content += "include ./input/MassesPotentials.lmp\n"

        for key, value in self.particles.items():
            content += "\n"
            content += f"{'\t'*indent}"
            content += f"molecule {key} {self.path}{key}.lmp\n"

            content += f"{'\t'*indent}"
            content += f"create_atoms 0 random {value} {self.rng} {self.region.name} mol {key} {self.rng} overlap {self.overlap}\n"
        return content

    def addMolecule(self, moleculeFormula: str, moleculeCount: int):
        self.particles[moleculeFormula] = (
            getattr(self.particles, moleculeFormula, 0) + moleculeCount
        )
        if moleculeFormula == "HNO3":
            self.malloc.mallocDict.update(
                {
                    key: self.malloc.mallocDict.get(key, 0) + Nitric.get(key, 0)
                    for key in set(Nitric)
                }
            )
        elif moleculeFormula == "H2O":
            self.malloc.mallocDict.update(
                {
                    key: self.malloc.mallocDict.get(key, 0) + Water.get(key, 0)
                    for key in set(Water)
                }
            )
        elif moleculeFormula == "NO3":
            self.malloc.mallocDict.update(
                {
                    key: self.malloc.mallocDict.get(key, 0) + Nitrate.get(key, 0)
                    for key in set(Nitrate)
                }
            )
        elif moleculeFormula == "H3O":
            self.malloc.mallocDict.update(
                {
                    key: self.malloc.mallocDict.get(key, 0) + Nitrate.get(key, 0)
                    for key in set(Nitrate)
                }
            )

    def addMolecules(self, speciation: MolecularSystem):
        for chemicalFormula, moleculeCount in speciation.species.items():
            self.addMolecule(chemicalFormula.formula, len(moleculeCount))


def test_LammpsRegion():
    test = LammpsMolecules(region=DefaultRegion())

    nitric = Molecule.fromChemicalFormula("HNO3")
    water = Molecule.fromChemicalFormula("H2O")

    molList = [nitric] * 60 + [water] * 50
    testSpeciation = MolecularSystem(molList)

    # test.addMolecule("HNO3", 10)
    test.addMolecules(testSpeciation)

    print(test.write())


if __name__ == "__main__":
    test_LammpsRegion()

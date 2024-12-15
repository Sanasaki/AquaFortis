import random
from dataclasses import dataclass, field

from Packages.Simulations.SimulationCore import Task


@dataclass
class LammpsContextManager:
    @property
    def rng(self) -> int:
        return random.randint(100000, 999999)

    jobName: str = "LammpsJob-" + str(rng)
    jobDir: str = "job"
    jobFilePath: str = jobDir + "/" + jobName + ".in"
    boundary: str = "p p p"
    units: str = "real"
    timestep: float = 0.5

    regionName: str = "system"
    regionType: str = "block"
    regionSize: float = 40.0

    overlap: float = 1.2

    molecules: dict[str, int] = field(default_factory=dict[str, int])
    fixes: list[Task] = field(default_factory=list[Task])

    atomTypes: int = 0
    bondTypes: int = 0
    angleTypes: int = 0
    dihedralTypes: int = 0
    improperTypes: int = 0
    extraBondPerAtom: int = 0
    extraAnglePerAtom: int = 0
    extraSpecialPerAtom: int = 0
    extraDihedralPerAtom: int = 0
    extraImproperPerAtom: int = 0

    paths: dict[str, str] = field(
        default_factory=lambda: {
            "input": "input",
            "job": r"C:\Users\JL252842\Documents\Thesis\Data\Processed\PythonOutput\LammpsJob",
            "reference": r"C:\Users\JL252842\Documents\Thesis\Python\Packages\Simulations\Lammps\LammpsReferenceFile",
        }
    )
    memoryAllocation: dict[str, int] = field(
        default_factory=lambda: {
            "atom/types": 0,
            "bond/types": 0,
            "angle/types": 0,
            "dihedral/types": 0,
            "improper/types": 0,
            "extra/bond/per/atom": 0,
            "extra/angle/per/atom": 0,
            "extra/special/per/atom": 0,
            "extra/dihedral/per/atom": 0,
            "extra/improper/per/atom": 0,
        }
    )
    forceField: dict[str, str] = field(
        default_factory=lambda: {
            "atom_style": "full",
            "pair_style": "lj/cut/coul/wolf 0.2 10",
            "bond_style": "zero",
            "angle_style": "zero",
            "dihedral_style": "none",
            "improper_style": "none",
        }
    )

    labelAtoms = {
        1: "H[Nitric]",
        2: "N[Nitric]",
        3: "O1[Nitric]",
        4: "O2[Nitric]",
        5: "O[Water]",
        6: "H[Water]",
        7: "N[Nitrate]",
        8: "O[Nitrate]",
        9: "H[Hydronium]",
        10: "O[Hydronium]",
    }
    labelBonds = {
        1: "OH[Nitric]",
        2: "NO[Nitric]",
        3: "OH[Water]",
        4: "NO[Nitrate]",
        5: "OH[Hydronium]",
    }
    labelAngles = {
        1: "NOH[Nitric]",
        2: "ONO_1[Nitric]",
        3: "ONO_2[Nitric]",
        4: "ONO_3[Nitric]",
        5: "HOH[Water]",
        6: "ONO[Nitrate]",
        7: "HOH[Hydronium]",
    }

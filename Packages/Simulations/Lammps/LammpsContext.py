import random
from dataclasses import dataclass, field

from Packages.Simulations.Lammps.LammpsMolecules import LammpsMolecule
from Packages.Simulations.SimulationCore import Task


@dataclass
class LammpsContext:
    @property
    def rng(self) -> int:
        return random.randint(100000, 999999)

    regionName: str = "system"
    regionType: str = "block"
    regionSize: float = 40.0
    boundary: str = "p p p"
    units: str = "real"
    timestep: float = 0.5
    molecules: list[LammpsMolecule] = field(default_factory=list[LammpsMolecule])
    overlap: float = 1.2
    paths: dict[str, str] = field(
        default_factory=lambda: {
            "input": "input",
            "job": r"C:\Users\JL252842\Documents\Thesis\Data\Processed\PythonOutput\LammpsJob",
            "reference": r"C:\Users\JL252842\Documents\Thesis\Python\Modules\Scripts\LammpsFactoryComponent\LMPincludes",
        }
    )
    fixes: list[Task] = field(default_factory=list[Task])
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

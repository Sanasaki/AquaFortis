from dataclasses import dataclass, field
from io import StringIO
from random import randint

import Packages.Simulations.Lammps.LammpsFunctions as lmp
from Packages.Simulations.SimulationCore import Simulation, Task


@dataclass
class LammpsScriptData:
    @property
    def rng(self) -> int:
        return randint(100000, 999999)

    jobName: str = f"LammpsJob-{randint(0, 100)}"
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


class LammpsScriptLogic:
    """
    Python representation of a LAMMPS script.

    Attributes:
        - context ()
        - buffer
    """

    def __init__(self, context: LammpsScriptData = None):
        if context:
            self._attributes = context
        else:
            self._attributes = LammpsScriptData()

    @property
    def jobName(self) -> str:
        return self._attributes.jobName

    def appendPart(self, part: str):
        self._buffer.write(part)
        self._buffer.write("\n\n")

    def getBuffer(self):
        self._buffer = StringIO()
        self.appendPart(self.initialization())
        self.appendPart(self.forceField())
        self.appendPart(self.region())
        self.appendPart(self.memoryAllocation())
        self.appendPart(self.labels())
        self.appendPart(self.placeMolecules())
        self.appendPart(self.writeFixes())
        return self._buffer.getvalue()

    def writeFixes(self):
        tempTaskStr = ""
        for task in self._attributes.fixes:
            tempTaskStr += self.taskToFix(task)
            tempTaskStr += "\n"
        return tempTaskStr

    def initialization(self):
        temp = lmp.writeKeyword("units", self._attributes.units)
        temp += lmp.writeKeyword("boundary", self._attributes.boundary)
        temp += lmp.writeKeyword("timestep", self._attributes.timestep)
        return temp

    def forceField(self):
        temp = lmp.writeKeyword("atom_style", "full")
        temp += lmp.writeKeyword("pair_style", "lj/cut/coul/wolf 0.2 10")
        temp += lmp.writeKeyword("bond_style", "zero")
        temp += lmp.writeKeyword("angle_style", "zero")
        temp += lmp.writeKeyword("dihedral_style", "none")
        temp += lmp.writeKeyword("improper_style", "none")
        return temp

    def region(self):
        return lmp.writeRegion("system", "block", 40.0)

    def memoryAllocation(self):
        return lmp.writeCreateBox(
            regionName=self._attributes.regionName,
            atomTypes=self._attributes.atomTypes,
            bondTypes=self._attributes.bondTypes,
            angleTypes=self._attributes.angleTypes,
            dihedralTypes=self._attributes.dihedralTypes,
            improperTypes=self._attributes.improperTypes,
            extraBondPerAtom=self._attributes.extraBondPerAtom,
            extraAnglePerAtom=self._attributes.extraAnglePerAtom,
            extraSpecialPerAtom=self._attributes.extraSpecialPerAtom,
            extraDihedralPerAtom=self._attributes.extraDihedralPerAtom,
            extraImproperPerAtom=self._attributes.extraImproperPerAtom,
        )

    def labels(self):
        return (
            lmp.writeMultilineBlock("labelmap", "atom", self._attributes.labelAtoms)
            + lmp.writeMultilineBlock("labelmap", "bond", self._attributes.labelBonds)
            + lmp.writeMultilineBlock("labelmap", "angle", self._attributes.labelAngles)
        )

    def placeMolecules(self):
        tempString = ""
        for moleculeName, moleculeAmount in self._attributes.molecules.items():
            moleculePath = f"{self._attributes.jobPath}/input/{moleculeName}.lmp"
            includeMoleculeLine = lmp.writeKeyword(moleculeName, moleculePath)
            placeMoleculeLine = lmp.writeMolecule(
                moleculeName=moleculeName,
                moleculeAmount=moleculeAmount,
                regionName=self._attributes.regionName,
                overlap=self._attributes.overlap,
                rngSeed1=self._attributes.rng,
                rngSeed2=self._attributes.rng,
            )
            tempString += includeMoleculeLine + placeMoleculeLine + "\n"
        return tempString

    @staticmethod
    def taskToFix(task: Task) -> str:
        if task.ensemble == "NVT":
            return lmp.writeFixNVT(
                runTime=task.picoseconds,
                temperature=task.temperature,
                fixName="nvtFix",
                fixedAtoms="all",
                thermoTimestep=200,
            )
        elif task.ensemble == "NPT":
            return lmp.writeFixNPT(
                runTime=task.picoseconds,
                temperature=task.temperature,
                pressure=task.pressure,
                fixName="nptFix",
                fixedAtoms="all",
                thermoTimestep=200,
                baroTimestep=1000,
            )
        else:
            raise ValueError(f"Unknown ensemble {task.ensemble}")

    @classmethod
    def createScriptFrom(cls, simulation: Simulation) -> "LammpsScriptLogic":
        context = LammpsScriptData()
        context.fixes = simulation.task
        return LammpsScriptLogic(context)


if __name__ == "__main__":
    context = LammpsScriptData()
    script = LammpsScriptLogic(context)
    someTask = Task()
    anotherTask = Task(ensemble="NPT", temperature=230.15, pressure=1.0, picoseconds=1000)
    script._attributes.fixes.append(someTask)  # type: ignore
    script._attributes.fixes.append(anotherTask)  # type: ignore
    script.getBuffer()

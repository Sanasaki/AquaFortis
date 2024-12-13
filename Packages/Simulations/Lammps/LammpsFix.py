from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class LammpsFix(ABC):
    fixName: str
    fixedAtoms: str = "all"
    fixMolecule: bool = True
    fixType: str = ""
    runTime: int = 1000

    def write(self, append: str = "", indent: int = 0) -> str:
        content: str = ""
        content += f"fix {self.fixName} {self.fixedAtoms} {self.fixType} molecule "
        content += self.currentFixspecifities()
        content += "\n"
        content += f"run {self.runTime}\n"
        content += f"unfix {self.fixName}\n"
        return content

    @abstractmethod
    def currentFixspecifities(self) -> str:
        pass


@dataclass(slots=True)
class Thermostat:
    temperature: float = 298.15
    thermoTimestep: int = 200


@dataclass(slots=True)
class Barostat:
    pressure: float = 1.0
    baroTimestep: int = 1000


class FixNVT(LammpsFix):
    def __init__(
        self,
        fixName: str,
        fixedAtoms: str = "all",
        temperature: float = 298.15,
        thermoTimeStep: int = 200,
        runTime: int = 1000,
        fixMolecule: bool = True,
    ):
        super().__init__(
            fixName=fixName,
            fixedAtoms=fixedAtoms,
            fixMolecule=fixMolecule,
            runTime=runTime,
        )
        self.fixType: str = "rigid/nvt/small"
        self.thermostat: Thermostat = Thermostat(
            temperature=temperature, thermoTimestep=thermoTimeStep
        )

    def currentFixspecifities(self) -> str:
        return f"temp {self.thermostat.temperature} {self.thermostat.temperature} {self.thermostat.thermoTimestep}"


class FixNPT(FixNVT):
    def __init__(
        self,
        fixName: str,
        fixedAtoms: str = "all",
        temperature: float = 298.15,
        thermoTimeStep: int = 200,
        pressure: float = 1.0,
        baroTimeStep: int = 1000,
        runTime: int = 1000,
        fixMolecule: bool = True,
    ):
        super().__init__(
            fixName=fixName,
            fixedAtoms=fixedAtoms,
            temperature=temperature,
            thermoTimeStep=thermoTimeStep,
            runTime=runTime,
            fixMolecule=fixMolecule,
        )
        self.fixType: str = "rigid/npt/small"
        self.barostat: Barostat = Barostat(pressure=pressure, baroTimestep=baroTimeStep)

    def currentFixspecifities(self) -> str:
        return (
            super().currentFixspecifities()
            + f" iso {self.barostat.pressure} {self.barostat.pressure} {self.barostat.baroTimestep}"
        )

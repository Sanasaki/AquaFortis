from abc import ABC, abstractmethod
from dataclasses import dataclass

from Chemistry.Molecule import Molecule

from Packages.Chemistry.AbstractSystem import System
from Packages.Chemistry.Atom import Atom


@dataclass
class Task:
    ensemble: str = "NVT"
    temperature: float = 298.15
    pressure: float = 1.0
    picoseconds: int = 1000


class Simulation(ABC):
    """
    Careful, we don't do atomic simulation here, but molecular simulation.
    """

    def __init__(self, system: System[Molecule], task: list[Task]):
        self.system = system
        self.task = task


class SimulationScript(ABC):
    """
    Middle level object. Acts as a single-use collecting and ordering information in order to build a coherent simulation script.
    """

    @abstractmethod
    def build(self) -> str: ...


class AtomisticModelisationEngine(ABC):
    """
    An Atomistic Modelisation Engine (AME) is an abstract class designed to interface with simulation execution by third party software (e.g. LAMMPS, CP2K).\n
    It "has" a Simulation attribute, which is the Simulation to be executed.
    It has to be able to interpret by itself the Simulation object.
    When called, it should build a job file/dir which can easily be executed.\n
    For example, let "LAMMPS" be an implementation of an AME.
    It should intuitevely be used like this:

    ```python
    aQuiteShySystem = System[Molecule](HNO3=10, H2O=10, NO3=10, H3O=10)
    someIntensiveTask = Task(ensemble=NVT, T=298, timestep=0.5, runTime=100ps)
    aVeryInterestingSimulation = Simulation(aQuiteShySystem, someIntensiveTask)
    LAMMPS(aVeryInterestingSimulation)
    ```
    """

    def __init__(self, simulation: Simulation = None):
        if simulation is not None:
            self(simulation)

    @abstractmethod
    def __call__(self, simulation: Simulation): ...


if __name__ == "__main__":
    dummyTask = Task()
    someAtom = Atom(chemSymbol="H")
    someMolecule = Molecule([someAtom] * 2)
    moleculeSystem = System[Molecule]([someMolecule] * 10)
    testwithmol = Simulation(moleculeSystem, dummyTask)

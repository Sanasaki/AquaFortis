from io import StringIO

import Packages.Simulations.Lammps.LammpsLabels as LAMMPS_LABELS
from Packages.Chemistry.AbstractSystem import System
from Packages.Chemistry.Molecule import Molecule
from Packages.Simulations.Lammps.LammpsManagers import LammpsContextManager
from Packages.Simulations.Lammps.LammpsMolecules import LammpsMolecule
from Packages.Simulations.Lammps.LammpsUnits import (
    FileHandler,
    MemoryHandler,
    PostRunHandler,
    PreRunHandler,
    RunHandler,
)
from Packages.Simulations.Lammps.MoleculeHandler import MoleculeHandler
from Packages.Simulations.SimulationCore import Simulation


class OldLammpsScript:
    """
    LAMMPS implementation of AtomisticModelisationEngine. When called with a Simulation instance as an argument like `LAMMPS(simulationObject)`. It builds a LAMMPS job as follows:
    ```
    -jobDir/
    \t--inputFilesDir/
    \t--LammpsScript.lmp
    \t--SlurmScript.sh
    \t--JobDescription.json
    # inputFilesDir/: includes LAMMPS molecule files, forcefield, etc. required for LAMMPS to properly run
    # LammpsScript.lmp: the LAMMPS script file which should be run with lmp.exe -in LammpsScript.lmp
    # SlurmScript.sh: the slurm script file which should be run if run on distant machine
    # JobDescription.json: proper json file containing the job description for future reference
    ```
    """

    def __init__(self, contextManager: LammpsContextManager = None):
        self.contextManager = contextManager if contextManager else LammpsContextManager()
        self.prerunHandler: PreRunHandler = PreRunHandler(context=self.contextManager)
        self.memoryHandler: MemoryHandler = MemoryHandler(context=self.contextManager)
        self.moleculeHandler: MoleculeHandler = MoleculeHandler(
            context=self.contextManager
        )
        self.runHandler: RunHandler = RunHandler(context=self.contextManager)
        self.postrunHandler: PostRunHandler = PostRunHandler(context=self.contextManager)
        self.fileHandler: FileHandler = FileHandler(context=self.contextManager)

    def convertSystem(self, system: System[Molecule]) -> list[LammpsMolecule]:
        moleculeBuilder = LammpsMolecule()
        return [
            moleculeBuilder(molecule, amount)
            for molecule, amount in system.asDict.items()
        ]

    def setSimulation(self, simulation: Simulation):
        self.contextManager.molecules = self.convertSystem(simulation.system)
        self.contextManager.fixes = simulation.task

    def writeScript(self):
        self.fileHandler.execute()
        with open(
            self.contextManager.paths["job"] + "/AF.lmp", "w", newline="\n"
        ) as lammpsInputFile:
            lammpsInputFile.writelines(self.assemble())

    def assemble(self):
        buffer = StringIO()
        buffer.write(self.prerunHandler.build())
        buffer.write(self.memoryHandler.build())
        buffer.write(LAMMPS_LABELS.HardCodedAtoms)
        buffer.write(LAMMPS_LABELS.HardCodedBonds)
        buffer.write(LAMMPS_LABELS.HardCodedAngles)
        buffer.write("include ./input/MassesPotentials.lmp\n")
        buffer.write(self.moleculeHandler.build())
        buffer.write("include ./input/ThermoMonitoring.lmp\n")
        buffer.write(self.runHandler.build())
        buffer.write("include ./input/PostRun.lmp\n")
        buffer.write(self.postrunHandler.build())
        return buffer.getvalue()


if __name__ == "__main__":
    pass

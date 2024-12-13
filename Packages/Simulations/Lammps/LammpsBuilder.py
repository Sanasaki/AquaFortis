from io import StringIO

import Packages.Simulations.Lammps.LammpsLabels as LAMMPS_LABELS
from Packages.Chemistry.AbstractSystem import System
from Packages.Chemistry.Atom import Atom
from Packages.Chemistry.Molecule import Molecule
from Packages.Simulations.Lammps.LammpsContext import LammpsContext, LammpsMolecule
from Packages.Simulations.Lammps.LammpsUnits import (
    FileHandler,
    MemoryHandler,
    PostRunHandler,
    PreRunHandler,
    RunHandler,
)
from Packages.Simulations.Lammps.MoleculeHandler import MoleculeHandler
from Packages.Simulations.SimulationCore import Simulation, Task


class LammpsBuilder:
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

    def __init__(self):
        self.context = LammpsContext()
        self.prerunHandler: PreRunHandler = PreRunHandler(context=self.context)
        self.memoryHandler: MemoryHandler = MemoryHandler(context=self.context)
        self.moleculeHandler: MoleculeHandler = MoleculeHandler(context=self.context)
        self.runHandler: RunHandler = RunHandler(context=self.context)
        self.postrunHandler: PostRunHandler = PostRunHandler(context=self.context)
        self.fileHandler: FileHandler = FileHandler(context=self.context)

    def convertSystem(self, system: System[Molecule]) -> list[LammpsMolecule]:
        moleculeBuilder = LammpsMolecule()
        return [
            moleculeBuilder(molecule, amount)
            for molecule, amount in system.asDict.items()
        ]

    def __call__(self, simulation: Simulation):
        self.context.molecules = self.convertSystem(simulation.system)
        self.context.fixes = simulation.task
        self.fileHandler.execute()
        with open(
            self.context.paths["job"] + "/AF.lmp", "w", newline="\n"
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
    hydrogen = Atom(chemSymbol="H")
    nitrogen = Atom(chemSymbol="N")
    oxygen = Atom(chemSymbol="O")
    water = Molecule([hydrogen, hydrogen, oxygen])
    nitricAcid = Molecule([hydrogen, nitrogen, oxygen, oxygen, oxygen])
    hydronium = Molecule([hydrogen, hydrogen, hydrogen, oxygen])
    nitrate = Molecule([nitrogen, oxygen, oxygen, oxygen])
    system = System[Molecule](components=[water, nitricAcid, hydronium, nitrate] * 100)
    task = Task(ensemble="NVT", temperature=298.15, pressure=1.0, picoseconds=1000)
    simulation = Simulation(system, [task])
    LAMMPS = LammpsBuilder()
    LAMMPS(simulation)

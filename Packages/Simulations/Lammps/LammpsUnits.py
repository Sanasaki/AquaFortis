import shutil
from abc import ABC
from dataclasses import dataclass

from Packages.Simulations.Lammps.LammpsFix import FixNPT, FixNVT
from Packages.Simulations.Lammps.LammpsManagers import LammpsContextManager


@dataclass
class LammpsScriptUnit(ABC):
    context: LammpsContextManager

    def build(self) -> str: ...


class MemoryHandler(LammpsScriptUnit):
    def allocateMemory(self):
        for lammpsMolecule in self.context.molecules:
            self.context.memoryAllocation["atom/types"] += lammpsMolecule.atoms
            self.context.memoryAllocation["bond/types"] += lammpsMolecule.bonds
            self.context.memoryAllocation["angle/types"] += lammpsMolecule.angles
            self.context.memoryAllocation["dihedral/types"] += lammpsMolecule.dihedrals
            self.context.memoryAllocation["improper/types"] += lammpsMolecule.impropers
            self.context.memoryAllocation["extra/bond/per/atom"] += (
                lammpsMolecule.extraBonds
            )
            self.context.memoryAllocation["extra/angle/per/atom"] += (
                lammpsMolecule.extraAngles
            )
            self.context.memoryAllocation["extra/special/per/atom"] += (
                lammpsMolecule.extraSpecials
            )
            self.context.memoryAllocation["extra/dihedral/per/atom"] += (
                lammpsMolecule.extraDihedrals
            )
            self.context.memoryAllocation["extra/improper/per/atom"] += (
                lammpsMolecule.extraImpropers
            )

    def build(self) -> str:
        self.allocateMemory()
        memoryContent: str = "# Memory allocation\n"
        memoryContent += f"create_box {self.context.memoryAllocation['atom/types']} {self.context.regionName} &\n"
        for memoryType, allocation in self.context.memoryAllocation.items():
            if memoryType == "atom/types":
                continue
            memoryContent += f"{memoryType} {allocation} &\n"
        memoryContent = memoryContent[:-3] + "\n"
        return memoryContent


class RunHandler(LammpsScriptUnit):
    def build(self) -> str:
        runContent: str = "# Run\n"
        for fix in self.context.fixes:
            duration: int = int(fix.picoseconds / self.context.timestep)
            match fix.ensemble:
                case "NVT":
                    lammpsFix = FixNVT(
                        "nvtFix", runTime=duration, temperature=fix.temperature
                    )
                case "NPT":
                    lammpsFix = FixNPT(
                        "nptFix",
                        runTime=duration,
                        temperature=fix.temperature,
                        pressure=fix.pressure,
                    )
                case _:
                    raise ValueError(f"Unknown ensemble {fix.ensemble}")
            runContent += lammpsFix.write()
        return runContent


class PreRunHandler(LammpsScriptUnit):
    def build(self):
        initContent: str = "# Lammps script\n"
        initContent += f"units {self.context.units}\n"
        initContent += f"boundary {self.context.boundary}\n"
        initContent += f"region {self.context.regionName} {self.context.regionType}"
        size = f"{-self.context.regionSize/2} {self.context.regionSize/2}"
        initContent += f" {size} {size} {size}\n"
        initContent += f"timestep {self.context.timestep}\n"

        for key, value in self.context.forceField.items():
            initContent += f"{key} {value}\n"

        return initContent


class PostRunHandler(LammpsScriptUnit):
    def build(self) -> str:
        return "# Post run\n"


class FileHandler(LammpsScriptUnit):
    def execute(self):
        src = self.context.paths["reference"]
        dst = self.context.paths["job"]
        shutil.copytree(src, dst, dirs_exist_ok=True)

import globalConfigs
from Scripts.LammpsFactoryComponent.ForceField import ForceField, LennardJonesCoul
from Scripts.LammpsFactoryComponent.LammpsFix import FixNPT, FixNVT, LammpsFix
from Scripts.LammpsFactoryComponent.LammpsInit import DefaultInit, LammpsInit
from Scripts.LammpsFactoryComponent.LammpsRegion import (
    DefaultRegion,
    LammpsMolecules,
    LammpsRegion,
)


class LammpsFactory:
    initializer: LammpsInit = DefaultInit()
    forcefield: ForceField = LennardJonesCoul()
    region: LammpsRegion = DefaultRegion()
    particles: LammpsMolecules = LammpsMolecules(region=region)
    runs: list[LammpsFix]

    @classmethod
    def addRun(cls, fix: LammpsFix, duration: int):
        pass

    def __str__(self):
        content: str = ""
        content += self.initializer.write()
        content += "\n"
        content += self.forcefield.write()
        content += "\n"
        content += self.region.write()
        content += "\n"
        content += self.particles.write()
        content += "\n"
        content += "include ./input/ThermoMonitoring.lmp\n"
        for run in self.runs:
            content += run.write()
            content += "\n"
        content += "include ./input/PostRun.lmp\n"
        return content


def main():
    LmpFactory = LammpsFactory()
    systemMolecules = LmpFactory.particles
    systemMolecules.addMolecule("HNO3", 10)
    systemMolecules.addMolecule("H2O", 10)
    systemMolecules.addMolecule("NO3", 10)
    systemMolecules.addMolecule("H3O", 10)
    nvtEnsemble = FixNVT(fixName="testFix_1", temperature=400, runTime=50)
    nptEnsemble = FixNPT(
        fixName="testFix_2", temperature=500, pressure=1.0, runTime=500
    )
    LmpFactory.runs = [nvtEnsemble, nptEnsemble]

    # print(LmpFactory)

    outputLMPscript = globalConfigs.testFilesDirPath + "/LMP/FactoryTest.lmp"
    with open(outputLMPscript, "w") as file:
        file.write(str(LmpFactory))

    pass


if __name__ == "__main__":
    main()
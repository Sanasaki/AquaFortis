from Chemistry.Molecule import Molecule
from Systems.AbstractSystem import System


class MolecularSystem(System[Molecule]):
    def __init__(self, molecules: list[Molecule]) -> None:
        super().__init__(components=molecules)
        self.molecules = self.components
        self.species = self.components

    # @classmethod
    # def fromDict(cls, dictLine: dict[str, list[Molecule]]):
    #     return cls(species=dictLine)

    # @classmethod
    # def fromStr(cls, stringLine: str) -> dict[str, int]:
    #     # 4 {HNO3: 16, H2O: 76, H3NO4: 4}
    #     speciesLine: str = (stringLine.split('{')[-1]).split('}')[0]
    #     moleculeFound = {}
    #     for species in speciesLine.split(','):
    #         molFoundInLine = {}
    #         speciesName, speciesCount = species.strip().split(':')
    #         molFoundInLine[str(speciesName)] = int(speciesCount)
    #         moleculeFound.update(molFoundInLine)
    #     return cls(species=moleculeFound)

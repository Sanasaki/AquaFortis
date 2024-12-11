from Chemistry.Molecule import Molecule
from Systems.AbstractSystem import System


class MolecularSystem(System[Molecule]):
    """
    Speciation objects are dict, see example below:
    {HNO3: 16, H2O: 76, H3NO4: 4}
    """

    @property
    def species(self):
        return self.components

    def __init__(self, species: list[Molecule]) -> None:
        super().__init__(components=species)

    @classmethod
    def fromDict(cls, dictLine: dict[str, list[Molecule]]):
        return cls(species=dictLine)

    # @classmethod
    # def fromList(cls, listLine: list[Molecule]):

    # def __repr__(self) -> str:
    #     return f"{self.species}"

    # def toDict(self) -> str:
    #     moleculesDictList: dict[str, list[Molecule]] = {}
    #     for molecule in self.species:
    #         moleculesDictList[molecule.chemicalFormula] = moleculesDictList.get(
    #             molecule.chemicalFormula, []
    #         ) + [molecule]
    #     return cls(species=moleculesDictList)
    #     self.species.chemicalFormula
    #     printValue = "{"
    #     for keys, values in self.species.items():
    #         printValue += f"{keys}: {len(values)}, "
    #     printValue = printValue[:-2] + "}"
    #     return printValue

    # def __str__(self) -> str:
    #     printValue = "{"
    #     for keys, values in self.species.items():
    #         printValue += f"{keys}: {len(values)}, "
    #     printValue = printValue[:-2] + "}"
    #     return printValue

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

    # def toWrite(self):
    #     # {HNO3: 16, H2O: 76, H3NO4: 4}
    #     for moleculeName in self.species.keys():
    #         print(f"{moleculeName}: {len(self.species[moleculeName])}")

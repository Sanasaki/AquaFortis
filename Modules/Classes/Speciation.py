from dataclasses import dataclass

from Classes.ChemicalFormula import ChemicalFormula
from Classes.Chemistry.Molecule import Molecule


@dataclass(slots=True)
class Speciation:
    """
    Speciation objects are dict, see example below:
    {HNO3: 16, H2O: 76, H3NO4: 4}
    """

    species: dict[ChemicalFormula, list[Molecule]] = None
    index: int = None

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

    @classmethod
    def fromDict(cls, dictLine: dict[str, list[Molecule]]):
        return cls(species=dictLine)

    @classmethod
    def fromList(cls, listLine: list[Molecule]):
        moleculesDictList: dict[ChemicalFormula, list[Molecule]] = {}
        for molecule in listLine:
            moleculesDictList[molecule.chemicalFormula] = moleculesDictList.get(
                molecule.chemicalFormula, []
            ) + [molecule]
        return cls(species=moleculesDictList)

    def __repr__(self):
        # printValue = " "
        # for keys, values in self.species.items():
        #     printValue += (f"{keys}: {len(values)} ")

        return f"{self.species}"

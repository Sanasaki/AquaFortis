from dataclasses import dataclass
from random import sample

from Classes.Chemistry.Atom import Atom
from Classes.Chemistry.Molecule import Molecule


@dataclass(slots=True)
class Speciation:
    """
    Speciation objects are dict, see example below:
    {HNO3: 16, H2O: 76, H3NO4: 4}
    """

    species:  dict[str, list[Molecule]] = None
    index:      int                     = None

    @classmethod
    def fromStr(cls, stringLine: str) -> dict[str, int]:
        # 4 {HNO3: 16, H2O: 76, H3NO4: 4}
        speciesLine: str = (stringLine.split('{')[-1]).split('}')[0]
        moleculeFound = {}
        for species in speciesLine.split(','):
            molFoundInLine = {}
            speciesName, speciesCount = species.strip().split(':')
            molFoundInLine[str(speciesName)] = int(speciesCount)
            moleculeFound.update(molFoundInLine)
        return cls(species=moleculeFound)
    
    @classmethod
    def fromDict(cls, dictLine: dict[str, list[Molecule]]):
        return cls(species=dictLine)
        
    def __repr__(self):
        # printValue = " "
        # for keys, values in self.species.items():
        #     printValue += (f"{keys}: {len(values)} ")
            
        return f"{self.species}"
    

hydrogen = Atom("H", x=1, y=2, z=3)
oxygen = Atom("O", x=4, y=5, z=6)
nitrogen = Atom("N", x=7, y=8, z=9)

nitric = Molecule([hydrogen, nitrogen, oxygen, oxygen, oxygen])
water = Molecule([hydrogen, oxygen, hydrogen])

sampleDict = {nitric.chemicalFormula: [nitric], water.chemicalFormula: [water]}

TestSpeciation = Speciation.fromDict(sampleDict)

print(TestSpeciation)
# for i in TestSpeciation.species:
#     print(i, (TestSpeciation.species[i])[0].atoms)
#     (TestSpeciation.species[i])[0].plot(18)

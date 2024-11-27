from dataclasses import dataclass

from Classes.Chemistry.Molecule import Molecule


@dataclass(slots=True)
class Speciation:
    """
    Speciation objects are dict, see example below:
    {HNO3: 16, H2O: 76, H3NO4: 4}
    """

    molecules:  dict[Molecule, float]   = None
    # stringLine: str                     = None
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
        return cls(molecules=moleculeFound)
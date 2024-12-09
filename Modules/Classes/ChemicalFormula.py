from dataclasses import dataclass
from typing import Any

from Classes.Chemistry.Atom import Atom


@dataclass(slots=True)
class ChemicalFormula:
    # __slots__ = ["formula"]
    """
    formula = "HNO3"
    """

    formula: str

    # def __init__(self, inputName: str) -> None:
    #     assert isinstance(inputName, str)
    #     self.formula = inputName

    # try:
    #     self.formula = self._fromCondensed(inputName)
    # except TypeError:
    #     self.formula = self._fromAtoms(inputName)

    # @classmethod
    # def _fromCondensed(cls, condensedFormula: str, formulaRepetition: float = 1):
    #     if not isinstance(condensedFormula, str):
    #         raise TypeError
    #     else:
    #         return cls(condensedFormula)

    @classmethod
    def fromAtoms(cls, listOfAtoms: list["Atom"]) -> "ChemicalFormula":
        countH: int = 0
        countN: int = 0
        countO: int = 0
        for child in listOfAtoms:
            if child.__repr__() == "H":
                countH += 1
            if child.__repr__() == "N":
                countN += 1
            if child.__repr__() == "O":
                countO += 1

        if countH == 0:
            strH: str = ""
        elif countH == 1:
            strH: str = "H"
        else:
            strH: str = f"H{countH}"

        if countN == 0:
            strN: str = ""
        elif countN == 1:
            strN: str = "N"
        else:
            strN: str = f"N{countN}"

        if countO == 0:
            strO: str = ""
        elif countO == 1:
            strO: str = "O"
        else:
            strO: str = f"O{countO}"

        name: str = f"{''.join([strH, strN, strO])}"
        return cls(name)

    def __hash__(self):
        return hash(self.formula)

    def __eq__(self, other: Any) -> bool:
        return self.__hash__() == other.__hash__()

    def __repr__(self):
        return f"{self.formula}"

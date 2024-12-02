import re

from Classes.Chemistry.Atom import Atom


class ChemicalFormula:
    __slots__ = ["formula"]

    def __init__(self, inputName):
        try:
            self.formula = self._fromCondensed(inputName)
            # self.formula = "Blablbalba"
        except TypeError:
            # print("Atoms parsed instead of condensed formula.")
            self.formula = self._fromAtoms(inputName)

    @classmethod
    def _fromCondensed(cls, condensedFormula: str, formulaRepetition: float=1):
        if not isinstance(condensedFormula, str):
            raise TypeError
        else:
            return condensedFormula
        # HNO3
        atomicElementPattern = r"([A-Z][a-z]*)(\d*\.?\d*)"
        atomicMatches = re.findall(atomicElementPattern, condensedFormula)
        atomicComposition = {}
        for elementSymbol, elementCount in atomicMatches:
            if elementCount == "":
                elementCount = 1
            element = Atom(chemSymbol=elementSymbol)
            atomicComposition[element] = float(elementCount)*formulaRepetition

        return cls(atomicComposition)
    
    @classmethod
    def _fromAtoms(cls, listOfAtoms):
        countH = 0
        countN = 0
        countO = 0
        for child in listOfAtoms:
            if child.__repr__() == 'H': countH +=1
            if child.__repr__() == 'N': countN +=1
            if child.__repr__() == 'O': countO +=1
        if countH==0: strH=''
        if countH==1: strH='H'
        if countH>1: strH=f'H{countH}'

        if countN==0: strN=''
        if countN==1: strN='N'
        if countN>1: strN=f'N{countN}'

        if countO==0: strO=''
        if countO==1: strO='O'
        if countO>1: strO=f'O{countO}'

        name = f"{''.join([strH, strN, strO])}"
        return cls(name)
    
    def __hash__(self):
        return hash(self.formula)
    
    def __eq__(self, other):
        return self.__hash__() == other.__hash__()
    
    def __repr__(self):
        return f"{self.formula}"
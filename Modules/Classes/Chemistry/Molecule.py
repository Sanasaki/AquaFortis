import re
import sys
from operator import countOf
from time import sleep
from typing import List

from Classes.Chemistry.Atom import Atom
from matplotlib import pyplot as plt


def _getChemicalFormula(listOfAtoms):
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

    return f"{''.join([strH, strN, strO])}"

class Molecule():
    __slots__ = ["_atoms", "chemicalFormula", "_atomsSymbol"]

    @property
    def atoms(self):
        return self._atoms
    
    @atoms.setter
    def atoms(self, listOfAtoms: List[Atom]):
        self._atoms = listOfAtoms

    def __init__(self, atoms: List[Atom]=None):
        # self.name = name
        if atoms == None:
            self._atoms = []
            # print("I shouldn't get here !")
        else:
            self._atoms = atoms
            # print(atoms)
            self.chemicalFormula = _getChemicalFormula(atoms) #cette ligne doit se trouver après l'ajout des atomes, mais la formule chimique sert pour le hash, mais addAtom a besoin prématurément de ce hash pour comparer les molécules afin de transférer les atomes d'une molécule (qui a pu recevoir son nom) à une nouvelle (qui n'a pas encore pu recevoir son nom)
            # self._checkConflict()
            # for atom in atoms:
                # if atom.molecule == None: print("1")
                # if atom.molecule != None: print("2")
                # self.addAtom(atom)
                # atom.molecule = self

    def _parseFormula(self, formulaRepetition: float=1):
        # HNO3
        # HNOOO
        atomicElementPattern = r"([A-Z][a-z]*)(\d*\.?\d*)"
        atomicMatches = re.findall(atomicElementPattern, self.chemicalFormula)
        atomicComposition = {}
        for elementSymbol, elementCount in atomicMatches:
            if elementCount == "":
                elementCount = 1
            element = Atom(chemSymbol=elementSymbol)
            atomicComposition[element] = float(elementCount)*formulaRepetition

        return atomicComposition
    
    def _setAtomicSystem(self) -> None:
        self._atomsSymbol = {atom: atom.chemSymbol for atom in self.atoms}
    
    def _getAtomSymbols(self) -> list:
        return sorted([atom.chemSymbol for atom in self.atoms])
       
    def plot(self, atomicSystemSize, printPositions=False):
        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')
        ax.set_xlim([0, atomicSystemSize])
        ax.set_ylim([0, atomicSystemSize])
        ax.set_zlim([0, atomicSystemSize])
        # element, x, y, z = self.getNumpyTuple()
        colorAtom = {"H": "green", "N" : "blue", "O": "red"}
        colorList = [colorAtom[atom.chemSymbol] for atom in self.atoms]
        x = [atom.x for atom in self.atoms]
        y = [atom.y for atom in self.atoms]
        z = [atom.z for atom in self.atoms]
        if printPositions==True:
            print(f"{self}")
            for atom in self.atoms:
                print(atom.chemSymbol, atom.x, atom.y, atom.z)
        ax.scatter3D(x,y,z, c=colorList, s=100)
        plt.show()
        
    @classmethod
    def fromChemicalFormula(cls, chemicalFormula:str):
        return

    def __repr__(self):
        return f"{self.chemicalFormula}"
    
    def __hash__(self):
        return hash(self.chemicalFormula)
    
    def __eq__(self, other):
        return self.__hash__() == other.__hash__()
    



    # def __init__(self, chemicalFormula: str, atomicComposition: dict[str, float]=None, phase: str=None, count: float=None):
    #     self.chemicalFormula = chemicalFormula
    #     self.atomicComposition = self._parseFormula() if atomicComposition is None else atomicComposition
    #     self.phase = "void" if phase is None else phase
    #     self.count = float(1) if count is None else count

    # def __hash__(self):
    #     return hash(self.chemicalFormula, self.phase)
    
    # def __eq__(self, other):
    #     return (
    #         isinstance(other, Molecule) and
    #         self.chemicalFormula == other.chemicalFormula
    #     )
    
    # def __repr__(self) -> str:
    #     return f"{self.chemicalFormula}"
    
    
# Test après reset

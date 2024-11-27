
import config
from Classes.ChemicalFormula import ChemicalFormula
from Classes.Chemistry.Atom import Atom
from matplotlib import pyplot as plt


class Molecule():
    __slots__ = ["_atoms", "chemicalFormula", "_atomsSymbol"]

    def __init__(self, atoms: tuple[Atom]=None):
        if atoms == None:
            self._atoms = ()
        else:
            self._atoms = atoms
        self.chemicalFormula = ChemicalFormula(atoms)

    def __repr__(self):
        return f"{self.chemicalFormula}"
    
    def __hash__(self):
        return hash(self.chemicalFormula)
    
    def __eq__(self, other):
        return self.__hash__() == other.__hash__()
    
    @property
    def atoms(self):
        return self._atoms
    
    @atoms.setter
    def atoms(self, listOfAtoms: tuple[Atom]):
        self._atoms = listOfAtoms

    # def _setAtomicSystem(self) -> None:
    #     self._atomsSymbol = {atom: atom.chemSymbol for atom in self.atoms}
    
    # def _getAtomSymbols(self) -> list[str]:
    #     return sorted([atom.chemSymbol for atom in self.atoms])
       
    def plot(self, atomicSystemSize, printPositions=False):
        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')
        ax.set_xlim([0, atomicSystemSize])
        ax.set_ylim([0, atomicSystemSize])
        ax.set_zlim([0, atomicSystemSize])
        
        colorList = [config.colorAtom[atom.chemSymbol] for atom in self.atoms]
        x = [atom.x for atom in self.atoms]
        y = [atom.y for atom in self.atoms]
        z = [atom.z for atom in self.atoms]
        if printPositions==True:
            print(f"{self}")
            for atom in self.atoms:
                print(atom.chemSymbol, atom.x, atom.y, atom.z)
        ax.scatter3D(x,y,z, c=colorList, s=100)
        plt.show()
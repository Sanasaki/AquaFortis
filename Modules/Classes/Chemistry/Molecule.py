
import copy

import config
from Classes.ChemicalFormula import ChemicalFormula
from Classes.Chemistry.Atom import Atom
from Classes.Vector import Vector
from matplotlib import pyplot as plt


class Molecule(Vector):
    atomicSystemSize: float = 30
    # __slots__ = ["_atoms", "chemicalFormula", "_atomsSymbol"]

    def __init__(self, atoms: tuple[Atom]=None, x: float=None, y: float=None, z: float=None):
        super().__init__(x, y, z)
        if atoms == None:
            self._atoms: tuple[Atom] = ()
        else:
            self._atoms: tuple[Atom] = atoms
        self.chemicalFormula = ChemicalFormula(atoms)

    def __repr__(self):
        return f"{self.chemicalFormula}"
    
    def __hash__(self):
        return hash(self.chemicalFormula)
    
    def __eq__(self, other):
        return self.__hash__() == other.__hash__()
    
    # def __add__(self, other):
    #     return Aggregate(self + other)
    
    # def plot(self):
    #     return self
    
    @property
    def atoms(self):
        return self._atoms
    
    # @atoms.setter
    # def atoms(self, listOfAtoms: tuple[Atom]):
    #     self._atoms = listOfAtoms

    # def _setAtomicSystem(self) -> None:
    #     self._atomsSymbol = {atom: atom.chemSymbol for atom in self.atoms}
    
    # def _getAtomSymbols(self) -> list[str]:
    #     return sorted([atom.chemSymbol for atom in self.atoms])
       
    def plot(self, printPositions=False):
        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')
        ax.set_xlim([0, Molecule.atomicSystemSize])
        ax.set_ylim([0, Molecule.atomicSystemSize])
        ax.set_zlim([0, Molecule.atomicSystemSize])
        
        colorList = [config.colorAtom[atom.chemSymbol] for atom in self.atoms]
        x = [atom.x + Molecule.atomicSystemSize/2 for atom in self.atoms]
        y = [atom.y + Molecule.atomicSystemSize/2 for atom in self.atoms]
        z = [atom.z + Molecule.atomicSystemSize/2 for atom in self.atoms]
        if printPositions==True:
            print(f"{self}")
            for atom in self.atoms:
                print(atom.chemSymbol, atom.x, atom.y, atom.z)
        ax.scatter3D(x,y,z, c=colorList, s=100)
        plt.show()



def main():
    hydrogen = Atom("H", 1.0, 1.0, 1.0)
    oxygen = Atom("O", 9.0, 9.0, 9.0)

    hydroxide = Molecule((hydrogen, oxygen))
    newHydroxide = copy.deepcopy(hydroxide)
    newHydroxide.position = newHydroxide.centerOfMass(newHydroxide.atoms)
    # newHydroxyde = newHydroxide()

    print(hydroxide.position)
    for atom in hydroxide.atoms:
        print(atom.position)
        print(atom.magnitude)

    print("\n")

    print(newHydroxide.position)
    for atom in newHydroxide.atoms:
        atom.setOrigin(newHydroxide)
        print(atom.position)
        print(atom.magnitude)

if __name__ == "__main__":
    main()
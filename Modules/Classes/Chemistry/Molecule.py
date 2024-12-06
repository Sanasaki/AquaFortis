

import config
from Classes.ChemicalFormula import ChemicalFormula
from Classes.Chemistry.Atom import Atom
from Classes.Vector import Vector
from matplotlib import pyplot as plt


class Molecule(Vector):
    atomicSystemSize: float = 30

    def __init__(self, atomList: list[Atom]):
        self.atoms = atomList
        self.chemicalFormula = ChemicalFormula(self.atoms)

    def __repr__(self):
        return f"{self.chemicalFormula}: {self.atoms}"
    
    def __hash__(self):
        return hash(self.chemicalFormula)
    
    def __eq__(self, other):
        return self.__hash__() == other.__hash__()
       
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
    pass

if __name__ == "__main__":
    main()
from functools import cached_property
from typing import Iterable

import globalConfigs
import numpy as np
from Classes.Chemistry.Atom import Atom
from Classes.Chemistry.Molecule import Molecule
from Classes.Speciation import Speciation
from matplotlib import pyplot as plt


class AtomicSystem():
    cutoffRadii = globalConfigs.cutOff

    def __init__(
            self,
            atoms:  list[Atom]  = None,
            numpyArrays: tuple[list, np.ndarray, np.ndarray, np.ndarray] = None,
            size:   float       = None,
            ):
        
        if size is not None: self.size = size
        self.atoms = atoms
        self._numpyArrays = numpyArrays
    
    @cached_property
    def distanceMatrix(self) -> np.ndarray:
        
        def matrixModulo(distanceArray: np.ndarray, atomicSystemSize: float) -> np.ndarray:
            distanceArray = np.where(distanceArray>(atomicSystemSize/2), atomicSystemSize - distanceArray, distanceArray)
            return distanceArray
        
        def getDistanceArray(array: np.ndarray) -> np.ndarray:
            return abs(array[:, None] - array[None, :])

        _, x, y, z = self._numpyArrays
        
        dx = getDistanceArray(x)
        dx = matrixModulo(dx, self.size)

        dy = getDistanceArray(y)
        dy = matrixModulo(dy, self.size)

        dz = getDistanceArray(z)
        dz = matrixModulo(dz, self.size)

        return (dx**2 + dy**2 + dz**2)**(1/2)
        
    @cached_property
    def neighborsMatrix(self, isOneIndexed: bool = False) -> np.ndarray:
    
        neighborsMatrix = np.where(self.distanceMatrix < AtomicSystem.cutoffRadii, float(1), float(0))
        neighborsMatrix[neighborsMatrix==0] = ['NaN']
        # Multiplying each col by its index, thus transforming 1 -> index
        neighborsMatrix[:] *= range(len(self.distanceMatrix[0]))
        if isOneIndexed == True: neighborsMatrix[:] += 1
        
        return neighborsMatrix

    @cached_property
    def neighborsPerAtom(self) -> dict[Atom, list[Atom]]:
        #Zip function is very slow, so it should be replaced with a dict update here
        # neighbors = {}
        # this atom neighbor = {i : self.atoms[int(j)]}
        # neighbors.update(this atom neighbor)
        neighbors: list[int] = []

        for i in range(len(self.neighborsMatrix)):
            listOfIndex = ((self.neighborsMatrix[i,:])[~np.isnan(self.neighborsMatrix[i,:])]).tolist()
            iNeighbors = []
            for j in listOfIndex:
                iNeighbors.append(self.atoms[int(j)])
            neighbors.append(iNeighbors)

        return {atom: neighbors for atom, neighbors in zip(self.atoms, neighbors)}
    
    @cached_property
    def molecules(self) -> list[Molecule]:
        molecules = []
        
        def parseNeighbors(parsedAtoms:dict[Atom, bool], atom:Atom) -> None:
            if not parsedAtoms.get(atom, False):
                parsedAtoms[atom] = True
                for neighborAtom in self.neighborsPerAtom[atom]:
                    parseNeighbors(parsedAtoms, neighborAtom)

        totalParsedAtoms: dict[Atom, bool] = {}

        for atom in self.neighborsPerAtom.keys():
            if not totalParsedAtoms.get(atom, False):
                newMoleculeAtoms: dict[Atom, bool] = {}
                parseNeighbors(newMoleculeAtoms, atom)
                totalParsedAtoms.update(newMoleculeAtoms)
                # is this one-liner understandable?
                molecules.append(Molecule([atom for atom in newMoleculeAtoms.keys()]))

        return molecules

    @cached_property
    def speciation(self):
        return Speciation.fromList(self.molecules)
    
    def write(self, path) -> None:
        with open(path, "w") as f:
            f.write(f"{len(self.atoms)}\n")
            f.write(f"# system size (angstrom) =\t{float(self.size):.10f}\n")
            f.writelines(f"{atom.symbol}\t{float(atom.x):.10f}\t{float(atom.y):.10f}\t{float(atom.z):.10f}\n" for atom in self.__iter__())
    
    def __iter__(self) -> Atom:
        return AtomicSystemIterator(self)

    def __repr__(self) -> str:
        return f"Frame with {len(self.atoms)} atoms" 
    
    def plot(self):
        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')
        ax.set_xlim([0, Molecule.atomicSystemSize])
        ax.set_ylim([0, Molecule.atomicSystemSize])
        ax.set_zlim([0, Molecule.atomicSystemSize])
        
        colorList = [globalConfigs.colorAtom[atom.chemSymbol] for atom in self.atoms]
        x = [atom.x + Molecule.atomicSystemSize/2 for atom in self.atoms]
        y = [atom.y + Molecule.atomicSystemSize/2 for atom in self.atoms]
        z = [atom.z + Molecule.atomicSystemSize/2 for atom in self.atoms]
        ax.scatter3D(x,y,z, c=colorList, s=100)
        plt.show()
    
    # @property
    # def children(self):
    #     return self.molecules
class AtomicSystemIterator():
    def __init__(self, atomicSystem: AtomicSystem):
        self.atoms = atomicSystem.atoms
        self.index = 0

    def __iter__(self) -> Atom:
        return self 

    def __next__(self) -> Atom:
        self.index += 1
        try:
            return self.atoms[self.index-1]
        except IndexError:
            self.index = 0
            raise StopIteration
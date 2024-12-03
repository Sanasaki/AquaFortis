from functools import cached_property
from typing import Iterable

import config
import numpy as np
from Classes.Chemistry.Atom import Atom
from Classes.Chemistry.Molecule import Molecule
from Classes.Speciation import Speciation


class AtomicSystem():
    cutoffRadii = config.cutOff

    def __init__(
            self,
            inputData: Iterable[str]= None,
            size:           float   = None,
            ):
        
        if size is not None: self.size = size
        self.atoms:             tuple[Atom]             = Atom.fromIterable(inputData)

    def __iter__(self) -> iter:
        return AtomicSystemIterator(self) 
    
    
    @cached_property
    def _numpyArrays(self, getArrays=True) -> tuple[list[str], np.ndarray]:
        ## Fusionner la création des arrays et des atomes depuis l'iterable
        atomSymbols:    list[str]   = []
        xCoordinates:   list[float] = []
        yCoordinates:   list[float] = []
        zCoordinates:   list[float] = []

        for atom in self.atoms:
            atomSymbols.append(atom.chemSymbol)
            xCoordinates.append(float(atom.x))
            yCoordinates.append(float(atom.y))
            zCoordinates.append(float(atom.z))

        xArray = np.array(xCoordinates, dtype=float)
        yArray = np.array(yCoordinates, dtype=float)
        zArray = np.array(zCoordinates, dtype=float)

        if getArrays == True:
            return (atomSymbols, xArray, yArray, zArray)
        
        positionsMatrix = np.ndarray([xArray, yArray, zArray])
        return (atomSymbols, positionsMatrix)
    
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
    
    
    def buildAtoms(self) -> None:
        Atoms: list[Atom] = []
        symbol, x,y,z = self.getNumpyTuple()
        for i in range(len(symbol)):
            Atoms.append(Atom(chemSymbol=symbol[i], x=x[i], y=y[i], z=z[i]))
        self.atoms = Atoms
    
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
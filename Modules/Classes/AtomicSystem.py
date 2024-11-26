from typing import Iterable

import config
import numpy as np
from Classes.Chemistry.Atom import Atom
from Classes.Chemistry.Molecule import Molecule


class AtomicSystem():
    __slots__ = ["atoms", "size", "molecules", "distanceMatrix", "neighborsPerAtom", "neighborsMatrix"]

    def __init__(
            self,
            inputData: Iterable[str]= None,
            size:           float   = None,
            ):
        
        if size is not None: self.size = size
        self.atoms      = self._getAtomsFromStrIter(inputData)
        self.distanceMatrix = None
        self.neighborsPerAtom = None
        self.molecules = None

    def __iter__(self) -> iter:
        return AtomicSystemIterator(self)
    
    # The following function could be made an alternative __init__ of the Atom calss but I don't know how to do that yet
    def _getAtomsFromStrIter(self, inputData: Iterable[str]) -> list[Atom]:
        atoms = [self._getAtomFromStr(atomXYZline) for atomXYZline in inputData]
        return atoms
    
    def _getAtomFromStr(self, atomLine:str) -> Atom:
        # atomLine format example :
        # "N 12.8755651 -5.6214523 0.0156299"
        # print(atomLine)
        chemSymbol, x, y, z = atomLine.split()
        return Atom(chemSymbol, x=x, y=y, z=z)
    
        
    def buildPairsDistance(self) -> None:
        def matrixModulo(distanceArray: np.ndarray, atomicSystemSize: float) -> np.ndarray:
            distanceArray = np.where(distanceArray>(atomicSystemSize/2), atomicSystemSize-distanceArray, distanceArray)
            return distanceArray

        def getDistanceArray(array: np.ndarray) -> np.ndarray:
            return abs(array[:, None] - array[None, :])

        symbolList, x, y, z = self._getNumPyArrays(getArrays=True)
        
        dx = getDistanceArray(x)
        dx = matrixModulo(dx, self.size)

        dy = getDistanceArray(y)
        dy = matrixModulo(dy, self.size)

        dz = getDistanceArray(z)
        dz = matrixModulo(dz, self.size)

        self.distanceMatrix = (dx**2 + dy**2 + dz**2)**(1/2)
        

    def buildNeighborsMatrix(self, 
        cutoffRadii:    float   = config.cutOff, 
        isOneIndexed:   bool    = False
        ) -> None:
        if self.distanceMatrix is None: self.buildPairsDistance()
    
        # Mapping close/far atoms to 1/0
        neighborsMatrix = np.where(self.distanceMatrix < cutoffRadii, float(1), float(0))
        # Mapping 0 to NaN
        neighborsMatrix[neighborsMatrix==0] = ['NaN']
        # Multiplying each col by its index, thus transforming 1 -> index
        neighborsMatrix[:] *= range(len(self.distanceMatrix[0]))
        if isOneIndexed == True: neighborsMatrix[:] += 1
        self.neighborsMatrix = neighborsMatrix

    def buildNeighbors(self) -> None:
        if self.distanceMatrix is None: self.buildNeighborsMatrix()
        neighbors = []
        for i in range(len(self.neighborsMatrix)):
            listOfIndex = ((self.neighborsMatrix[i,:])[~np.isnan(self.neighborsMatrix[i,:])]).tolist()
            iNeighbors = []
            for j in listOfIndex:
                iNeighbors.append(self.atoms[int(j)])
            neighbors.append(iNeighbors)
        self.neighborsPerAtom = {atom: neighbors for atom, neighbors in zip(self.atoms, neighbors)}


    def buildMolecules(self) -> None:
        if self.neighborsPerAtom is None: self.buildNeighbors()
        def parseNeighbors(parsedAtoms:dict, atom:Atom):
            if not parsedAtoms.get(atom, False):
                parsedAtoms[atom] = True
                for neighborAtom in self.neighborsPerAtom[atom]:
                    parseNeighbors(parsedAtoms, neighborAtom)
        totalParsedAtoms = {}
        MolList = []
        for atom, neighbors in self.neighborsPerAtom.items():
            if not totalParsedAtoms.get(atom, False):
                parsedAtoms = {}
                parseNeighbors(parsedAtoms, atom)
                newMolecule = Molecule(parsedAtoms.keys())
                totalParsedAtoms.update(parsedAtoms)
                MolList.append(newMolecule)
        self.molecules = MolList

    def getSpeciation(self) -> str:
        if self.molecules is None: self.buildMolecules()
        moleculesCount = {}
        for molecule in self.molecules:
            moleculesCount[molecule] = moleculesCount.get(molecule, 0) + 1
        strSpeciation = str(moleculesCount)
        return strSpeciation
    
    def _getNumPyArrays(self, getArrays=False) -> tuple[list[str], np.ndarray]:
        
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
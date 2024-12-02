import time
from re import X
from typing import Iterable

import numpy as np

import config
from Classes.Chemistry.Atom import Atom
from Classes.Chemistry.Molecule import Molecule
from Classes.Speciation import Speciation
from Functions.FxStaticFunctions import FxProcessTime


class AtomicSystem():
    __slots__ = (
        "positions",
        "atoms", 
        "size", 
        "molecules", 
        "distanceMatrix", 
        "neighborsPerAtom", 
        "neighborsMatrix"
        )

    cutoffRadii = config.cutOff

    def __init__(
            self,
            inputData: Iterable[str]= None,
            size:           float   = None,
            ):
        
        if size is not None: self.size = size
        self.atoms      = Atom.fromIterable(inputData)
        self.distanceMatrix = None
        self.neighborsPerAtom = None
        self.molecules = None

    def __iter__(self) -> iter:
        return AtomicSystemIterator(self) 
    
    
    def _getNumPyArrays(self, getArrays=False) -> tuple[list[str], np.ndarray]:
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
    
    
    def buildPairsDistance(self) -> None:
        
        def matrixModulo(distanceArray: np.ndarray, atomicSystemSize: float) -> np.ndarray:
            distanceArray = np.where(distanceArray>(atomicSystemSize/2), atomicSystemSize - distanceArray, distanceArray)
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
        isOneIndexed:   bool    = False
        ) -> None:
        if self.distanceMatrix is None: self.buildPairsDistance()
    
        # Mapping close/far atoms to 1/0
        neighborsMatrix = np.where(self.distanceMatrix < AtomicSystem.cutoffRadii, float(1), float(0))
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
        startTime = time.time()
        for atom, neighbors in self.neighborsPerAtom.items():
            if not totalParsedAtoms.get(atom, False):
                parsedAtoms = {}
                parseNeighbors(parsedAtoms, atom)
                atomComposingMolecule = []
                for atom in parsedAtoms.keys():
                    atomComposingMolecule.append(atom)
                newMolecule = Molecule(atomComposingMolecule)
                # newMolecule = Molecule(parsedAtoms.keys())
                totalParsedAtoms.update(parsedAtoms)
                MolList.append(newMolecule)
        endTime = time.time()
        self.molecules = MolList

    def getSpeciation(self) -> dict[str, list[Molecule]]:
        if self.molecules is None: self.buildMolecules()
        moleculesDictList = {}
        for molecule in self.molecules:
            # faire un dict {molecule.chemicalFormula: list[molecule]}
            moleculesDictList[molecule.chemicalFormula] = moleculesDictList.get(molecule.chemicalFormula, []) + [molecule]
        return Speciation.fromDict(dictLine=moleculesDictList)
    
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

    # @classmethod
    # def fromAtomIterable(cls, lineIterable):
    #     Symbols = []
    #     Xcoords = []
    #     Ycoords = []
    #     Zcoords = []
    #     for line in lineIterable:
    #         s, x, y, z = line.split()
    #         Symbols.append(s)
    #         Xcoords.append(x)
    #         Ycoords.append(y)
    #         Zcoords.append(z)
        
    #     self.positions = np.array([Xcoords, Ycoords, Zcoords])
    
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
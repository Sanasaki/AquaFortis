from abc import ABC
from typing import Iterable

import numpy as np
import pandas as pd
from FxMatrices import periodicBoundaryConditions

from chemistry.Atom import Atom
from chemistry.Molecule import Molecule


class Volume(ABC):
    def __init__(self, volume:float) -> None:
        self.volume = volume

class AtomicSystem():
    def __init__(
            self,
            inputData:  
                list[Atom]
                | tuple[list[str], np.ndarray] 
                | Iterable[str] 
                = None,
            size:         float = None,
            tryBuildAtoms: bool = False,
            ):
        
        # self.inputData = inputData
        if size is not None: self.size = size

        # if tryBuildAtoms:
        #     if isinstance(inputData, list[Atom]):
        #         self.atoms      = inputData
        #         self.atomsTuple = self._getNumPyArrays()
        #     elif isinstance(inputData, Iterable[str]):
        #         self.atoms      = self._getAtomsFromStrIter(inputData)
        #         self.atomsTuple = self._getNumPyArrays()
        #     elif isinstance(inputData, tuple[list[str], np.ndarray]):
        #         self.atomsTuple: tuple[list[str], np.ndarray] = inputData
        #         self.atoms = self._getAtomsFromTuple(inputData)
        #     else:
        #         self.atoms = []
        #         print("Build requested, but no input data given. Creating empty system.")
        # else:
        #     if inputData is not None:
        #         self.inputData = inputData
        #         print("Data supplied but atoms not built. Creating empty system.")
        #     else:
        #         print("No data supplied. Creating empty system.")
        #     self.atoms = []
        #     self.atomsTuple = ([], np.ndarray([]))
        self.atoms      = self._getAtomsFromStrIter(inputData)
        # self.atomsTuple = self._getNumPyArrays()
        self.molecules = None,
        self.distanceMatrix = None
        self.neighbors = None
        self.molecules = None

    
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
    
    def _getAtomsFromTuple(self, inputData: tuple[list[str], np.ndarray]) -> list[Atom]:

        if self.atoms is None:
            self.atoms: list[Atom] = []
        else:
            return self.atoms
        
        atomSymbols, coordinates = self.inputData
        xyzPositions: list[list[float]] = coordinates.T.tolist()
        # nestedLists = [ [x1, y1, z1], ..., [xN, yN, zN] ]
        atoms = [
            Atom(
                chemSymbol  = atomSymbol, 
                x       = xyz[0], 
                y       = xyz[1], 
                z       = xyz[2]) 
            for atomSymbol, xyz in zip(atomSymbols, xyzPositions)
            ]
        return atoms
        
    def buildPairsDistance(self) -> None:
        # elements, x,y,z = self.getNumpyTuple()
        symbolList, x, y, z = self._getNumPyArrays(getArrays=True)

        dx = abs(x[:, None] - x[None, :])
        if self.size != None: dx = periodicBoundaryConditions(dx, self.size)

        dy = abs(y[:, None] - y[None, :])
        if self.size != None: dy = periodicBoundaryConditions(dy, self.size)

        dz = abs(z[:, None] - z[None, :])
        if self.size != None: dz = periodicBoundaryConditions(dz, self.size)

        DistanceMatrix = (dx**2 + dy**2 + dz**2)**(1/2)
        # print(DistanceMatrix)
        self.distanceMatrix = DistanceMatrix

    def buildNeighborsMatrix(self, 
        cutoffRadii:    float   = 1.575, 
        isOneIndexed:   bool    = False
        ) -> None:
        if self.distanceMatrix is None: self.buildPairsDistance()
    
        neighborsMatrix = np.where(self.distanceMatrix<cutoffRadii, float(1), float(0))
        neighborsMatrix[neighborsMatrix==0]=['NaN']
        # print(self.distanceMatrix)
        neighborsMatrix[:] *= range(len(self.distanceMatrix[0]))
        if isOneIndexed==True: neighborsMatrix[:] += 1
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
        self.neighbors = {atom: neighbors for atom, neighbors in zip(self.atoms, neighbors)}


    def buildMolecules(self) -> None:
        if self.neighbors is None: self.buildNeighbors()
        def parseNeighbors(parsedAtoms:dict, atom:Atom):
            if not parsedAtoms.get(atom, False):
                parsedAtoms[atom] = True
                for neighborAtom in self.neighbors[atom]:
                    parseNeighbors(parsedAtoms, neighborAtom)
        totalParsedAtoms = {}
        MolList = []
        for atom, neighbors in self.neighbors.items():
            if not totalParsedAtoms.get(atom, False):
                parsedAtoms = {}
                parseNeighbors(parsedAtoms, atom)
                newMolecule = Molecule(parsedAtoms.keys())
                totalParsedAtoms.update(parsedAtoms)
                MolList.append(newMolecule)
        self.molecules = MolList

    def getSpeciation(self) -> dict:
        if self.molecules is None: self.buildMolecules()
        speciation = {}
        for molecule in self.molecules:
            speciation[molecule] = speciation.get(molecule, 0) + 1
        return speciation
    
    def placeHolder(self):
        atomSymbols:    list[str]   = []
        xCoordinates:   list[float] = []
        yCoordinates:   list[float] = []
        zCoordinates:   list[float] = []
            # chemSymbol, x, y, z = atomXYZline.split()
            # atomSymbols.append(chemSymbol)
            # xCoordinates.append(float(x))
            # yCoordinates.append(float(y))
            # zCoordinates.append(float(z))

        xArray = np.array(xCoordinates, dtype=float)
        yArray = np.array(yCoordinates, dtype=float)
        zArray = np.array(zCoordinates, dtype=float)
        positionsMatrix = np.ndarray([xArray, yArray, zArray], dtype=float)

        atoms = self._getAtomsFromTuple(zip(atomSymbols, positionsMatrix))
    
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
    

    
    def _getNumpyTuple(self) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        def cleanMatrix(array: np.ndarray) -> np.ndarray:
            array += self.size
            array = np.where(array>self.size, array%self.size, array)
            return array
        
        elements        = self.data.Element.to_numpy(dtype=str)
        xCoordinates    = cleanMatrix(self.data.x.to_numpy(dtype=float))
        yCoordinates    = cleanMatrix(self.data.y.to_numpy(dtype=float))
        zCoordinates    = cleanMatrix(self.data.z.to_numpy(dtype=float))
        return elements, xCoordinates, yCoordinates, zCoordinates
    
    def __iter__(self) -> iter:
        return AtomicSystemIterator(self)
    
    # def _initDataFromAtoms(self) -> None:
    #     """
    #     N x y z
    #     O x y z
    #     O x y z
    #     H x y z
    #     """
    #     data = np.ndarray([[ for row in self.atoms] for atom in self.atoms])
    #     self.data = data
    
    
class AtomicSystemIterator():
    def __init__(self, atomicSystem):
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
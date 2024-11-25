import concurrent.futures
import glob
import os
from asyncio import as_completed
from io import TextIOWrapper
from itertools import batched, islice
from threading import Thread
from typing import Iterable, List

import numpy as np
import pandas as pd
from AtomicSystem import AtomicSystem
from chemistry.Atom import Atom
from chemistry.Molecule import Molecule
from File import File
from FxMatrices import periodicBoundaryConditions
from FxStaticFunctions import FxAssignThreadsToTasks, FxProcessTime, makeDir
from matplotlib import pyplot as plt

# class CP2K(File):
    # subclass input
    # subclass output
    # subclass ener ?
# class LAMMPS(File):
    # subclass params
    # subclass output ?

# class Frame:
#     def __init__(self, sliceOfTxt:iter):
#         self.sliceOfTxt = sliceOfTxt
    
#     def Write(self, path:str):
#         with open(path, "a", newline= '\n') as frameFile:
#             frameFile.writelines(self.sliceOfTxt)

class CP2Kfile(File):
    def __init__(
            self, 
            filePath: str
            ):
        super().__init__(filePath)

        with open(self.filePath, 'r') as f:
            for line in f:
                if "ABC" in line:
                    self.cp2kSystemSize = float(line.split()[-1])

    def __repr__(self):
        return f"CP2K file: {self.name}"

class AtomicCoordinatesXYZfile(File):

    def __init__(
            self, 
            filePath:           str, 
            atomicSystemSize:   float   = None, 
            atomNumber:         int     = None,
            travisInstructions: str     = None,
            toInitialize:       bool    = False,
            linkedCP2KFile:         CP2Kfile= None,
            ):
        super().__init__(filePath)
        if linkedCP2KFile is not None: self.atomicSystemSize = linkedCP2KFile.cp2kSystemSize
        if atomicSystemSize is not None: self.atomicSystemSize = atomicSystemSize
        # self.atomicSystemSize = atomicSystemSize
        # if self.atomicSystemSize is None:
        #     cp2kInputFilePath = os.path.join(self.currentDirPath, "cp2k.inp")
        #     if os.path.exists(cp2kInputFilePath):
        #         with open(cp2kInputFilePath, 'r') as f:
        #             for line in f:
        #                 if "ABC" in line:
        #                     self.atomicSystemSize = float(line.split()[-1])
                            
        #                     break
        #     else:
        #         print("Warning: Atomic system size not specified, some functions may not work properly")
        self.atomNumber = self.getAtomNumber() if atomNumber is None else atomNumber
        self.travisInstructions = travisInstructions
        self.framesPath = self.currentDirPath + f"/{self.name}-frames/"

        self._linesPerFrame: int = self.atomNumber+2
        self.numberOfFrames: int = self.getFileLength() % (self._linesPerFrame)
        self._reset(toInitialize)

    def _reset(self, toInit):
        if self.isSingleFrame() and toInit==True:
            self.buildDataframe()
            self.buildPairsDistance()
            self.buildAtoms()
            self.buildNeighborsMatrix()
            self.buildNeighbors()
            self.buildMolecules()
    
    # @FxProcessTime
    def _cleanMatrix(self, m: np.ndarray) -> np.ndarray:
        m += self.atomicSystemSize
        m = np.where(m>self.atomicSystemSize, m%self.atomicSystemSize, m)
        return m
    
    # @FxProcessTime
    def plot(self):
        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')
        ax.set_xlim([0, self.atomicSystemSize])
        ax.set_ylim([0, self.atomicSystemSize])
        ax.set_zlim([0, self.atomicSystemSize])
        element, x, y, z = self.getNumpyTuple()
        colorAtom = {"H": "green", "N" : "blue", "O": "red"}
        colorList = [colorAtom[atom] for atom in element]
        ax.scatter3D(x,y,z, c=colorList, s=100)
        plt.show()

    # @FxProcessTime
    def getNumpyTuple(self):
        if self.dataFrame is None: self.buildDataframe()
        elements        = self.dataFrame.Element.to_numpy(dtype=str)

        xCoordinates    = self._cleanMatrix(self.dataFrame.x.to_numpy(dtype=float))
        yCoordinates    = self._cleanMatrix(self.dataFrame.y.to_numpy(dtype=float))
        zCoordinates    = self._cleanMatrix(self.dataFrame.z.to_numpy(dtype=float))
        return elements, xCoordinates, yCoordinates, zCoordinates
    
    # @FxProcessTime
    def buildPairsDistance(self) -> None:
        elements, x,y,z = self.getNumpyTuple()

        dx = abs(x[:, None] - x[None, :])
        if self.atomicSystemSize != None: dx = periodicBoundaryConditions(dx, self.atomicSystemSize)

        dy = abs(y[:, None] - y[None, :])
        if self.atomicSystemSize != None: dy = periodicBoundaryConditions(dy, self.atomicSystemSize)

        dz = abs(z[:, None] - z[None, :])
        if self.atomicSystemSize != None: dz = periodicBoundaryConditions(dz, self.atomicSystemSize)

        DistanceMatrix = (dx**2 + dy**2 + dz**2)**(1/2)
        self.distanceMatrix = DistanceMatrix

    # @FxProcessTime
    def buildAtoms(self) -> None:
        Atoms: List[Atom] = []
        symbol, x,y,z = self.getNumpyTuple()
        for i in range(len(symbol)):
            Atoms.append(Atom(chemSymbol=symbol[i], x=x[i], y=y[i], z=z[i]))
        self.atoms = Atoms

    # @FxProcessTime
    def buildNeighborsMatrix(self, 
        cutoffRadii:    float   = 1.575, 
        isOneIndexed:   bool    = False
        ) -> None:
    
        neighborsMatrix = np.where(self.distanceMatrix<cutoffRadii, float(1), float(0))
        neighborsMatrix[neighborsMatrix==0]=['NaN']
        neighborsMatrix[:] *= range(len(self.distanceMatrix[0]))
        if isOneIndexed==True: neighborsMatrix[:] += 1
        self.neighborsMatrix = neighborsMatrix

    # @FxProcessTime
    def buildNeighbors(self) -> None:
        neighbors = []
        for i in range(len(self.neighborsMatrix)):
            listOfIndex = ((self.neighborsMatrix[i,:])[~np.isnan(self.neighborsMatrix[i,:])]).tolist()
            iNeighbors = []
            for j in listOfIndex:
                iNeighbors.append(self.atoms[int(j)])
            neighbors.append(iNeighbors)
        self.neighbors = {atom: neighbors for atom, neighbors in zip(self.atoms, neighbors)}

    # @FxProcessTime
    def buildMolecules(self) -> None:
        def parseNeighbors(parsedAtoms:dict, atom:Atom):
            if not parsedAtoms.get(atom, False):
                parsedAtoms[atom] = True
                for neighborAtom in self.neighbors[atom]:
                    parseNeighbors(parsedAtoms, neighborAtom)
        MolList = []
        totalParsedAtoms = {}
        for atom, neighbors in self.neighbors.items():
            if not totalParsedAtoms.get(atom, False):
                parsedAtoms = {}
                parseNeighbors(parsedAtoms, atom)
                newMolecule = Molecule(parsedAtoms.keys())
                totalParsedAtoms.update(parsedAtoms)
                MolList.append(newMolecule)
        self.molecules = MolList

    # @FxProcessTime
    def getSpeciation(self) -> dict:
        speciation = {}
        for molecule in self.molecules:
            speciation[molecule] = speciation.get(molecule, 0) + 1
        return speciation
    
    # @FxProcessTime
    def _ChunkBuildDataframe(self):
        # it should produce an iterator of iterator
        # iterator of atomic system, within them being iterator of atoms
        chunkSize: int  = self.getAtomNumber()+2
        chunkIter: iter    = pd.read_table(self.filePath, index_col=False, header=None, names=["Col"], iterator=True, chunksize=chunkSize)

        def _cleanDataframe(rawChunk) -> pd.DataFrame:
            """
            Input is a chunk of a pandas Dataframe iterable
            The chunk is a standalone xyz file, formatted as :

            Line 1. {atomNumber}            // self-explainatory integer 
            Line 2. whatever                // comment line ignored by softwares
            Line 3. {Element} {x} {y} {z}   // atom coordinates
            Lines ...                       // atom coordinates
            Line {atomNumber+2}.            // atom coordinates
            
            Output : NumPy array of shape (atomNumber, 4)
            Only atom coordinates are relevant, so the first two lines are removed.
            """            
            cleanChunk = rawChunk.reset_index(drop=True)
            cleanChunk = cleanChunk.loc[~(cleanChunk.index).isin([0,1])]
            cleanChunk = rawChunk.reset_index(drop=True)

            colnames= ["Element", "x", "y", "z"]
            cleanChunk = pd.DataFrame(cleanChunk["Col"].str.split().tolist(),columns=colnames)
            return cleanChunk
            
    @FxProcessTime
    def _trajectorySlicer(self) -> Iterable[Iterable[str]]:
        # def _chunkSlicer(chunk) -> iter[str]:
        
        speciations = {}
        atomicSystems: list[AtomicSystem] = []
        with open(self.filePath, 'r') as file:
            with concurrent.futures.ThreadPoolExecutor(max_workers=12) as executor:
                blockSize = self.getAtomNumber()+2
                start, stop = 2, blockSize
                for i in range(0, self.getFileLength()-blockSize, blockSize):
                    chunk = islice(file, start, stop, 1)
                    # Dividing frame into atom coordinates lines
                    # Start = 2 to skip the first two lines
                    frame = AtomicSystem(inputData=chunk, size=self.atomicSystemSize, tryBuildAtoms=True)
                    speciation = executor.submit(frame.getSpeciation)
                    speciations[(i//blockSize)+1]= speciation.result()
        return speciations
            


                    

        
        
        
        

            
        
    # @FxProcessTime
    def buildDataframe(self) -> None :
        colnames= ["Element", "x", "y", "z"]
        df = pd.read_table(self.filePath, index_col=False, header=None, names=["Col"])
        df = df.loc[~(df.index % (self.getAtomNumber()+2)).isin([0,1])].reset_index(drop=True)
        df = pd.DataFrame(df["Col"].str.split().tolist(),columns=colnames)
        df.convert_dtypes()
        df["Element"] = df["Element"].astype('string')
        df["x"] = pd.to_numeric(df["x"], errors='coerce')
        df["y"] = pd.to_numeric(df["y"], errors='coerce')
        df["z"] = pd.to_numeric(df["z"], errors='coerce')
        self.dataFrame = df
   
    

    # def SelectLines(self,
    #         startingLine:  int=None,
    #         endingLine:    int=None
    #         ) -> iter:
        
    #     # Default values (all lines are selected)
    #     startingLine = 0 if startingLine is None else startingLine
    #     endingLine = self.getFileLength() if endingLine is None else endingLine

    #     # Instantiating the iterable
    #     with open(self.filePath, "r") as ReferenceFrameFile:
    #         lineRange = islice(ReferenceFrameFile, startingLine, endingLine)

    #     return lineRange

    # @FxProcessTime
    def getAtomNumber(self):
        with open(self.filePath, 'r') as f:
            return int(f.readline())
    
    # @FxProcessTime
    def getFileLength(self):
        with open(self.filePath, 'r') as f:
            return len(f.readlines())

    # @FxProcessTime        
    def BuildTravisInstructions(self, customName:str=None):
        if customName is None:
            customName: str = "TravisInstruction.txt"
        travisInstructionsPath = os.path.join(self.currentDirPath, customName)
        with open(travisInstructionsPath, 'w') as f:
            f.write("! TRAVIS input file")
            f.write("\n! Created with TRAVIS version compiled at Jul 30 2022 00:22:24")
            f.write("\n! Source code version: Jul 29 2022")
            f.write("\n! Input file written at Wed Oct 30 09:52:44 2024.")
            f.write("\n! Use the advanced mode until the analysis selection menu (y/n)? [no] ")
            f.write("\n")
            f.write("\n! Are the 3 cell vectors of the same size (yes/no)? [yes] ")
            f.write("\n")
            f.write("\n! Enter length of cell vector in pm: ")
            f.write("\n"+str(self.atomicSystemSize*100))
        print(f"Travis instructions written to {travisInstructionsPath}")
        return travisInstructionsPath
    
    # @FxProcessTime
    def buildFramesList(self) -> None:
        self._frames: list = glob.glob(self.framesPath + "*.xyz")
    
    def SplitTrajectory(self, exportPath:str=None, dirName:str=None) -> None:
        if self.isSingleFrame() == True:
            return
        
        makeDir(self.framesPath)
        
        # @FxProcessTime
        def writeFrame(frameName, contentToWrite):
            with open(frameName, 'w', newline="\n") as frame:
                frame.writelines(contentToWrite)
        
        # Xyz files have 2 extra lines (1 for number of atoms and 1 for comment)
        # Depending on the software producing the xyz, the comment line is different
        # Lammps = Timestep number
        # CP2K = step number/simulation time(fs)/energy
        # Ovito = lattice/origin, so no actual timestep information
        linesToWrite = self.atomNumber+2
        with open(self.filePath, 'r') as wholeXYZ:
            Content = wholeXYZ.readlines()
            frameNumber: int = len(Content)//(self.getAtomNumber()+2)
            # n=1
            with concurrent.futures.ThreadPoolExecutor(max_workers=12) as executor:
                for n in range(1, frameNumber+1):
                # for _ in range(0, len(Content), linesToWrite):
                    frameName = f"{self.framesPath}{self.name}-f{n}.xyz"
                    contentToWrite = Content[(n-1)*linesToWrite:n*linesToWrite]
                    executor.submit(writeFrame, frameName, contentToWrite)
                    # n += 1
        self.buildFramesList()
                
    def isSingleFrame(self):
        return self.getFileLength() == self.getAtomNumber()+2
    
    
    @property
    def frames(self):
        return self._frames
    
    # def atomicSystemGenerator(self) -> iter:
    #     with open(self.filePath, 'r').readlines() as file:
    #         for i in range(0, len(file), self.atomNumber+2):
    #             yield file[i+2:i+self.atomNumber+2]
    

        # for chunk in iter(lambda: f.readlines(jumpSize), []): #This could actually write all the files very fast ? with just writelines(jumpSize) or something

# class AtomicXYZfileIterator():
#     def __init__(self, AtomicXYZfile:AtomicCoordinatesXYZfile):
#         self.data: TextIOWrapper = open(AtomicXYZfile.filePath, 'r')
#         self.length: int = AtomicXYZfile.atomNumber+2
#         self.index = 0

#     def __iter__(self) -> AtomicSystem:
#         return self 

#     def __next__(self) -> AtomicSystem:
#         self.index += self.length
#         try:
#             return self.data.readlines([(self.index-self.length):self.index])
#         except IndexError:
#             self.index = 0
#             self.data.close()
#             raise StopIteration
import concurrent.futures
import glob
import os
from asyncio import as_completed
from itertools import islice
from threading import Thread
from typing import List

import numpy as np
import pandas as pd
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

class AtomicCoordinatesXYZfile(File):

    def __init__(
            self, 
            filePath:           str, 
            atomicSystemSize:   float   = None, 
            atomNumber:         int     = None,
            travisInstructions: str     = None,
            toInitialize:       bool    = False,
            ):
        super().__init__(filePath)
        self.atomicSystemSize = atomicSystemSize
        if self.atomicSystemSize is None:
            cp2kInputFilePath = os.path.join(self.currentDirPath, "cp2k.inp")
            if os.path.exists(cp2kInputFilePath):
                with open(cp2kInputFilePath, 'r') as f:
                    for line in f:
                        if "ABC" in line:
                            self.atomicSystemSize = float(line.split()[-1])
                            
                            break
            else:
                print("Warning: Atomic system size not specified, some functions may not work properly")
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
            Atoms.append(Atom(symbol=symbol[i], x=x[i], y=y[i], z=z[i]))
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
        colnames= ["Element", "x", "y", "z"]
        frameList: list = []
        for frame in pd.read_table(self.filePath, index_col=False, header=None, names=["Col"], iterator=True, chunksize=(self.getAtomNumber()+2)):
            df = frame.loc[~(frame.index % (self.getAtomNumber()+2)).isin([0,1])].reset_index(drop=True)
            df = pd.DataFrame(df["Col"].str.split().tolist(),columns=colnames)
            frameList.append(df)
        self._frames = frameList
        
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
    def buildFramesList(self) -> list:
        self._frames: list = glob.glob(self.framesPath + "*.xyz")
    
    # @FxProcessTime
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
    
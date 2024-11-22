import glob
import os
import re as regex
import threading
from typing import List

from FxStaticFunctions import (FxAssignThreadsToTasks, FxProcessTime,
                               MolecularAnalysis)

from FileTypes import AtomicCoordinatesXYZfile


class ThreadedTravis(threading.Thread):
    def __init__(self, threadID, name, framesList, travInstr, outputDir):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.framesList = framesList
        self.travInstr = travInstr
        self.outputDir = outputDir

    def run(self):
        print(f"Starting {self.name}")
        s=0
        for frame in self.framesList:
            if s>9:
                break
            MolecularAnalysis(frame=frame, travisInstructions=self.travInstr, workingDir=self.outputDir)
            s+=1
        print(f"Finished {self.name}")

# class MolecularDynamicsFrame(AtomicCoordinatesXYZfile):
#     def __init__(self, filePath:str, atomicSystemSize:float=None):
#         super().__init__(filePath)

class MolecularDynamicsTrajectory(AtomicCoordinatesXYZfile):        
    def __init__(
                self, 
                xyzFilePath: str, 
                atomicSystemSize: float=None, 
                atomNumber: int=None, 
                framesList: list=None, 
                travisInstructions: str=None
                ):
        super().__init__(xyzFilePath)
        self._frames: List[AtomicCoordinatesXYZfile] = []
        
    def BuildExportPath(self, exportPath:str=None, dirName:str=None) -> str:
        if dirName is None:
            dirName: str = "frames"
        if exportPath is None:
            exportPath = self.currentDirPath + f"/{dirName}/"
        else:
            exportPath += f"/{dirName}/"
        if not os.path.exists(exportPath):
            os.mkdir(exportPath)
        self.framesPath = exportPath
        return self.framesPath
    
    def buildFramesList(self) -> list:
        self._frames: list = glob.glob(self.framesPath + "*.xyz")   
    
    @FxProcessTime
    def MultiThreadedTravisFrames(self, threadNumber:int=4):
        ##UPGRADE:Could probably be made into a decorator or something
        if self.isSingleFrame() == True:
            return
        
        # Multi-threading
        self.buildFramesList() if self._frames == None or [] else None
        numberOfFrames= len(self._frames)
        self.BuildTravisInstructions()
        batchSize = numberOfFrames // threadNumber
        loneTasks = numberOfFrames % threadNumber
        threadsObjects = []
        travInstrDebug = self.BuildTravisInstructions()
        print(travInstrDebug)
        for travisThread in range(threadNumber):
            startFrame    = travisThread*batchSize
            endFrame      = ((travisThread+1)*batchSize)-1
            frameListForThisThread = self._frames[startFrame:endFrame]

            # Setting up directory for each thread
            outputThreadDirName = f"Thread-{travisThread}"
            outputThreadDirPath = self.currentDirPath + f"/{outputThreadDirName}/"
            if not os.path.exists(outputThreadDirPath):
                os.mkdir(outputThreadDirPath)

            thread = ThreadedTravis(travisThread, f"Thread-{travisThread}", frameListForThisThread, travInstrDebug, outputThreadDirPath)
            threadsObjects.append(thread)
            thread.start()
        loneFramesList = self._frames[-loneTasks:]
        outputThreadDirName = f"Thread-{threadNumber}"
        outputThreadDirPath = self.currentDirPath + f"/{outputThreadDirName}/"
        if not os.path.exists(outputThreadDirPath):
            os.mkdir(outputThreadDirPath)
        loneThread = ThreadedTravis(threadNumber, f"Thread-{threadNumber}", loneFramesList, travInstrDebug, outputThreadDirPath)
        threadsObjects.append(loneThread)
        loneThread.start()

        for thread in threadsObjects:
            thread.join()







    # def FindSpeciation(self, listOfTravisLogFiles):
    #     if self.framesPath is None:
    #         raise Exception("Trajectory has not been split yet")
    #     else:
    #         # In travis log file, identified molecule are listed like :
    #         # "- Molecule 1:  H3NO4 (2 pieces, 81.03 g/mol)"
    #         moleculeLinePattern = r"- Molecule\s+\d+:\s+(\w+)\s+\((\d+)\s+pieces"
    #         # Speciation is stored as a list of Molecule objects
    #         moleculesObjects = {}
    #         for file in listOfTravisLogFiles:
    #             with open(file, 'r') as f:
    #                 for line in f:
    #                     regexMatch = regex.search(moleculeLinePattern, line)
                        
    #                     if regexMatch:
    #                         foundMolecule = regexMatch.group(1)
    #                         lineMolNum = int(regexMatch.group(2))
    #                         if foundMolecule in moleculesObjects:
    #                             moleculesObjects[foundMolecule] += lineMolNum
    #                         else:
    #                             moleculesObjects[foundMolecule] = lineMolNum
    #     return moleculesObjects
    

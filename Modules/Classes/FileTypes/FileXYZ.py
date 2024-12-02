import concurrent.futures as MPI
from itertools import islice

from Classes.AtomicSystem import AtomicSystem
from Classes.FileTypes.CP2K import FileCP2Kinput
from Classes.FileTypes.File import File
from Functions.FxStaticFunctions import FxProcessTime


class FileXYZ(File):
    __slots__ = ["atomicSystemSize", "atomNumber", "linesToIgnore", "chunkSize"]

    def __init__(
            self,
            filePath:           str,
            atomicSystemSize:   float   = None,
            atomNumber:         int     = None,
            linkedCP2KFile:     FileCP2Kinput= None,
            ):

        super().__init__(filePath)

        if linkedCP2KFile   is not None: self.atomicSystemSize = linkedCP2KFile.cp2kSystemSize
        if atomicSystemSize is not None: self.atomicSystemSize = atomicSystemSize
        self.atomNumber:    int = self.getAtomNumber() if atomNumber is None else atomNumber

        # Start = 2 to skip the first two lines
        self.linesToIgnore: int = 2
        self.chunkSize:     int = self.atomNumber + self.linesToIgnore
        
    def getPicosecond(self, picosecond):
        def getFrame(index):
            theFrameStartsAt = index * self.chunkSize
            return theFrameStartsAt
        
        # 1 picosecond = 1000 fs
        # 1 fs = 2 timestep
        # 1 pico = 2000 timestep
        thePicoSecondStartsAtTimestep = picosecond * 2000
        # theFrameStartsAt = thePicoSecondStartsAtTimestep * (self.chunkSize)
        theFrameStartsAt = getFrame(thePicoSecondStartsAtTimestep)
        return int(theFrameStartsAt)
    
    def getTimeSpeciation(self, picosecondStart=0, picosecondEnd=0, output='str') -> list[str]:
        def MPIgetSpeciation(chunk):
            frame = AtomicSystem(inputData=chunk, size=self.atomicSystemSize)
            return frame.getSpeciation()


        # theFrameStartsAt = self.getPicosecond(picosecondStart)
        # theFrameEndsAt = self.getPicosecond(picosecondEnd)
        # print(theFrameStartsAt, theFrameEndsAt)
        start, stop = self.linesToIgnore, self.chunkSize
        frames = []
        # with open(self.filePath, 'r') as file:
        #     for _ in range(theFrameStartsAt, theFrameEndsAt-self.chunkSize-1, self.chunkSize):
        #         chunk = islice(file, start, stop, 1)
        #         frames.append(chunk)
        #     with MPI.ThreadPoolExecutor(max_workers=4) as executor:
        #         speciationResults = []
        #         for result in executor.map(MPIgetSpeciation, frames):
        #             speciationResults.append(result)
        #         # for _ in range(0, self.fileLength-self.chunkSize, self.chunkSize):
        #             # frame = AtomicSystem(inputData=chunk, size=18.424083371)
        #             # result = frame.getSpeciation()
        #             # speciationResults.append(result)
        #     if output == 'str':
        #         return [result.__repr__() for result in speciationResults]
        #     else:
        #         return [result for result in speciationResults]
        with open(self.filePath, 'r') as file:
            speciationResults = []
            for _ in range(0, self.fileLength-self.chunkSize, self.chunkSize):
                # while _ <= theFrameEndsAt:
                #     _ += self.chunkSize
                #     next(file)
                chunk = islice(file, start, stop, 1)
                #Coder une factory DP pour créer une liste d'atome qui sera donnée telle qu'elle à la classe AtomicSystem
                frame = AtomicSystem(inputData=chunk, size=self.atomicSystemSize)
                result = frame.getSpeciation()
                speciationResults.append(result)
        if output != 'str':
            return [result.__repr__() for result in speciationResults]
        else:
            return [result for result in speciationResults]
        
    def getAtomNumber(self):
        with open(self.filePath, 'r') as f:
            return int(f.readline())
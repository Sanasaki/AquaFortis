import concurrent.futures as MPI
from itertools import islice

from Classes.AtomicSystem import AtomicSystem
from Classes.FileTypes.CP2K import FileCP2Kinput
from Classes.FileTypes.File import File
from Classes.Speciation import Speciation
from Functions.FxStaticFunctions import FxProcessTime


class FileXYZ(File):
    __slots__ = ("atomicSystemSize", "atomNumber", "linesToIgnore", "chunkSize")

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

    @property        
    def frames(self):
        start, stop = self.linesToIgnore, self.chunkSize
        with open(self.filePath, 'r') as file:
            speciationResults: list[Speciation] = []
            for _ in range(0, self.fileLength-self.chunkSize, self.chunkSize):

                # Coder une factory DP pour créer une liste d'atome qui sera donnée telle qu'elle à la classe AtomicSystem
                # frame = FactoryAtomicSystem(chunk, self.atomicSystemSize)
                # J'ai essayé, mais je ne suis pas sûr que ç'ait vraiment simplifier quoi que ce soit
                # Alors j'ai laissé tel quel

                chunk = islice(file, start, stop, 1)
                yield AtomicSystem(inputData=chunk, size=self.atomicSystemSize)
    
    def getTimeSpeciation(self, picosecondStart=0, picosecondEnd=0) -> list[str]:
        # future implementation to select a range and not whole trajectory
        # theFrameStartsAt = self.getPicosecond(picosecondStart)
        # theFrameEndsAt = self.getPicosecond(picosecondEnd)
        # print(theFrameStartsAt, theFrameEndsAt)

        start, stop = self.linesToIgnore, self.chunkSize
        with open(self.filePath, 'r') as file:
            speciationResults: list[Speciation] = []
            for frame in self.frames:
                speciationResults.append(frame.speciation)
        return [speciation for speciation in speciationResults]
        
    def getAtomNumber(self):
        with open(self.filePath, 'r') as f:
            return int(f.readline())
        
    # def getPicosecond(self, picosecond):
    #     def getFrame(index):
    #         theFrameStartsAt = index * self.chunkSize
    #         return theFrameStartsAt
        
    #     # 1 picosecond = 1000 fs
    #     # 1 fs = 2 timestep
    #     # 1 pico = 2000 timestep
    #     thePicoSecondStartsAtTimestep = picosecond * 2000
    #     # theFrameStartsAt = thePicoSecondStartsAtTimestep * (self.chunkSize)
    #     theFrameStartsAt = getFrame(thePicoSecondStartsAtTimestep)
    #     return int(theFrameStartsAt)
    
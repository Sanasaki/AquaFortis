import concurrent.futures as MPI
from functools import cached_property
from itertools import islice

from Classes.AtomicSystem import AtomicSystem
from Classes.FileTypes.CP2K import FileCP2Kinput
from Classes.FileTypes.File import File
from Classes.Speciation import Speciation
from Classes.Trajectory import Trajectory
from Functions.FxStaticFunctions import FxProcessTime


class FileTrajectory(File):
    __slots__ = ("atomicSystemSize", "linesToIgnore", "chunkSize")

    def __init__(
            self,
            filePath:       str,
            linkedCP2KFile: FileCP2Kinput= None,
            ):

        super().__init__(filePath)

        if linkedCP2KFile   is not None: self.atomicSystemSize = linkedCP2KFile.cp2kSystemSize
        # if atomicSystemSize is not None: self.atomicSystemSize = atomicSystemSize

        # Start = 2 to skip the first two lines
        self.linesToIgnore: int = 2
        self.chunkSize:     int = self.atomNumber + self.linesToIgnore
        
    def yieldTrajectory(self):
        # Coder une factory DP pour créer une liste d'atome qui sera donnée telle qu'elle à la classe AtomicSystem
        # J'ai essayé, mais je ne suis pas sûr que ç'ait vraiment simplifier quoi que ce soit
        # Alors j'ai laissé tel quel
        
        start, stop = self.linesToIgnore, self.chunkSize
        with open(self.filePath, 'r') as file:
            speciationResults: list[Speciation] = []
            for _ in range(0, self.fileLength-self.chunkSize, self.chunkSize):
                chunk = islice(file, start, stop, 1)
                yield AtomicSystem(inputData=chunk, size=self.atomicSystemSize)

    @property
    def trajectory(self):
        return Trajectory(list(self.yieldTrajectory()))

    @property
    def atomNumber(self):
        with open(self.filePath, 'r') as f:
            return int(f.readline())

    # @property        
    # def frames(self):
    #     # Coder une factory DP pour créer une liste d'atome qui sera donnée telle qu'elle à la classe AtomicSystem
    #     # J'ai essayé, mais je ne suis pas sûr que ç'ait vraiment simplifier quoi que ce soit
    #     # Alors j'ai laissé tel quel

    #     start, stop = self.linesToIgnore, self.chunkSize
    #     with open(self.filePath, 'r') as file:
    #         speciationResults: list[Speciation] = []
    #         for _ in range(0, self.fileLength-self.chunkSize, self.chunkSize):
    #             chunk = islice(file, start, stop, 1)
    #             yield AtomicSystem(inputData=chunk, size=self.atomicSystemSize)

    # @frames.setter
    # def frames(self, value):
    #     self.frames = value

    
    # @property
    # def dynamicSpeciation(self, picosecondStart=0, picosecondEnd=0) -> list[Speciation]:
    #     # future implementation to select a range and not whole trajectory
    #     return [frame.speciation for frame in self.frames]
        
    # def getAtomNumber(self):
    #     with open(self.filePath, 'r') as f:
    #         return int(f.readline())
        
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
    
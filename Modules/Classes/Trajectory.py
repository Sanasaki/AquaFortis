from abc import ABC

from Classes.FileTypes.File import File
from Functions.FxStaticFunctions import FxProcessTime


class AtomicSystem(ABC):
    __slots__ = ("atoms", "_superSet")
    
    @property
    def superSet(self) -> 'AtomicSystem':
        return self._superSet

    @superSet.setter
    def superSet(self, newSuperSet: 'AtomicSystem') -> None:
        self._superSet = newSuperSet

    @superSet.deleter
    def superSet(self) -> None:
        del self._superSet

class Atom(AtomicSystem):
    __slots__ = ("x", "y", "z", "chemSymbol")
    pass

class Molecule(AtomicSystem):
    __slots__ = ("name")
    def __init__(self, atoms: (Atom), name:str):
        super().__init__(atoms)
        self.name = name
        pass
    pass

class Aggregate(AtomicSystem):
    __slots__ = ("molecules")
    def __init__(self, molecules: (Molecule)):
        super().__init__(molecules)
        self.molecules = molecules
    pass












# Reading order : Trajectory -> Frames -> Atoms
# Should be done as whole in pandas/numpy for quick processing

# Analyzing order : Atoms -> Molecules -> Aggregates
# Should be done for selected frame/range of frame to not overload the memory

"""
I should note that using Pandas is fast enough most of the time, 
and you get the benefit of Pandas’ sophisticated indexing features. 
It’s only in loops that the microseconds start to add up to minutes.
"""

class Frame(AtomicSystem):
    pass

# class Trajectory():
#     timestep:       float   = 0.5
#     framesPerPs:    int     = int(1000 / timestep)

#     __slots__ = ("_frames", "time")
#     def __init__(self) -> None:
#         self._frames = []
#         pass

#     def buildSubSet(self):
#         self.frames = []
#         pass

#     @property
#     def time(self):
#         return self._frames
    
#     @property
#     def frames(self):
#         return self._frames

class FileTrajectory(File):
    timestep:       float   = 0.5
    framesPerPs:    int     = int(1000 / timestep)
    linesToIgnore:  int     = 2

    __slots__ = ("trajectory", "atomNumber", "chunkSize")
    def __init__(self, filePath: str, atomNumber:int = None) -> None:
        super().__init__(filePath)
        self.atomNumber:    int = self.getAtomNumber() if atomNumber is None else atomNumber
        self.chunkSize:     int = self.atomNumber + FileTrajectory.linesToIgnore
        pass

    def readlines(self) -> list[dict[str, int]]:
        with open(self.filePath, 'r') as file:
            return file.readlines()
    
    def getDynamicSpeciation(self, range):
        self.trajectory.buildSubSet(range)
        pass
    
    
    def getPicosecond(self, picosecond):
        def getFrame(index):
            theFrameStartsAt = index * self.chunkSize
            return theFrameStartsAt
        
        # 1 picosecond = 1000 fs
        # 1 fs = 2 timestep
        # 1 pico = 2000 timestep
        thePicoSecondStartsAtTimestep = picosecond * FileTrajectory.framesPerPs
        # theFrameStartsAt = thePicoSecondStartsAtTimestep * (self.chunkSize)
        theFrameStartsAt = getFrame(thePicoSecondStartsAtTimestep)
        return int(theFrameStartsAt)
    
    def printPicosecond(self, picosecond):
        theFrameStartsAt = self.getPicosecond(picosecond)
        theFrameEndsAt = self.getPicosecond(picosecond+1)
        print(theFrameStartsAt, theFrameEndsAt)
        # return
        frames = self.readlines()
        for i, frame in enumerate(range(theFrameStartsAt, theFrameEndsAt, self.chunkSize)):
            print(i)
            # selectedFrames = frames[i*theFrameStartsAt:(i+1)*theFrameEndsAt]
            print(frame)
        pass
    
    @FxProcessTime
    def getAtomNumber(self):
        with open(self.filePath, 'r') as f:
            return int(f.readline())

    pass
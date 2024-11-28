from itertools import islice

from Classes.AtomicSystem import AtomicSystem
from Classes.FileTypes.CP2K import FileCP2Kinput
from Classes.FileTypes.File import File


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
        
    def getTimeSpeciation(self, output='str') -> list[str]:
        start, stop = self.linesToIgnore, self.chunkSize
        with open(self.filePath, 'r') as file:
            speciationResults = []
            for _ in range(0, self.fileLength-self.chunkSize, self.chunkSize):
                chunk = islice(file, start, stop, 1)
                frame = AtomicSystem(inputData=chunk, size=self.atomicSystemSize)
                result = frame.getSpeciation()
                speciationResults.append(result)
        if output == 'str':
            return [result.__repr__() for result in speciationResults]
        else:
            return [result for result in speciationResults]

    def getAtomNumber(self):
        with open(self.filePath, 'r') as f:
            return int(f.readline())
import concurrent.futures
from itertools import islice

from Classes.AtomicSystem import AtomicSystem
from Classes.File import File

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
            linkedCP2KFile:     CP2Kfile= None,
            ):
        
        super().__init__(filePath)

        if linkedCP2KFile   is not None: self.atomicSystemSize = linkedCP2KFile.cp2kSystemSize
        if atomicSystemSize is not None: self.atomicSystemSize = atomicSystemSize
        self.atomNumber:    int = self.getAtomNumber() if atomNumber is None else atomNumber
        
        # Start = 2 to skip the first two lines
        self.linesToIgnore: int = 2 
        self.chunkSize:     int = self.atomNumber + self.linesToIgnore
  
    def getTimeSpeciation(self) -> list[str]:       
        start, stop = self.linesToIgnore, self.chunkSize
        with open(self.filePath, 'r') as file:
            for _ in range(0, self.fileLength-self.chunkSize, self.chunkSize):
                chunk = islice(file, start, stop, 1)
                frame = AtomicSystem(inputData=chunk, size=self.atomicSystemSize)
                speciationResults = frame.getSpeciation()
        return [result for result in speciationResults]

    def getAtomNumber(self):
        with open(self.filePath, 'r') as f:
            return int(f.readline())
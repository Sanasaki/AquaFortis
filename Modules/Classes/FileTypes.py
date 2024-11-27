import concurrent.futures
from itertools import islice

from Classes.AtomicSystem import AtomicSystem
from Classes.File import File
from Functions.FxStaticFunctions import FxProcessTime

#test comment

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

class SpeciationFile(File):
    def __init__(
            self, 
            filePath: str,
            speciesPerStep: list[str] = None,
            ):
        super().__init__(filePath)
        if speciesPerStep != None: 
            self.speciesPerStep = speciesPerStep
            self.steps = len(speciesPerStep)

    def write(self) -> None:
        with open(self.filePath, 'w', newline='\n') as file:
            for step, item in enumerate(self.speciesPerStep):
                file.write(f"{step} {item}\n")
    
    def readlines(self) -> list[str]:
        with open(self.filePath, 'r') as file:
            return file.readlines()
    
    def plot(self):
        def getSpecies(speciationLine: str) -> dict[str, int]:
            # 4 {HNO3: 16, H2O: 76, H3NO4: 4}
            speciesLine: str = (speciationLine.split('{')[-1]).split('}')[0]
            moleculeFound = {}
            for species in speciesLine.split(','):
                molFoundInLine = {}
                speciesName, speciesCount = species.strip().split(':')
                molFoundInLine[str(speciesName)] = int(speciesCount)
                moleculeFound.update(molFoundInLine)
            return moleculeFound
        # timeSpeciation: list[dict[str, int]] = map(getSpecies, self.speciesPerStep)
        
        
        

class CP2Kfile(File):
    __slots__ = ["cp2kSystemSize"]
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
    __slots__ = ["atomicSystemSize", "atomNumber", "linesToIgnore", "chunkSize"]

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
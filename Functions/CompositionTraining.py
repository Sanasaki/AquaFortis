from __future__ import annotations

from abc import ABC
from typing import List

from FileTypes import AtomicCoordinatesXYZfile


class Component(ABC):

    @property
    def AnyParentNameCanDo(self) -> Component:
        return self._parent
    
    @AnyParentNameCanDo.setter
    def AnyParentNameCanDo(self, parent: Component) -> None:
        self._parent = parent 

    def isComposite(self) -> bool:
        return True

class frameSet(Component, AtomicCoordinatesXYZfile):
    def __init__(self, filePath) -> None:
        super().__init__(filePath)
        self._AnyChildNameAlso: List[Component] = []

    def add(self, component: Component) -> None:
        self._AnyChildNameAlso.append(component)
        component.AnyParentNameCanDo = self
    
    def remove(self, component: Component) -> None:
        self._AnyChildNameAlso.remove(component)
        component.AnyParentNameCanDo = None

    def operation(self) -> str:
        results = []
        for child in self._AnyChildNameAlso:
            results.append(child.operation())
        return f"Frames :\n{', '.join(results)}"
    

class frame(Component, AtomicCoordinatesXYZfile):
    def __init__(self, filePath) -> None:
        super().__init__(filePath)

    def operation(self) -> str:
        return f"{self.filePath}"
    
    def isComposite(self) -> bool:
        return False

AframeSet = frameSet("C:/Users/JL252842/Documents/Thesis/Python/TestFiles/xyz/80HNO3-20H2O-1-pos-1.xyz")
OneFrame = frame("C:/Users/JL252842/Documents/Thesis/Python/TestFiles/xyz/frames/80HNO3-20H2O-1-pos-1-f1.xyz")
AnotherFrame = frame("C:/Users/JL252842/Documents/Thesis/Python/TestFiles/xyz/frames/80HNO3-20H2O-1-pos-1-f2.xyz")

AframeSet.add(OneFrame)
AframeSet.add(AnotherFrame)

print(AframeSet.operation())


def MultiThreadedSplit(self):

    # 1. Preparing the threads
        # This is the second time I do something similar, so once done I should abstract it
        # 1.1. Getting file length as integer
            # If file length isn't an attribute, it should be read -and instantiated-
        # 1.2. Diving file length integer into batches (modulo T)
        # 1.3. Dispatch indexes among threads

    # 2. Defining the function frame writer
        # It will read a specific range of lines in a file, and copy them to a new frame file
        # Arguments thus should be :
        # File to read
        # Range of lines in File to read
        # frame ID (will serve to write frame file name)
    def tempName():
        yield startLine, endLine, indexNumber

    InitialPath = "SamplePath"
    OriginalTrajectory = AtomicCoordinatesXYZfile(InitialPath)
    
    
    
    A = 0
    B = 10
    newStandAloneFrameRange = OriginalTrajectory.SelectFrames(A, B)
    newStandAloneFrame.AddFrame(newStandAloneFrameRange)


for i in range (0, 47614, 462):
    print(i)



    

    
        

    # T threads will all read one file, so the "with open read-only" should be instantiated by each thread
    # for thread in range(T)
        # 
    pass
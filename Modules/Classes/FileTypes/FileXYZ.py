from collections.abc import Iterator
from itertools import islice

from Classes.AtomicSystem import AtomicSystem
from Classes.AtomicSystemFactory import AtomicSystemFromIterable
from Classes.FileTypes.CP2K import FileCP2Kinput
from Classes.FileTypes.File import File
from Classes.Trajectory import Trajectory


class FileTrajectory(File):
    __slots__ = ("atomicSystemSize", "linesToIgnore", "chunkSize")

    def __init__(
        self,
        filePath: str,
        linkedCP2KFile: FileCP2Kinput = None,
    ):
        super().__init__(filePath)

        if linkedCP2KFile is not None:
            FileTrajectory.atomicSystemSize = linkedCP2KFile.cp2kSystemSize
        else:
            luckyCP2KFile = FileCP2Kinput(filePath.replace(".xyz", ".inp"))
            self.atomicSystemSize = luckyCP2KFile.cp2kSystemSize

        # Start = 2 to skip the first two lines
        self.linesToIgnore: int = 2
        self.chunkSize: int = self.atomNumber + self.linesToIgnore

    def yieldTrajectory(self) -> Iterator[AtomicSystem]:
        start, stop = self.linesToIgnore, self.chunkSize
        with open(self.filePath, "r") as file:
            for _ in range(0, self.fileLength, self.chunkSize):
                chunk = islice(file, start, stop, 1)
                yield AtomicSystemFromIterable(
                    atomIterable=chunk, size=self.atomicSystemSize
                )

    @property
    def trajectory(self) -> Trajectory:
        return Trajectory(list(self.yieldTrajectory()))

    @property
    def atomNumber(self):
        with open(self.filePath, "r") as f:
            return int(f.readline())

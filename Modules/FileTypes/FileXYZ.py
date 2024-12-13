from collections.abc import Iterator
from itertools import islice

from Classes.Trajectory import Trajectory
from FileTypes.CP2K import FileCP2Kinput
from FileTypes.File import File

from Packages.Simulations.SimulationCell import SimulationCell


class FileTrajectory(File):
    __slots__ = (
        "atomicSystemSize",
        "linesToIgnore",
        "chunkSize",
        "trajectory",
        "trajectoryPP",
        "_atomNumber",
    )

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
            self._atomNumber = luckyCP2KFile.cp2kAtomCount

        # Start = 2 to skip the first two lines
        self.linesToIgnore: int = 2
        self.chunkSize: int = self.atomNumber + self.linesToIgnore
        self.trajectory = Trajectory(list(self.yieldTrajectory()))
        # self.trajectoryPP = Trajectory(list(self.yieldTrajectoryPP()))

    def yieldTrajectory(self) -> Iterator[SimulationCell]:
        start, stop = self.linesToIgnore, self.chunkSize
        # i = 0
        with open(self.filePath, "r") as file:
            while chunk := list(islice(file, start, stop, 1)):
                yield SimulationCell.fromIterable(
                    atomIterable=chunk, size=self.atomicSystemSize
                )

    # def yieldTrajectoryPP(self) -> Iterator[SimulationCell]:
    #     start, stop = self.linesToIgnore, self.chunkSize
    #     # i = 0
    #     with open(self.filePath, "r") as file:
    #         while chunk := list(islice(file, start, stop, 1)):
    #             yield SimulationCell.fromIterablePP(
    #                 atomIterable=chunk, size=self.atomicSystemSize
    #             )

    @property
    def atomNumber(self) -> int:
        if self._atomNumber is None:
            with open(self.filePath, "r") as f:
                self._atomNumber = int(f.readline())
        return self._atomNumber

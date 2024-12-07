from tkinter import filedialog as fd
from typing import Any

from Classes.FileTypes.CP2K import FileCP2Kinput
from Classes.FileTypes.FileXYZ import FileTrajectory
from Classes.InteractiveSpeciation import InteractiveSpeciation
from Classes.Trajectory import Trajectory


def main(**argv: Any) -> None:
    selectedFiles = fd.askopenfilenames(
        title="Select XYZ files",
        initialdir=r"C:\Users\JL252842\Documents\Thesis\Data\Raw\Simulations\2024-11-22\AIMD-SCAN-AF",
    )
    files: list[Trajectory] = []
    for xyzFile in selectedFiles:
        currentDirPath = (
            "/".join(xyzFile.split("/")[:-1])
            + f"/{xyzFile.split("/")[-1].split(".")[0]}.inp"
        )
        cp2kFile = FileCP2Kinput(currentDirPath)
        trjFile = FileTrajectory(xyzFile, linkedCP2KFile=cp2kFile)
        files.append(trjFile.trajectory)

    app = InteractiveSpeciation(files)


if __name__ == "__main__":
    main()

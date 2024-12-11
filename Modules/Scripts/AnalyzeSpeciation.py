from tkinter import filedialog as fd
from typing import Any

import numpy as np
import numpy.typing as npt
from FileTypes.CP2K import FileCP2Kinput
from FileTypes.FileXYZ import FileTrajectory
from Interfaces.InteractiveSpeciation import InteractiveSpeciation


def toCodomain(dynamicDict: list[dict[Any, int]]) -> dict[Any, npt.NDArray[np.int64]]:
    foundKeys: dict[Any, list[int]] = {}
    for timestep, molecules in enumerate(dynamicDict):
        for speciesName, speciesCount in molecules.items():
            foundKeys[speciesName] = foundKeys.get(speciesName, [0] * timestep) + [
                speciesCount
            ]

        notFoundMolecules = set(foundKeys.keys()) - set(molecules.keys())
        for notFoundMolecule in notFoundMolecules:
            foundKeys[notFoundMolecule].append(0)

    for molecule, occurrences in foundKeys.items():
        foundKeys[molecule] = np.array(occurrences, dtype=int)

    return foundKeys


def main(**argv: Any) -> None:
    # filePicked = fd.askopenfilenames(title='Select speciation to analyze', initialdir = config.pythonOutput)

    # trajectory = FileSpeciation(filePicked[0])
    # listOfDict = trajectory.plot()
    # codomains = toCodomain(listOfDict)
    # df = pd.DataFrame(codomains, dtype=float)
    # df = df[df.iloc[0].sort_values(ascending=False).index]
    # dfpercent = df.div(df.sum(axis=1), axis=0) * 100
    # ax = dfpercent.plot.area()
    # ax.set_xlim(0, len(listOfDict)-1)
    # ax.set_ylim(0, 100)

    # plt.show()

    selectedFiles = fd.askopenfilenames(
        title="Select XYZ files",
        initialdir=r"C:\Users\JL252842\Documents\Thesis\Data\Raw\Simulations\2024-11-22\AIMD-SCAN-AF",
    )
    files = []
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

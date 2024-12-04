from tkinter import filedialog as fd

import config
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from Classes.FileTypes.CP2K import FileCP2Kinput
from Classes.FileTypes.FileSpeciation import FileSpeciation
from Classes.FileTypes.FileXYZ import FileTrajectory
from Classes.InteractiveSpeciation import InteractiveSpeciation


def toCodomain(dynamicDict: list[dict[any, int]]) -> dict[any, np.array]:

    foundKeys: dict[any, list[int]] = {}
    for timestep, molecules in enumerate(dynamicDict):
        for speciesName, speciesCount in molecules.items():
            foundKeys[speciesName] = foundKeys.get(speciesName, [0]*timestep) + [speciesCount]

        notFoundMolecules = set(foundKeys.keys()) - set(molecules.keys())
        for notFoundMolecule in notFoundMolecules:
            foundKeys[notFoundMolecule].append(0)

    for molecule, occurrences in foundKeys.items():
        foundKeys[molecule] = np.array(occurrences, dtype=int)

    return foundKeys

def main(**argv):
    filePicked = fd.askopenfilenames(title='Select speciation to analyze', initialdir = config.pythonOutput)

    trajectory = FileSpeciation(filePicked[0])
    listOfDict = trajectory.plot()
    codomains = toCodomain(listOfDict)
    df = pd.DataFrame(codomains, dtype=float)
    df = df[df.iloc[0].sort_values(ascending=False).index]
    dfpercent = df.div(df.sum(axis=1), axis=0) * 100
    ax = dfpercent.plot.area()
    ax.set_xlim(0, len(listOfDict)-1)
    ax.set_ylim(0, 100)
    
    plt.show()

    selectedFiles = fd.askopenfilenames(title='Select XYZ files', initialdir=r'C:\Users\JL252842\Documents\Thesis\Data\Raw\Simulations\2024-11-22\AIMD-SCAN-AF')
    files=[]
    for xyzFile in selectedFiles:
        currentDirPath = "/".join(xyzFile.split("/")[:-1]) + f"/{xyzFile.split("/")[-1].split(".")[0]}.inp"
        cp2kFile = FileCP2Kinput(currentDirPath)
        trjFile = FileTrajectory(xyzFile, linkedCP2KFile=cp2kFile)
        files.append(trjFile.trajectory)
    
    app = InteractiveSpeciation(files)

if __name__ == "__main__":
    main()
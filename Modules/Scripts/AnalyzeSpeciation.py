import time
import tkinter as tk
from tkinter import filedialog as fd

import config
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from Classes.FileTypes.FileSpeciation import FileSpeciation


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

if __name__ == "__main__":
    main()
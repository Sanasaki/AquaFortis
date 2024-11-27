import time
from tkinter import filedialog as fd

import config
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from Classes.FileTypes import SpeciationFile


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
    filePicked = fd.askopenfilenames(title='Select speciation to analyze', initialdir=config.pythonOutput)

    # stringLineA: str = "1 {HNO3: 16, H2O: 76, H3NO4: 4}"
    # stringLineB: str = "2 {HNO3: 16, H2O: 76, H3NO4: 4}"
    # stringLineC: str = "3 {HNO3: 16, H2O: 76, H3NO4: 4}"
    # stringLineD: str = "114 {HNO3: 16, H2O: 75, H3NO4: 3, NO2: 1, H4O2: 1, HO: 1}"
    # stringLineE: str = "5 {HNO3: 14, H2O: 74, H3NO4: 6}"
    # stringLineF: str = "6 {HNO3: 13, H2O: 73, H3NO4: 7}"
    # stringLineG: str = "7 {HNO3: 11, H2O: 71, H3NO4: 9}"
    # stringLineH: str= "26 {HNO3: 13, H2O: 71, H3NO4: 7, H4O2: 1}"
    # stringLineI: str = "9 {HNO3: 9, H2O: 69, H3NO4: 11}"
    # stringLineJ: str = "114 {HNO3: 16, H2O: 75, H3NO4: 3, NO2: 1, H4O2: 1, HO: 1}"
    # speciationSample = [stringLineA, stringLineB, stringLineC, stringLineD, stringLineE, stringLineF, stringLineG, stringLineH, stringLineI, stringLineJ]

    # listOfDict = list(map(getSpecies, speciationSample))
    # speciationSample = r"C:\Users\JL252842\Documents\Thesis\Data\Processed\PythonOutput/x50N100-3-pos-1-speciation.txt"
    trajectory = SpeciationFile(filePicked[0])
    with open(speciationSample, 'r') as f:
        listOfDict: list[dict[str, int]] = list(map(getSpecies, f))
    codomains = toCodomain(listOfDict)
    df = pd.DataFrame(codomains, dtype=float)
    df = df[df.iloc[0].sort_values(ascending=False).index]
    # print(df)
    dfpercent = df.div(df.sum(axis=1), axis=0) * 100
    print(dfpercent)
    ax = dfpercent.plot.area()
    ax.set_xlim(0, len(listOfDict)-1)
    ax.set_ylim(0, 100)
    
    plt.show()
    
    # domain = np.linspace(0, len(listOfDict), len(listOfDict))
    # fig, ax = plt.figure()
    # # for codomain in codomains:
    # #     ax.plot(domain, codomains[codomain], label=codomain)
    
    # percent = codomains / codomains.sum(axis=0).astype(float) * 100
    # ax.stackplot(domain, percent)
    # ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    # ax.set_xlabel("Timestep")
    # ax.set_ylabel("Occurences")

    # plt.show()

if __name__ == "__main__":
    main()
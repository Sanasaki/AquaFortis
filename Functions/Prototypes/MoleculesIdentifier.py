import ctypes

import numpy as np
import pandas as pd
from chemistry.Atom import Atom
from chemistry.Molecule import Molecule
from FileTypes import AtomicCoordinatesXYZfile
from matplotlib import pyplot as plt

if __name__ == "__main__":
    xyzFile = AtomicCoordinatesXYZfile("C:/Users/JL252842/Documents/Thesis/Python/TestFiles/xyz/80HNO3-20H2O-1-pos-1-f4.xyz")
    systemSize: float = 18.1462749444
    df = xyzFile.buildDataframe()
    
    a = df.Element.to_numpy(dtype=str)
    x = df.x.to_numpy(dtype=float)
    # print(x)
    xb = np.where(x>systemSize/2, x-systemSize, x)
    xb = np.where(xb<-systemSize/2, xb+systemSize, xb)
    # print(x)
    y = df.y.to_numpy(dtype=float)
    yb = np.where(y>systemSize/2, y-systemSize, y)
    yb = np.where(yb<-systemSize/2, yb+systemSize, yb)
    z = df.z.to_numpy(dtype=float)
    zb = np.where(z>systemSize/2, z-systemSize, z)
    zb = np.where(zb<-systemSize/2, zb+systemSize, zb)

    # fileInNumpy = np.array((x,y,z))
    # print(fileInNumpy)

    print("\ndx\n")
    dx = abs(xb[:, None] - xb[None, :])
    print(dx)
    dx = np.where(dx>systemSize/2, systemSize-dx, dx)
    print(dx)
    dx = np.where(dx<-systemSize/2, dx+systemSize, dx)
    print(dx)

    print("\ndy\n")
    dy = abs(yb[:, None] - yb[None, :])
    print(dy)
    dy = np.where(dy>systemSize/2, systemSize-dy, dy)
    print(dy)
    dy = np.where(dy<-systemSize/2, dy+systemSize, dy)
    print(dy)

    print("\ndz\n")
    dz = abs(zb[:, None] - zb[None, :])
    print(dz)
    dz = np.where(dz>systemSize/2, systemSize-dz, dz)
    print(dz)
    dz = np.where(dz<-systemSize/2, dz+systemSize, dz)
    print(dz)

    Square = dx**2 + dy**2 + dz**2
    M = Square**(1/2)
    print(M)

    fig = plt.figure()
    df["Element"] = df["Element"].astype('string')
    df["x"] = pd.to_numeric(df["x"], errors='coerce')
    df["y"] = pd.to_numeric(df["y"], errors='coerce')
    df["z"] = pd.to_numeric(df["z"], errors='coerce')

    foundAtoms = [Atom(symbol=element, coordinates=[x, y, z]) for element, x, y, z in df.itertuples(index=False)]

    print(foundAtoms)
    print(df.dtypes)
    ax = fig.add_subplot(projection='3d')
    # for element, xcoord, ycoord, zcoord in df.itertuples(index=False):
        # xplot = df.iloc[grp_idx, 0]
        # ypd = df.iloc[grp_idx, 1]
        # zpd = df.iloc[grp_idx, 2]
    colors = {"H": "white", "N" : "blue", "O": "red"}
    df["Element"] = df["Element"].str.replace("H", "green")
    df["Element"] = df["Element"].str.replace("N", "blue")
    df["Element"] = df["Element"].str.replace("O", "red")
    ax.set_xlim([-systemSize/2, systemSize/2])
    ax.set_ylim([-systemSize/2, systemSize/2])
    ax.set_zlim([-systemSize/2, systemSize/2])
    ax.scatter3D(xb, yb, zb, c=df["Element"])

    # for i in range(len(xb)):
    #     ax.scatter3D(xb[i], yb[i], zb[i], marker='${}$'.format(i))

    # plt.show()

    cutoff: float = 1.5
    TruthNeighbors = np.where(M<cutoff,float(1),float(0))
    print(TruthNeighbors)
    TruthNeighbors[:] *= range(1, 461)
    print(TruthNeighbors)
    TruthNeighbors[TruthNeighbors==0]=['NaN']
    NeighList = np.nanmin(TruthNeighbors, axis=1).tolist()
    AtomIndexToAddress = {}
    for i,firstEncounteredIndex in enumerate(NeighList):
        currentAtomIndex = i+1
        if currentAtomIndex == firstEncounteredIndex:
            AtomIndexToAddress[currentAtomIndex] = id(firstEncounteredIndex)
        else:
            B = ctypes.cast(AtomIndexToAddress[int(firstEncounteredIndex)], ctypes.py_object).value
            A = AtomIndexToAddress[int(firstEncounteredIndex)]
            AtomIndexToAddress[currentAtomIndex] = A
            NeighList[i]= B


    # print(NeighList)
    # print(len(set(NeighList)))

    MolFoundID = {}
    MolFoundElement = {}
    for molecule in set(NeighList):
        MolFoundID[molecule] = []
        MolFoundElement[molecule] = []
        for i, atom in enumerate(NeighList):
            #convert to numpy again to use where func ? or truth indexing ?
            if atom == molecule:
                MolFoundID[molecule].append(i+1)
                MolFoundElement[molecule].append(a[i])

    print(MolFoundID)
    print(MolFoundElement)

    cleanMolecules = {}
    for firstAtom, molecule in MolFoundElement.items():
        moleculeStr = ''.join(molecule)
        cleanMolecules[firstAtom] = Molecule(moleculeStr)

    print(cleanMolecules)

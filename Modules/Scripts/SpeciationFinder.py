import concurrent.futures
from tkinter import filedialog as fd

from memory_profiler import profile

from Classes.FileTypes.CP2K import FileCP2Kinput
from Classes.FileTypes.FileXYZ import FileXYZ
from Functions.FxStaticFunctions import FxProcessTime


def writeFile(exportPath: str, speciations, name):
    path = exportPath + f'/{name}-speciation.txt'
    print("Writing:", name)
    with open(path, 'w') as outfile:
        # print(speciations)
        for i, item in enumerate(speciations):
            outfile.write(f"{i}")
            outfile.write(" {")
            numberOfMolecules = len(item.species.keys())
            j=0
            for key, value in item.species.items():
                j+=1
                if j != numberOfMolecules:
                    outfile.write(f"{key}: {len(value)}, ")
                else:
                    outfile.write(f"{key}: {len(value)}")
            outfile.write("}")
            outfile.write("\n")
            # outfile.write(f"{i} {item}\n")

@FxProcessTime
def indirectMethod(xyzFile):
    currentDirPath = "/".join(xyzFile.split("/")[:-1]) + f"/{xyzFile.split("/")[-1].split(".")[0]}.inp"
    cp2kFile = FileCP2Kinput(currentDirPath)
    atomicFile = FileXYZ(xyzFile, linkedCP2KFile=cp2kFile)
    print("Reading:", atomicFile.name)
    return atomicFile.getTimeSpeciation()

@profile
def main(**argv):
    selectedXyzFiles = fd.askopenfilenames(title='Select XYZ files', initialdir=r'C:\Users\JL252842\Documents\Thesis\Data\Raw\Simulations\2024-11-22\AIMD-SCAN-AF')

    exportPath: str = fd.askdirectory(title='Select export directory', initialdir=r"C:\Users\JL252842\Documents\Thesis\Data\Processed\PythonOutput")

    with concurrent.futures.ProcessPoolExecutor(max_workers=12) as multiProcess:
        dynamicSpeciations = multiProcess.map(indirectMethod, selectedXyzFiles)
    # dynamicSpeciations = map(indirectMethod, selectedXyzFiles)
        for xyzFilePath, data in zip(selectedXyzFiles, dynamicSpeciations):
            name = xyzFilePath.split("/")[-1].split(".")[0]
            Trajectory = data[0]
            writeFile(exportPath, data, name)

    # xyzFile = selectedXyzFiles[0]
    # currentDirPath = "/".join(xyzFile.split("/")[:-1]) + f"/{xyzFile.split("/")[-1].split(".")[0]}.inp"
    # cp2kFile = FileCP2Kinput(currentDirPath)
    # atomicFile = FileXYZ(xyzFile, linkedCP2KFile=cp2kFile)
    
    # for i in Trajectory.species:
    #     if i != "H2O":
    #         if i != "HNO3":
    #             mol = (Trajectory.species[i])[0]
    #             iAtoms = mol.atoms
    #             for atom in iAtoms:
    #                 print(atom.x, atom.y, atom.z)
    #             # mol.plot(18)
    #             # print()
    #             (Trajectory.species[i])[0].plot(atomicFile.atomicSystemSize)

    
if __name__ == "__main__":
    main()
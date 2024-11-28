import concurrent.futures
from tkinter import filedialog as fd

from Classes.FileTypes.CP2K import FileCP2Kinput
from Classes.FileTypes.FileXYZ import FileXYZ
from Functions.FxStaticFunctions import FxProcessTime
from memory_profiler import profile


def writeFile(exportPath: str, speciations, name):
    path = exportPath + f'/{name}-speciation.txt'
    print("Writing:", name)
    with open(path, 'w') as outfile:
        for i, item in enumerate(speciations):
            outfile.write(f"{i} {item}\n")

@FxProcessTime
def indirectMethod(xyzFile):
    currentDirPath = "/".join(xyzFile.split("/")[:-1]) + f"/{xyzFile.split("/")[-1].split(".")[0]}.inp"
    cp2kFile = FileCP2Kinput(currentDirPath)
    atomicFile = FileXYZ(xyzFile, linkedCP2KFile=cp2kFile)
    print("Reading:", atomicFile.name)
    return atomicFile.getTimeSpeciation('str')

@profile
def main(**argv):
    selectedXyzFiles = fd.askopenfilenames(title='Select XYZ files', initialdir=r'C:\Users\JL252842\Documents\Thesis\Data\Raw\Simulations\2024-11-22\AIMD-SCAN-AF')

    exportPath: str = fd.askdirectory(title='Select export directory', initialdir=r"C:\Users\JL252842\Documents\Thesis\Data\Processed\PythonOutput")

    with concurrent.futures.ProcessPoolExecutor(max_workers=12) as multiProcess:
        dynamicSpeciations = multiProcess.map(indirectMethod, selectedXyzFiles)
        for xyzFilePath, data in zip(selectedXyzFiles, dynamicSpeciations):
            name = xyzFilePath.split("/")[-1].split(".")[0]
            writeFile(exportPath, data, name)
    
    
if __name__ == "__main__":
    main()
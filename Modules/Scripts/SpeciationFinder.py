import concurrent.futures
from tkinter import filedialog as fd

from FileTypes import AtomicCoordinatesXYZfile, CP2Kfile


def writingFile(exportPath: str, speciations, name):
    path = exportPath + f'/{name}-speciation.txt'
    print("Writing:", name)
    with open(path, 'w')as outfile:
        # for item in dict(sorted(speciations.items())).items():
        for i, item in enumerate(speciations):
            outfile.write(f"{i} {item}\n")

def indirectGetSpeciation(xyzFile):
    currentDirPath = "/".join(xyzFile.split("/")[:-1]) + f"/{xyzFile.split("/")[-1].split(".")[0]}.inp"
    cp2kFile = CP2Kfile(currentDirPath)
    atomicFile = AtomicCoordinatesXYZfile(xyzFile, linkedCP2KFile=cp2kFile)
    print("Reading:", atomicFile.name)
    return atomicFile.getTimeSpeciation()

def main(**argv):
    xyzFilesToGetSpeciation = fd.askopenfilenames(title='Select XYZ files', initialdir=r'C:\Users\JL252842\Documents\Thesis\Data\Raw\Simulations\2024-11-22\AIMD-SCAN-AF')

    exportPath: str = fd.askdirectory(title='Select export directory', initialdir=r"C:\Users\JL252842\Documents\Thesis\Data\Processed\PythonOutput")

    with concurrent.futures.ProcessPoolExecutor(max_workers=12) as multiProcess:
        speciationsResults = multiProcess.map(indirectGetSpeciation, xyzFilesToGetSpeciation)
        for xyzFilePath, data in zip(xyzFilesToGetSpeciation, speciationsResults):
            name = xyzFilePath.split("/")[-1].split(".")[0]
            writingFile(exportPath, data, name)
    
    
if __name__ == "__main__":
    main()
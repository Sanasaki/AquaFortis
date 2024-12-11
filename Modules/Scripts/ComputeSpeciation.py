import concurrent.futures

from Chemistry.Molecule import Molecule
from Classes.AtomicSystem import AtomicSystem
from Classes.FileTypes.FileXYZ import FileTrajectory
from Classes.Speciation import Speciation
from Functions.FxDistanceMatrix import distanceMatrix
from Functions.FxInferMolecules import inferMolecules
from Functions.FxNeighborsMatrix import neighborsMatrix
from Functions.FxNeighborsPerAtom import neighborsPerAtom
from Functions.FxStaticFunctions import pickFiles


def computeSpeciation(file: str):
    xyzFile = FileTrajectory(filePath=file)
    trajectory = xyzFile.trajectory
    frames = trajectory.frames
    outputFile = file.replace(".xyz", "-spc.dat")

    def speciationYielder(frames: list["AtomicSystem"]):
        def speciation(molecules: list["Molecule"]) -> "Speciation":
            return Speciation.fromList(molecules)

        for i, frame in enumerate(frames):
            # print(i)
            _, x, y, z = frame.numpyArrays
            size = frame.size

            distanceMatrixArray = distanceMatrix(x, y, z, size)
            neighborsMatrixArray = neighborsMatrix(distanceMatrixArray)
            neighborsPerAtomDict = neighborsPerAtom(neighborsMatrixArray, frame.atoms)
            moleculesList = inferMolecules(neighborsPerAtomDict)
            yield str(i) + " " + str(speciation(moleculesList)) + "\n"

    speciationsStr = list(speciationYielder(frames))

    def write_speciation_results(outputFile: str, speciationsStr: list[str]) -> None:
        with open(outputFile, "w", newline="\n") as outfile:
            outfile.writelines(speciationsStr)

    write_speciation_results(outputFile, speciationsStr)
    return 0


if __name__ == "__main__":
    files = pickFiles()
    assert files != ""
    with concurrent.futures.ProcessPoolExecutor(max_workers=8) as multiprocess:
        multiprocess.map(computeSpeciation, files)

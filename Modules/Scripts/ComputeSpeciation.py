import concurrent.futures

from Chemistry.Molecule import Molecule
from FileTypes.FileXYZ import FileTrajectory
from Functions.FxDistanceMatrix import distanceMatrix
from Functions.FxInferMolecules import inferMolecules
from Functions.FxNeighborsPerAtom import neighborsPerAtom
from Functions.FxStaticFunctions import FxProcessTime, pickFiles
from Simulation.SimulationCell import SimulationCell
from Systems.AbstractSystem import System


@FxProcessTime
def computeSpeciation(file: str):
    xyzFile = FileTrajectory(filePath=file)
    trajectory = xyzFile.trajectory
    frames = trajectory.frames
    outputFile = file.replace(".xyz", "-spc.dat")

    def speciationYielder(frames: list["SimulationCell"]):
        for i, frame in enumerate(frames):
            # print(i)
            _, x, y, z = frame.data
            size = frame.cellSize

            distanceMatrixArray = distanceMatrix(x, y, z, size)
            neighborsPerAtomDict = neighborsPerAtom(
                distanceMatrixArray, frame.system.components
            )
            moleculesList = inferMolecules(neighborsPerAtomDict)
            yield (
                str(i)
                + " "
                + str(System[Molecule](moleculesList).asDict).replace("'", "")
                + "\n"
            )

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

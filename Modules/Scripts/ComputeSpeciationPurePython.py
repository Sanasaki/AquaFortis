import concurrent.futures

from FileTypes.FileXYZ import FileTrajectory
from Functions.FxStaticFunctions import pickFiles
from Scripts.ComputeSpeciation import FxProcessTime
from Simulation.SimulationCell import SimulationCell


def distanceMatrixPP(simulationCell: SimulationCell):
    for i, atom_i in enumerate(simulationCell.system):
        for j, atom_j in enumerate(simulationCell.system, i + 1):
            dx = atom_i.x - atom_j.x
            dy = atom_i.y - atom_j.y
            dz = atom_i.z - atom_j.z


@FxProcessTime
def computeSpeciationPP(file: str):
    xyzFile = FileTrajectory(filePath=file)
    trajectory = xyzFile.trajectoryPP
    frames = trajectory.frames
    outputFile = file.replace(".xyz", "-spc.dat")

    for frame in frames:
        distanceMatrixPP(frame)


if __name__ == "__main__":
    files = pickFiles()
    assert files != ""
    with concurrent.futures.ProcessPoolExecutor(max_workers=8) as multiprocess:
        multiprocess.map(computeSpeciationPP, files)

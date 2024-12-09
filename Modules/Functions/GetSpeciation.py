import globalConfigs
import numpy as np
import numpy.typing as npt
from Classes.AtomicSystem import AtomicSystem
from Classes.Chemistry.Atom import Atom
from Classes.Chemistry.Molecule import Molecule
from Classes.FileTypes.FileXYZ import FileTrajectory
from Classes.Speciation import Speciation
from Functions.FxStaticFunctions import pickAFile
from Scripts.SpeciationFinder import FxProcessTime


# @FxProcessTime
def distanceMatrix(
    x: npt.NDArray[np.float64],
    y: npt.NDArray[np.float64],
    z: npt.NDArray[np.float64],
    size: float,
) -> npt.NDArray[np.float64]:
    def matrixModulo(
        distanceArray: npt.NDArray[np.float64], atomicSystemSize: float
    ) -> npt.NDArray[np.float64]:
        distanceArray = np.where(
            distanceArray > (atomicSystemSize / 2),
            atomicSystemSize - distanceArray,
            distanceArray,
        )
        return distanceArray

    def getDistanceArray(array: npt.NDArray[np.float64]) -> npt.NDArray[np.float64]:
        return abs(array[:, None] - array[None, :])

    # _, x, y, z = self._numpyArrays

    dx = getDistanceArray(x)
    dx = matrixModulo(dx, size)

    dy = getDistanceArray(y)
    dy = matrixModulo(dy, size)

    dz = getDistanceArray(z)
    dz = matrixModulo(dz, size)

    return (dx**2 + dy**2 + dz**2) ** (1 / 2)


# @FxProcessTime
def neighborsMatrix(
    distanceMatrix: npt.NDArray[np.float64], isOneIndexed: bool = False
) -> npt.NDArray[np.float64]:
    neighborsMatrix = np.where(
        distanceMatrix < globalConfigs.cutOff, float(1), float(0)
    )
    neighborsMatrix[neighborsMatrix == 0] = ["NaN"]

    # Multiplying each col by its index, thus transforming 1 -> index
    neighborsMatrix[:] *= range(len(distanceMatrix[0]))

    if isOneIndexed is True:
        neighborsMatrix[:] += 1

    return neighborsMatrix


# @FxProcessTime
def neighborsPerAtom(
    neighborsMatrix: npt.NDArray[np.float64], atoms: list["Atom"]
) -> dict[Atom, list[Atom]]:
    # Zip function is very slow, so it should be replaced with a dict update here
    # neighbors = {}
    # this atom neighbor = {i : self.atoms[int(j)]}
    # neighbors.update(this atom neighbor)
    neighbors: list[list[Atom]] = []

    for i in range(len(neighborsMatrix)):
        listOfIndex = (
            (neighborsMatrix[i, :])[~np.isnan(neighborsMatrix[i, :])]
        ).tolist()
        iNeighbors: list[Atom] = []
        for j in listOfIndex:
            iNeighbors.append(atoms[int(j)])
        neighbors.append(iNeighbors)

    return {atom: neighbors for atom, neighbors in zip(atoms, neighbors)}


# @FxProcessTime
def molecules(neighborsPerAtom: dict[Atom, list[Atom]]) -> list["Molecule"]:
    molecules: list[Molecule] = []

    def parseNeighbors(parsedAtoms: dict[Atom, bool], atom: Atom) -> None:
        if not parsedAtoms.get(atom, False):
            parsedAtoms[atom] = True
            for neighborAtom in neighborsPerAtom[atom]:
                parseNeighbors(parsedAtoms, neighborAtom)

    totalParsedAtoms: dict[Atom, bool] = {}

    for atom in neighborsPerAtom.keys():
        if not totalParsedAtoms.get(atom, False):
            newMoleculeAtoms: dict[Atom, bool] = {}
            parseNeighbors(newMoleculeAtoms, atom)
            totalParsedAtoms.update(newMoleculeAtoms)
            # is this one-liner understandable?
            molecules.append(Molecule([atom for atom in newMoleculeAtoms.keys()]))

    return molecules


# @FxProcessTime
def speciation(molecules: list["Molecule"]) -> "Speciation":
    return Speciation.fromList(molecules)


@FxProcessTime
def main() -> None:
    filePath = pickAFile()
    assert filePath != ""
    xyzFile = FileTrajectory(filePath=filePath)
    trajectory = xyzFile.trajectory
    frames = trajectory.frames
    outputFile = filePath.replace(".xyz", ".dat")

    @FxProcessTime
    def speciationIterator(frames: list["AtomicSystem"]):
        for i, frame in enumerate(frames):
            # print(i)
            _, x, y, z = frame.numpyArrays
            size = frame.size

            distanceMatrixArray = distanceMatrix(x, y, z, size)
            neighborsMatrixArray = neighborsMatrix(distanceMatrixArray)
            neighborsPerAtomDict = neighborsPerAtom(neighborsMatrixArray, frame.atoms)
            moleculesList = molecules(neighborsPerAtomDict)
            yield str(i) + " " + str(speciation(moleculesList)) + "\n"

    speciationsStr = list(speciationIterator(frames))

    write_speciation_results(outputFile, speciationsStr)


@FxProcessTime
def write_speciation_results(outputFile: str, speciationsStr: list[str]) -> None:
    with open(outputFile, "w", newline="\n") as outfile:
        # outfile.writelines(f"{i} {speciationObj}\n")
        # print(speciationsStr)
        outfile.writelines(speciationsStr)

        # atoms = frame.atoms
        # x, y, z = atoms.x, atoms.y, atoms.z
        # size = frame.size
        # distanceMatrixArray = distanceMatrix(x, y, z, size)
        # neighborsMatrixArray = neighborsMatrix(distanceMatrixArray)
        # neighborsPerAtomDict = neighborsPerAtom(neighborsMatrixArray, atoms)
        # moleculesList = molecules(neighborsPerAtomDict)
        # speciationObj = speciation(moleculesList)
        # print(speciationObj)


if __name__ == "__main__":
    main()

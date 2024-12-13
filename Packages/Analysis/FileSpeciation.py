from collections.abc import Iterable

from Classes.File import File


class FileSpeciation(File):
    def __init__(
        self,
        filePath: str,
        speciesPerStep: list[str] = None,
    ):
        super().__init__(filePath)

        if speciesPerStep is not None:
            self.speciesPerStep = speciesPerStep
            self.steps = len(speciesPerStep)

    def write(self) -> None:
        with open(self.filePath, "w", newline="\n") as file:
            for step, item in enumerate(self.speciesPerStep):
                file.write(f"{step} {item}\n")

    def readlines(self) -> Iterable[str]:
        with open(self.filePath, "r") as file:
            return file.readlines()

    def plot(self):
        def getSpecies(speciationLine: str) -> dict[str, int]:
            # 4 {HNO3: 16, H2O: 76, H3NO4: 4}
            speciesLine: str = (speciationLine.split("{")[-1]).split("}")[0]
            moleculeFound: dict[str, int] = {}
            for species in speciesLine.split(","):
                molFoundInLine: dict[str, int] = {}
                speciesName, speciesCount = species.strip().split(":")
                molFoundInLine[str(speciesName)] = int(speciesCount)
                moleculeFound.update(molFoundInLine)
            return moleculeFound

        listOfDict: list[dict[str, int]] = list(map(getSpecies, self.readlines()))
        return listOfDict
        # timeSpeciation: list[dict[str, int]] = map(getSpecies, self.speciesPerStep)

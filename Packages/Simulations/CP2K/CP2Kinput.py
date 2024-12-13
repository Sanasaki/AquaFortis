import json
from dataclasses import dataclass, field
from typing import Any

from Classes.File import File

import globalConfigs
from Packages.Analysis.FileXYZ import FileTrajectory
from Packages.Chemistry.Atom import Atom


@dataclass(slots=True)
class CP2K:
    data: dict[str, Any] = field(default_factory=dict)

    # def __init__(self, data: dict[str, Any] = None) -> None:
    #     self.data = data or {}

    def setSystem(self, atoms: list[Atom] = None) -> None:
        self.data["FORCE_EVAL.SUBSYS.COORD"] = atoms

    def __setitem__(self, key: str, value: Any) -> None:
        keys: list[str] = key.split(".")
        tempDict = self.data
        for childKey in keys[:-1]:
            tempDict = tempDict.setdefault(childKey, {})
        tempDict[keys[-1]] = value

    def __getitem__(self, key: str) -> dict[str, Any]:
        keys = key.split(".")
        d = self.data
        for k in keys:
            d = d[k]
        return d

    @classmethod
    def readJSON(cls, jsonCP2Kfile: str) -> "CP2K":
        with open(jsonCP2Kfile, "r") as f:
            data: dict[str, Any | str] = json.load(f)
        return cls(data)

    def writeInput(self, filePath: str) -> "FileCP2K":
        with open(filePath, "w") as f:

            def write_recursive(dataDict: dict[str, Any], indent: int = 0):
                try:
                    for key, value in dataDict.items():
                        f.write(f"{' '*indent}")
                        if type(value) is dict[Any, Any]:
                            f.write(f"&{key}\n")
                            write_recursive(value, indent + 4)
                            f.write(f"{' '*indent}")
                            f.write(f"&END {key}")
                        elif type(value) is list[Any]:
                            f.write(f"{key}\t")
                            f.write(
                                "\t".join(
                                    [f"{float(listItem):.10f}" for listItem in value]
                                )
                            )
                        else:
                            f.write(f"{key}\t{value}")
                        f.write("\n")
                except AttributeError:
                    pass

            write_recursive(self.data)
        return FileCP2K(filePath)

    def writeJSON(self, filePath: str) -> File:
        with open(filePath, "w") as f:
            json.dump(self.data, f, indent=4)
        return File(filePath)


class FileCP2K(File):
    def __init__(self, filePath: str) -> None:
        super().__init__(filePath)


def main():
    xyzFile = FileTrajectory(
        globalConfigs.testFilesDirPath + "/xyz/80HNO3-20H2O-1-pos-1-f4.xyz"
    )
    simulationCell = xyzFile.trajectory.frames[0]

    cp2k = CP2K.readJSON("cp2k_input.json")

    cp2k["FORCE_EVAL.SUBSYS.CELL.ABC"] = [simulationCell.size] * 3
    cp2k["FORCE_EVAL.SUBSYS.COORD"] = {
        atom: [atom.x, atom.y, atom.z] for atom in simulationCell.system
    }

    CP2K.writeInput(cp2k, "cp2k_input_copy.inp")


if __name__ == "__main__":
    main()

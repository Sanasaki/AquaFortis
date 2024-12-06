import json

import globalConfigs
from Classes.AtomicSystem import AtomicSystem
from Classes.Chemistry.Atom import Atom
from Classes.FileTypes.File import File
from Classes.FileTypes.FileXYZ import FileTrajectory


class CP2K:
    __slots__ = ["data"]
    def __init__(self, data = None) -> None:
        self.data = data or {}

    def setSystem(self, atoms: list[Atom]=None) -> None:
        self.data["FORCE_EVAL.SUBSYS.COORD"] = atoms

    def __setitem__(self, key, value) -> None:
        keys = key.split('.')
        tempDict = self.data
        for childKey in keys[:-1]:
            tempDict = tempDict.setdefault(childKey, {})
        tempDict[keys[-1]] = value

    def __getitem__(self, key) -> dict:
        keys = key.split('.')
        d = self.data
        for k in keys:
            d = d[k]
        return d
    
    @classmethod
    def readJSON(cls, jsonCP2Kfile: File) -> "CP2K":
        with open(jsonCP2Kfile, 'r') as f:
            data = json.load(f)
        return cls(data)
    
    def writeInput(self, filePath) -> "FileCP2K":
        with open(filePath, 'w') as f:
            def write_recursive(d, indent=0):
                try:
                    for key, value in d.items():
                        f.write(f"{' '*indent}")
                        if isinstance(value, dict):
                            f.write(f"&{key}\n")
                            write_recursive(value, indent+4)
                            f.write(f"{' '*indent}")
                            f.write(f"&END {key}")
                        elif isinstance(value, list):
                            f.write(f"{key}\t")
                            f.write(f"\t".join([f"{float(listItem):.10f}" for listItem in value]))
                        else:
                            f.write(f"{key}\t{value}")
                        f.write(f"\n")
                except AttributeError:
                    pass

            write_recursive(self.data)
        return FileCP2K(filePath)

    def writeJSON(self, filePath: str) -> File:
        with open(filePath, 'w') as f:
            json.dump(self.data, f, indent=4)
        return File(filePath)
class FileCP2K(File):
    def __init__(self, filePath:str) -> None:
        super().__init__(filePath)


def main():
    xyzFile = FileTrajectory(globalConfigs.testFilesDirPath + "/xyz/80HNO3-20H2O-1-pos-1-f4.xyz")
    atomicSystem = xyzFile.trajectory.frames[0]

    cp2k = CP2K.readJSON("cp2k_input.json")

    cp2k["FORCE_EVAL.SUBSYS.CELL.ABC"] = [atomicSystem.size]*3
    cp2k["FORCE_EVAL.SUBSYS.COORD"] = {atom: [atom.x, atom.y, atom.z] for atom in atomicSystem}

    CP2K.writeInput(cp2k, "cp2k_input_copy.inp")

if __name__ == "__main__":
    main()
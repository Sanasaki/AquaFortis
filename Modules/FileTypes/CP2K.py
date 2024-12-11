from FileTypes.File import File


class FileCP2Kinput(File):
    __slots__ = ["cp2kSystemSize", "cp2kAtomCount"]

    def __init__(self, filePath: str):
        super().__init__(filePath)

        with open(self.filePath, "r") as f:
            for line in f:
                if "ABC" in line:
                    self.cp2kSystemSize = float(line.split()[-1])
                atomCount: int = 0
                if "&COORD" in line:
                    next(f)
                    while "&END COORD" not in line:
                        atomCount += 1
                        line = next(f)
                    self.cp2kAtomCount = atomCount
                    break

    def __repr__(self):
        return f"CP2K file: {self.name}"

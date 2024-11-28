from Classes.FileTypes.File import File


class FileCP2Kinput(File):
    __slots__ = ["cp2kSystemSize"]
    def __init__(
            self, 
            filePath: str
            ):
        super().__init__(filePath)

        with open(self.filePath, 'r') as f:
            for line in f:
                if "ABC" in line:
                    self.cp2kSystemSize = float(line.split()[-1])

    def __repr__(self):
        return f"CP2K file: {self.name}"
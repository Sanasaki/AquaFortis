from Classes.FileTypes.File import File


class FileMoleculeLMP(File):
    def __init__(self, filePath: str) -> None:
        super().__init__(filePath)
        self.molecule: str = self.name

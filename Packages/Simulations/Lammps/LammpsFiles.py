from Classes.File import File


class LammpsMoleculeFile(File):
    def __init__(self, filePath: str) -> None:
        super().__init__(filePath)
        self.molecule: str = self.name


class LammpsInputFile(File):
    def __init__(self, filePath: str) -> None:
        super().__init__(filePath)


class LammpsPotentialFile(File):
    def __init__(self, filePath: str) -> None:
        super().__init__(filePath)

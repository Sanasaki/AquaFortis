periodicTable: dict[str, dict[str, float | int]] = {
    "H": {"atomicWeight": 1.0080, "atomicNumber": 1},
    "He": {"atomicWeight": 4.00260, "atomicNumber": 2},
    "Li": {"atomicWeight": 7.0, "atomicNumber": 3},
    "Be": {"atomicWeight": 9.012183, "atomicNumber": 4},
    "B": {"atomicWeight": 10.81, "atomicNumber": 5},
    "C": {"atomicWeight": 12.011, "atomicNumber": 6},
    "N": {"atomicWeight": 14.007, "atomicNumber": 7},
    "O": {"atomicWeight": 15.999, "atomicNumber": 8},
}


STATS_ENSEMBLE = {
    "NVT": ("amount", "size", "temperature"),
    "NPT": ("amount", "pressure", "temperature"),
}


colorAtom: dict[str, str] = {"H": "green", "N": "blue", "O": "red"}

cutOff: float = 1.577

rootPath: str = r"C:\Users\JL252842\Documents\Thesis\Python"
testFilesDirPath: str = rootPath + r"\TestFiles"
testDataPath: str = rootPath + r"\Tests\TestData"

pythonOutputPath: str = (
    r"C:\Users\JL252842\Documents\Thesis\Data\Processed\PythonOutput"
)

moleculesPath: str = r"C:\Users\JL252842\Documents\Thesis\Lab\ReferenceData\Molecules"

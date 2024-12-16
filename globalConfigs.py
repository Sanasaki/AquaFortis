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

ROOT_PYTHON_PATH: str = r"C:\Users\JL252842\Documents\Thesis\Python"
TEST_FILES_PATH: str = ROOT_PYTHON_PATH + r"\TestFiles"
TEST_DATA_PATH: str = ROOT_PYTHON_PATH + r"\Tests\TestData"

LAB_PATH: str = r"C:\Users\JL252842\Documents\Thesis\Lab"
MOLECULES_PATH: str = LAB_PATH + r"\ReferenceData\Molecules"

DATA_PATH: str = r"C:\Users\JL252842\Documents\Thesis\Data"
PYTHON_OUTPUT_PATH: str = DATA_PATH + r"\Processed\PythonOutput"

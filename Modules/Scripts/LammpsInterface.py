from dataclasses import dataclass

import globalConfigs


@dataclass(slots=True)
class LammpsFix:
    name: str
    style: str
    group: str = 'all'

def atomicSystemDesigner() -> 'AtomicSystem':
    return


def atomicSystemPicker() -> 'AtomicSystem':
    return



def main():
    name: str = "teeeee"


    atomicSystemPicker()
    exportPath = globalConfigs.testFilesDirPath + f"/cp2k/{name}"

    pass

















if __name__ == "__main__":
    main()
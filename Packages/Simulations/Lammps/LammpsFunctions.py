from typing import Any


def writeFixNVT(
    runTime: int,
    temperature: float,
    fixName: str = "nvtFix",
    fixedAtoms: str = "all",
    thermoTimestep: int = 200,
) -> str:
    return f"""fix {fixName} {fixedAtoms} nvt/rigid/small molecule temp {temperature} {temperature} {thermoTimestep}
    run {runTime}
    unfix {fixName}
"""


def writeFixNPT(
    runTime: int,
    temperature: float,
    pressure: float,
    fixName: str = "nptFix",
    fixedAtoms: str = "all",
    thermoTimestep: int = 200,
    baroTimestep: int = 1000,
) -> str:
    return f"""fix {fixName} {fixedAtoms} npt/rigid/small molecule temp {temperature} {temperature} {thermoTimestep} iso {pressure} {pressure} {baroTimestep}
    run {runTime}
    unfix {fixName}
"""


def writeKeyword(keyword: Any, value: Any) -> str:
    return f"{keyword} {value}\n"


def writeRegion(
    regionName: str = "system",
    regionType: str = "block",
    regionSize: float = 40.0,
) -> str:
    return f"region {regionName} {regionType} -{regionSize/2} {regionSize/2} -{regionSize/2} {regionSize/2} -{regionSize/2} {regionSize/2}\n"


def writeForcefield(
    atomStyle: str = "full",
    pairStyle: str = "lj/cut/coul/wolf 0.2 10",
    bondStyle: str = "zero",
    angleStyle: str = "zero",
    dihedralStyle: str = "none",
    improperStyle: str = "none",
) -> str:
    return f"""atom_style {atomStyle}
    pair_style {pairStyle}
    bond_style {bondStyle}
    angle_style {angleStyle}
    dihedral_style {dihedralStyle}
    improper_style {improperStyle}"""


def writeMolecule(
    moleculeName: str,
    moleculeAmount: int,
    regionName: str,
    overlap: float,
    rngSeed1: int,
    rngSeed2: int,
) -> str:
    return f"create_atoms 0 random {moleculeAmount} {rngSeed1} {regionName} mol {moleculeName} {rngSeed2} overlap {overlap}\n"


def writeThermoStyle(
    columns: list[str],
    style: str = "custom",
) -> str:
    return f"thermo_style {style} {' '.join(columns)}\n"


def setVariable(
    variableName: str,
    value: Any,
) -> str:
    return f"variable {variableName} equal {value}\n"


def writeMultilineBlock(
    firstLineKeyword: str,
    firstLineValue: str,
    multilineKeyValues: dict[Any, Any],
    optionalPrefix: str = "\t",
):
    if firstLineValue == "":
        multiline = f"{firstLineKeyword} &\n"
    else:
        multiline = f"{firstLineKeyword} {firstLineValue} &\n"
    for key, value in multilineKeyValues.items():
        multiline += f"{optionalPrefix}{key} {value} &\n"
    return multiline[:-3] + "\n"


def writeCreateBox(
    regionName: str,
    atomTypes: int,
    bondTypes: int,
    angleTypes: int,
    dihedralTypes: int,
    improperTypes: int,
    extraBondPerAtom: int,
    extraAnglePerAtom: int,
    extraSpecialPerAtom: int,
    extraDihedralPerAtom: int,
    extraImproperPerAtom: int,
    optionalPrefix: str = "",
) -> str:
    firstLineValue = f"{atomTypes} {regionName}"
    multiLineDict = {
        "atom/types": atomTypes,
        "bond/types": bondTypes,
        "angle/types": angleTypes,
        "dihedral/types": dihedralTypes,
        "improper/types": improperTypes,
        "extra/bond/per/atom": extraBondPerAtom,
        "extra/angle/per/atom": extraAnglePerAtom,
        "extra/special/per/atom": extraSpecialPerAtom,
        "extra/dihedral/per/atom": extraDihedralPerAtom,
        "extra/improper/per/atom": extraImproperPerAtom,
    }
    return writeMultilineBlock(
        firstLineKeyword="create_box",
        firstLineValue=firstLineValue,
        multilineKeyValues=multiLineDict,
        optionalPrefix=optionalPrefix,
    )


def writeFixData(
    nEvery: int,
    nRepeat: int,
    nFreq: int,
    keywordsLabels: dict[str, str],
    dataFile: str,
    fixName: str = "fixData",
    fixedAtoms: str = "all",
) -> str:
    return f"""fix {fixName} {fixedAtoms} ave/time {nEvery} {nRepeat} {nFreq} &
    {" ".join(keywordsLabels.keys())} &
    file {dataFile} &
    title1 Timestep {" ".join(keywordsLabels.values())}"""


def writeDump(
    nEvery: int,
    nRepeat: int,
    nFreq: int,
    dumpName: str,
    dumpType: str,
    dumpFile: str,
    dumpAtoms: str = "all",
) -> str:
    return f"""dump {dumpName} {dumpAtoms} {dumpType} {nEvery} &
    {dumpFile}"""


def writeDumpModify(
    dumpName: str,
    editedAttribute: str,
    editedValue: str,
) -> str:
    return f"""dump_modify {dumpName} {editedAttribute} {editedValue}"""


labelAtomDict = {
    1: "H[Nitric]",
    2: "N[Nitric]",
    3: "O1[Nitric]",
    4: "O2[Nitric]",
    5: "O[Water]",
    6: "H[Water]",
    7: "N[Nitrate]",
    8: "O[Nitrate]",
    9: "H[Hydronium]",
    10: "O[Hydronium]",
}

columns = ["step", "temp", "press", "pe", "ke", "etotal", "vol", "density"]
colLabel = {
    1: "Timestep",
    2: "Temperature",
    3: "Pressure",
    4: "Potential Energy",
    5: "Kinetic Energy",
    6: "Total Energy",
    7: "Volume",
    8: "Density",
}

memoryAllocation = {
    "atom/types": 10,
    "bond/types": 5,
    "angle/types": 0,
    "dihedral/types": 3,
    "improper/types": 0,
    "extra/bond/per/atom": 0,
    "extra/angle/per/atom": 0,
    "extra/special/per/atom": 0,
    "extra/dihedral/per/atom": 0,
    "extra/improper/per/atom": 0,
}
if __name__ == "__main__":
    print(
        writeCreateBox(
            regionName="system",
            atomTypes=memoryAllocation["atom/types"],
            bondTypes=memoryAllocation["bond/types"],
            angleTypes=memoryAllocation["angle/types"],
            dihedralTypes=memoryAllocation["dihedral/types"],
            improperTypes=memoryAllocation["improper/types"],
            extraBondPerAtom=memoryAllocation["extra/bond/per/atom"],
            extraAnglePerAtom=memoryAllocation["extra/angle/per/atom"],
            extraSpecialPerAtom=memoryAllocation["extra/special/per/atom"],
            extraDihedralPerAtom=memoryAllocation["extra/dihedral/per/atom"],
            extraImproperPerAtom=memoryAllocation["extra/improper/per/atom"],
        )
    )

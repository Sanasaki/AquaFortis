from dataclasses import dataclass


@dataclass
class LammpsMolecule:
    chemicalFormula: str = ""
    amount: int = 0
    atoms: int = 0
    bonds: int = 0
    angles: int = 0
    dihedrals: int = 0
    impropers: int = 0
    extraBonds: int = 0
    extraAngles: int = 0
    extraSpecials: int = 0
    extraDihedrals: int = 0
    extraImpropers: int = 0

    def __call__(self, chemicalFormula: str, amount: int):
        match chemicalFormula:
            case "HNO3":
                return Nitric(amount)
            case "H2O":
                return Water(amount)
            case "NO3":
                return Nitrate(amount)
            case "H3O":
                return Hydronium(amount)
            case _:
                raise ValueError(f"Unknown chemical formula: {chemicalFormula}")


class Nitric(LammpsMolecule):
    def __init__(self, amount: int):
        self.chemicalFormula = "HNO3"
        self.amount = amount
        self.atoms = 4
        self.bonds = 2
        self.angles = 4
        self.dihedrals = 1
        self.impropers = 1
        self.extraBonds = 2
        self.extraAngles = 2
        self.extraSpecials = 0
        self.extraDihedrals = 1
        self.extraImpropers = 1


class Water(LammpsMolecule):
    def __init__(self, amount: int):
        self.chemicalFormula = "H2O"
        self.amount = amount
        self.atoms = 2
        self.bonds = 1
        self.angles = 1
        self.dihedrals = 0
        self.impropers = 0
        self.extraBonds = 1
        self.extraAngles = 1
        self.extraSpecials = 3
        self.extraDihedrals = 0
        self.extraImpropers = 0


class Nitrate(LammpsMolecule):
    def __init__(self, amount: int):
        self.chemicalFormula = "NO3"
        self.amount = amount
        self.atoms = 2
        self.bonds = 1
        self.angles = 1
        self.dihedrals = 0
        self.impropers = 0
        self.extraBonds = 0
        self.extraAngles = 0
        self.extraSpecials = 0
        self.extraDihedrals = 0
        self.extraImpropers = 0


class Hydronium(LammpsMolecule):
    def __init__(self, amount: int):
        self.chemicalFormula = "H3O"
        self.amount = amount
        self.atoms = 2
        self.bonds = 1
        self.angles = 1
        self.dihedrals = 0
        self.impropers = 0
        self.extraBonds = 0
        self.extraAngles = 0
        self.extraSpecials = 0
        self.extraDihedrals = 0
        self.extraImpropers = 0


HNO3 = """
# Nitric acid

5 atoms
4 bonds
4 angles
1 dihedrals
1 impropers

Coords

1 0 0 0
2 0 0 1.211
3 -1.0047 0 -0.654338
4 1.178167 0 -0.767305
5 1.928129 0 -0.161621

Types

1 N[Nitric]
2 O1[Nitric]
3 O1[Nitric]
4 O2[Nitric]
5 H[Nitric]

Molecules

1 1
2 1
3 1
4 1
5 1

Charges

1 0.964
2 -0.445
3 -0.445
4 -0.571
5 0.497

Bonds

1 NO[Nitric] 1 2
2 NO[Nitric] 1 3
3 NO[Nitric] 1 4
4 OH[Nitric] 4 5

Angles

1 ONO_1[Nitric] 2 1 3
2 ONO_2[Nitric] 3 1 4
3 ONO_3[Nitric] 4 1 2
4 NOH[Nitric]   5 4 1

Dihedrals

1 1 2 1 4 5

Impropers

1 1 1 3 4 2
"""

H2O = """
# Water molecule. SPC/E geometry

3 atoms
2 bonds
1 angles

Coords

1    0.00000  -0.06461   0.00000
2    0.81649   0.51275   0.00000
3   -0.81649   0.51275   0.00000

Types

1 O[Water]
2 H[Water]
3 H[Water]

Charges

1       -0.8476
2        0.4238
3        0.4238

Bonds

1 OH[Water] 1 2
2 OH[Water] 1 3

Angles

1 HOH[Water] 3 1 2

Shake Flags

1 1
2 1
3 1

Shake Atoms

1 1 2 3
2 1 2 3
3 1 2 3

Shake Bond Types

1 1 1 1
2 1 1 1
3 1 1 1

Special Bond Counts

1 2 0 0
2 1 1 0
3 1 1 0

Special Bonds

1 2 3
2 1 3
3 1 2
"""

NO3 = """
# Ion nitrate NO3-

4 atoms
3 bonds
3 angles

Coords

1       0       0       0
2       0       1.313   0
3       -1.137 -0.657  0
4       1.137  -0.657  0

Types

1   N[Nitrate]
2   O[Nitrate]
3   O[Nitrate]
4   O[Nitrate]

Molecules

1   1
2   1
3   1
4   1

Charges

1   0.65
2   -0.55
3   -0.55
4   -0.55

Bonds

1   NO[Nitrate] 1 2
2   NO[Nitrate] 1 3
3   NO[Nitrate] 1 4

Angles

1   ONO[Nitrate] 2 1 3
2   ONO[Nitrate] 3 1 4
3   ONO[Nitrate] 4 1 2
"""

H3O = """
# Ion hydronium H3O+

4 atoms
3 bonds
3 angles

Coords

1       0       0       0
2       0       0.976   -0.09
3       -0.845  -0.488  -0.09
4       0.845   -0.488  -0.09

Types

1   O[Hydronium]
2   H[Hydronium]
3   H[Hydronium]
4   H[Hydronium]

Molecules

1   1
2   1
3   1
4   1

Charges

1   -0.734
2   0.578
3   0.578
4   0.578

Bonds

1   OH[Hydronium] 1 2
2   OH[Hydronium] 1 3
3   OH[Hydronium] 1 4

Angles

1   HOH[Hydronium] 2 1 3
2   HOH[Hydronium] 3 1 4
3   HOH[Hydronium] 4 1 2
"""

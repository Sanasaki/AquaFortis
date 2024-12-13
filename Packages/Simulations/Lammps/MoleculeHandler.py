from Packages.Simulations.Lammps.LammpsUnits import LammpsScriptUnit


class MoleculeHandler(LammpsScriptUnit):
    def build(self) -> str:
        moleculeContent: str = "# Molecules\n"
        for lammpsMolecule in self.context.molecules:
            moleculeContent += self.includeMolecule(lammpsMolecule.chemicalFormula)
            moleculeContent += self.placeMolecule(
                lammpsMolecule.chemicalFormula, lammpsMolecule.amount
            )
            moleculeContent += "\n"
        return moleculeContent

    def includeMolecule(self, moleculeName: str):
        return f"molecule {moleculeName} ./{self.context.paths["input"]}/molecules/{moleculeName}.lmp\n"

    def placeMolecule(
        self,
        moleculeName: str,
        moleculeCount: int,
    ):
        return f"create_atoms 0 random {moleculeCount} {self.context.rng} {self.context.regionName} mol {moleculeName} {self.context.rng} overlap {self.context.overlap}\n"

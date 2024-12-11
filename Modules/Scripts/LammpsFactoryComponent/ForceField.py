from dataclasses import dataclass

from Scripts.LammpsFactoryComponent.LammpsScriptComponent import LammpsScriptComponent


@dataclass
class LammpsForceField(LammpsScriptComponent):
    atom_style: str
    pair_style: str
    bond_style: str
    angle_style: str
    dihedral_style: str
    improper_style: str

    # def write(self) -> str:
    #     forceFieldContent: str = f"atom_style\t{self.atom_style}\n"
    #     forceFieldContent += f"pair_style\t{self.pair_style}\n"
    #     forceFieldContent += f"bond_style\t{self.bond_style}\n"
    #     forceFieldContent += f"angle_style\t{self.angle_style}\n"
    #     forceFieldContent += f"dihedral_style\t{self.dihedral_style}\n"
    #     forceFieldContent += f"improper_style\t{self.improper_style}\n"
    #     return forceFieldContent


@dataclass
class LennardJonesCoul(LammpsForceField):
    atom_style: str = "full"
    pair_style: str = "lj/cut/coul/wolf 0.2 10"
    bond_style: str = "zero"
    angle_style: str = "zero"
    dihedral_style: str = "none"
    improper_style: str = "none"

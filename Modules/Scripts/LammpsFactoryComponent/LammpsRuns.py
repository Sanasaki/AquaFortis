from dataclasses import dataclass

from Scripts.LammpsFactoryComponent.LammpsScriptComponent import LammpsScriptComponent


@dataclass
class LammpsRuns(LammpsScriptComponent):
    boundary: str
    name: str
    size: float

    def write(self, append: str = "", indent: int = 0) -> str:
        # super().write(indent)
        content: str = ""
        content += f"{'\t'*indent}"
        content += f"boundary\t{self.boundary}\n"

        content += f"{'\t'*indent}"
        content += f"region\t{self.name}\tblock"

        xlo: float = -self.size / 2
        xhi: float = self.size / 2
        ylo: float = -self.size / 2
        yhi: float = self.size / 2
        zlo: float = -self.size / 2
        zhi: float = self.size / 2
        content += f"\t{xlo} {xhi} {ylo} {yhi} {zlo} {zhi}\n"
        return content

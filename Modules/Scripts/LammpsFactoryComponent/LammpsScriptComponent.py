from abc import ABC
from dataclasses import dataclass


@dataclass
class LammpsScriptComponent(ABC):
    def write(self, append: str = "", indent: int = 0) -> str:
        content: str = ""
        for key, value in vars(self).items():
            content += f"{'\t'*indent}"
            content += f"{key}\t{value}{append}\n"

        return content

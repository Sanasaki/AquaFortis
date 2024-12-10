from dataclasses import dataclass

from Scripts.LammpsFactoryComponent.LammpsScriptComponent import LammpsScriptComponent


@dataclass
class LammpsInit(LammpsScriptComponent):
    # jobName: str
    timestep: float
    units: str
    thermo: int


@dataclass
class DefaultInit(LammpsInit):
    # jobName: str = "AF"
    timestep: float = 0.5
    units: str = "real"
    thermo: int = 1000

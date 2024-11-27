
from abc import ABC
from dataclasses import dataclass


@dataclass(slots=True)
class Vector(ABC):
    x: float
    y: float
    z: float
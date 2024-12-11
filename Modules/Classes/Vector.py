from abc import ABC
from typing import Self


class Vector(ABC):
    __slots__ = "x", "y", "z", "label"

    def __init__(
        self, x: float = 0.0, y: float = 0.0, z: float = 0.0, label: str = ""
    ) -> None:
        self.x: float = x
        self.y: float = y
        self.z: float = z
        self.label: str = label

    def __add__(self, other: Self) -> "Vector":
        return Vector(x=self.x + other.x, y=self.y + other.y, z=self.z + other.z)

    def __sub__(self: Self, other: Self) -> "Vector":
        return Vector(x=self.x - other.x, y=self.y - other.y, z=self.z - other.z)

    def setOrigin(self, other: Self) -> None:
        self.x -= other.x
        self.y -= other.y
        self.z -= other.z

    @property
    def magnitude(self) -> float:
        return (self.x**2 + self.y**2 + self.z**2) ** 0.5

    # def __repr__(self):
    #     return f"Vector({self.x}, {self.y}, {self.z})"

    @property
    def position(self):
        return (self.x, self.y, self.z)

    @position.setter
    def position(self, newVector: "Vector"):
        self.x, self.y, self.z = newVector.position

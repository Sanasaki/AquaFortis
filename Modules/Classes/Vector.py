
from abc import ABC
from dataclasses import dataclass


@dataclass(slots=True)
class Vector(ABC):
    x: float = 0
    y: float = 0
    z: float = 0

    def __add__(self, other: "Vector") -> "Vector":
        return Vector(self.x + other.x, self.y + other.y, self.z + other.z)
    
    def __sub__(self, other: "Vector") -> "Vector":
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)
    
    def setOrigin(self, other: "Vector") -> None:
        self.x -= other.x
        self.y -= other.y
        self.z -= other.z
    
    @property
    def magnitude(self) -> float:
        return (self.x**2 + self.y**2 + self.z**2)**0.5
    
    def __repr__(self):
        return f"Vector({self.x}, {self.y}, {self.z})"
    
    @property
    def position(self):
        return [self.x, self.y, self.z]
    
    @position.setter
    def position(self, newVector: "Vector"):
        self.x, self.y, self.z = newVector.position
    
    @staticmethod
    def centerOfMass(vectors: list["Vector"]) -> "Vector":
        x = sum([vector.x for vector in vectors])/len(vectors)
        y = sum([vector.y for vector in vectors])/len(vectors)
        z = sum([vector.z for vector in vectors])/len(vectors)
        return Vector(x, y, z)
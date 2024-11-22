from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List



class Leaf(Component):
    pass

class Composite(Component):
    def __init__(self) -> None:
        self._children: List[Component] = []

    def add(self, component: Component) -> None:
        self._children.append(component)
        component.parent = self
    
    def remove(self, component: Component) -> None:
        self._children.remove(component)
        component.parent = None

    def isComposite(self) -> bool:
        return True
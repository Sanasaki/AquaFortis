from abc import ABC
from dataclasses import dataclass
from typing import Any

from Classes.Vector import Vector


@dataclass
class Gear:
    pass


class ContextProvider(ABC):
    def __init__(self):
        self._cachedAttributes: dict[str, str] = {}
        self._members: list[dict[str, str]] = []

    def register(self, gear: dict[str, str]):
        self._members.append(gear)

    def request(self, attr: Any, specifications: Any = None):
        if attrInCache := self._cachedAttributes.get(attr, None):
            return attrInCache
        for member in self._members:
            try:
                if attr in vars(member):
                    askedAttr = vars(member)[attr]
                    self._cachedAttributes[attr] = askedAttr
                    return askedAttr
            except TypeError:
                if askedAttr := member.get(attr, None):
                    return askedAttr
        raise AttributeError


class OperationManager(ABC):
    pass


class ExternalRessourceManager(ABC):
    pass


@dataclass
class ScriptDirector(ABC):
    jobProperties: ContextProvider
    jobWriter: OperationManager
    externalResourceManager: ExternalRessourceManager


if __name__ == "__main__":
    context = ContextProvider()
    aVector = Vector(x=0, y=1, z=3, label="10")
    someInfo = {"key": "value"}
    otherInfo = {"Koys": "aaaaaa"}
    context.register(someInfo)
    context.register(otherInfo)
    context.register(aVector)
    print(vars(aVector))

    print(context.request("Koys"))
    print(context.request("Koys"))
    print(context.request("label"))

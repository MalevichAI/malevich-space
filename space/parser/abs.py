from abc import ABC, abstractmethod

from space.schema import ComponentSchema


class AbsParser(ABC):
    @abstractmethod
    def parse(self, comp_dir: str) -> dict[str, ComponentSchema]:
        raise NotImplemented

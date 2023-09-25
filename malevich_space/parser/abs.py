from abc import ABC, abstractmethod

from malevich_space.schema import ComponentSchema


class AbsParser(ABC):
    @abstractmethod
    def parse(self, comp_dir: str) -> dict[str, ComponentSchema]:
        raise NotImplementedError

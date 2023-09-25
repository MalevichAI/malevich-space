from abc import ABC, abstractmethod

import malevich_space.schema as schema


class BaseComponentProvider(ABC):

    @abstractmethod
    def get_by_reverse_id(self, reverse_id: str) -> schema.ComponentSchema | None:
        raise NotImplementedError

    @abstractmethod
    def get_all(self) -> dict[str, schema.ComponentSchema]:
        raise NotImplementedError

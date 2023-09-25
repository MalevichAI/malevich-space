import malevich_space.schema as schema

from .base import BaseComponentProvider


class LocalComponentProvider(BaseComponentProvider):

    def __init__(self) -> None:
        self._components: dict[str, schema.ComponentSchema] = {}

    def register(self, comp: schema.ComponentSchema | dict[str, schema.ComponentSchema]):
        if type(comp) == schema.ComponentSchema:
            self._components[comp.reverse_id] = comp
        else:
            self._components = {**self._components, **comp}

    def get_by_reverse_id(self, reverse_id: str) -> schema.ComponentSchema | None:
        return self._components.get(reverse_id)

    def get_all(self) -> dict[str, schema.ComponentSchema]:
        return self._components

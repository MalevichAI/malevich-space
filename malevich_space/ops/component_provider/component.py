from collections import ChainMap

import malevich_space.schema as schema

from malevich_space.parser import YAMLParser

from .base import BaseComponentProvider
from .local import LocalComponentProvider


class ComponentProvider(BaseComponentProvider):

    def __init__(self) -> None:
        self.providers: list[BaseComponentProvider] = []

    def add_provider(self, provider: BaseComponentProvider):
        self.providers.append(provider)

    def get_by_reverse_id(self, reverse_id: str) -> schema.ComponentSchema | None:
        for provider in self.providers:
            matched = provider.get_by_reverse_id(reverse_id)
            if matched:
                return matched
        return None

    def get_all(self) -> dict[str, schema.ComponentSchema]:
        return dict(ChainMap(*self.providers))

    @staticmethod
    def get_yaml_provider(path: str) -> LocalComponentProvider:
        provider = LocalComponentProvider()
        parser = YAMLParser()
        provider.register(parser.parse(path))
        return provider

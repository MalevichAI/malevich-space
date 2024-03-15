import malevich_space.schema as schema

from .base import BaseService
from ..component_provider import BaseComponentProvider


class BaseComponentManager:

    def __init__(
        self,
        space: BaseService,
        host: schema.LoadedHostSchema,
        comp_dir: str | None = None,
        component_provider: BaseComponentProvider | None = None
    ) -> None:
        self.space = space
        self.host = host
        self.comp_dir = comp_dir
        self.component_provider = component_provider
    
    def component(
        self, comp: schema.ComponentSchema, version_mode: schema.VersionMode, sync: bool = True
    ) -> schema.LoadedComponentSchema:
        raise NotImplementedError

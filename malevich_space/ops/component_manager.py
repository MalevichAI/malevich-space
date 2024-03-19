from malevich_space.ops.component_provider.base import BaseComponentProvider
from malevich_space.ops.service.base import BaseService
from malevich_space.schema.component import ComponentSchema, LoadedComponentSchema
from malevich_space.schema.host import LoadedHostSchema
from malevich_space.schema.version_mode import VersionMode
from .service import BaseComponentManager


class ComponentManager(BaseComponentManager):

    def __init__(self, space: BaseService, host: LoadedHostSchema, comp_dir: str | None = None, component_provider: BaseComponentProvider | None = None):
        super().__init__(space, host, comp_dir, component_provider)

    def component(self, comp: ComponentSchema, version_mode: VersionMode, sync: bool = True) -> LoadedComponentSchema:
        return self.space.parse_raw(comp=comp, version_mode=version_mode, host_id=self.host.uid, sync=sync)

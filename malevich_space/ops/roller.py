import json
import logging

from typing import Any

import malevich_space.schema as schema

from malevich_space.parser import YAMLParser
from malevich_space.constants import ACTIVE_SETUP_PATH

from .space import SpaceOps
from .component_provider import ComponentProvider
from .component_manager import ComponentManager

from .env import get_active


class RollerOps:
    def __init__(
        self,
        config: schema.Setup,
        comp_dir: str,
        path: str | None = None,
        comp_provider: ComponentProvider | None = None
    ) -> None:
        logging.getLogger("gql.transport.aiohttp").setLevel(logging.ERROR)

        self.config = config

        self.space = SpaceOps(space_setup=self.config.space)

        self.host = self.ensure_host(self.config.space.host)

        self.comp_provider = None
        if comp_provider:
            self.comp_provider = comp_provider
        elif path:
            self.comp_provider = ComponentProvider()
            self.comp_provider.add_provider(ComponentProvider.get_yaml_provider(path))

        self.comp_manager = ComponentManager(
            space=self.space,
            host=self.host,
            comp_dir=comp_dir,
            component_provider=self.comp_provider,
        )

    def _load_host(self, local_host: schema.HostSchema) -> schema.LoadedHostSchema | None:
        hosts = self.space.get_my_hosts(url=local_host.conn_url)
        if hosts:
            return hosts[0]
        return None

    def ensure_host(self, local_host: schema.HostSchema) -> schema.LoadedHostSchema:
        loaded_host = self._load_host(local_host)
        if not loaded_host:
            loaded_host = self.space.create_host(alias=local_host.alias, conn_url=local_host.conn_url)
        return loaded_host

    def component(
        self,
        comp: schema.ComponentSchema,
        version_mode: schema.VersionMode = schema.VersionMode.DEFAULT,
    ) -> schema.LoadedComponentSchema:
        loaded = self.comp_manager.component(comp=comp, version_mode=version_mode)
        logging.info(f"Component processed: {loaded}")
        logging.info(f"|- Version: {loaded.version}")
        return loaded

    def build(self, comp: schema.LoadedComponentSchema) -> list[str] | None:
        """
        Build component active version :param comp: component to build :return task_id:

        Task ID for activated component.
        """
        if not comp.flow:
            return None
        task_id = self.space.build_task(flow_id=comp.flow.uid, host_id=self.host.uid)
        logging.info(f"Built {comp.reverse_id} with task_id (s): {task_id}")
        return task_id

    def boot(
        self,
        core_task: schema.LoadedTaskSchema,
        cfgs: list[schema.LoadedCfgSchema] | None = None,
        exec_mode: str | None = None,
    ) -> str:
        if cfgs is None:
            cfgs = []
        out = self.space.boot_task(
            task_id=core_task.uid, cfgs=[cfg.uid for cfg in cfgs], exec_mode=exec_mode
        )
        logging.info(f"Booted {core_task.uid}!")
        return out

    def run_task(self, task: schema.LoadedTaskSchema, raw: Any):
        if raw:
            raw = json.dumps(raw)
        run_id = self.space.run_task(task_id=task.uid, raw=raw)
        logging.info(f"Task: {task.uid}. Run: {run_id}!")
        return run_id

    def change_task_state(self, task: schema.LoadedTaskSchema, target_state: str):
        self.space.change_task_state(task_id=task.uid, target_state=target_state)
        logging.info(f"Updated task state ({task.uid}) -> {target_state}")

    def create_scheme(self, name: str, path: str) -> str:
        with open(path, "r") as f:
            data = f.read()
            return self.space.create_scheme(core_id=name, name=name, raw=data)


def local_roller(setup: str | None, comp_dir: str | str = None) -> RollerOps:
    if setup:
        config = schema.Setup(**YAMLParser.parse_yaml(setup))
    else:
        config = get_active(ACTIVE_SETUP_PATH)
    return RollerOps(config, path=comp_dir, comp_dir=comp_dir)

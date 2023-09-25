import os
import glob
import yaml
import logging

from typing import Any

from malevich_space.schema import *

from .abs import AbsParser


class YAMLParser(AbsParser):
    def __init__(self) -> None:
        pass

    def _parse_raw_requires(self, key: str, requires_data: dict[str, Any]) -> DepSchema:
        requires_data["key"] = key
        try:
            return DepSchema(**requires_data)
        except Exception as e:
            logging.exception(e)
            raise e

    def _parse_raw_op(self, op_core_id: str, op_data: dict[str, Any]) -> OpSchema:
        op_data["core_id"] = op_core_id
        if "requires" in op_data:
            op_data["requires"] = [
                self._parse_raw_requires(key, dep_data).dict()
                for key, dep_data in op_data["requires"].items()
            ]
        try:
            return OpSchema(**op_data)
        except Exception as e:
            logging.exception(e)
            raise e

    def _parse_raw_active_op(
        self, op_core_id: str | list[str], op_type: str
    ) -> list[OpSchema]:
        if isinstance(op_core_id, list):
            out = [OpSchema(core_id=uid, type=op_type) for uid in op_core_id]
        elif isinstance(op_core_id, str):
            out = [OpSchema(core_id=op_core_id, type=op_type)]
        else:
            out = []
        return out

    def _parse_raw_cfg(self, cfg_core_id: str, cfg_data: dict[str, Any]) -> CfgSchema:
        try:
            return CfgSchema(
                readable_name=cfg_data["name"],
                cfg_json=cfg_data["raw"],
                core_name=cfg_core_id,
            )
        except Exception as e:
            logging.exception(e)
            raise e

    @staticmethod
    def _get_path(path: str) -> str | None:
        if not os.path.exists(path):
            raise ValueError(f"File does not exist: {path}")
        with open(path) as f:
            return f.read()

    def _parse_raw_comp(
        self, comp_reverse_id: str, comp_data: dict[str, Any], comp_dir: str
    ) -> Optional[ComponentSchema]:
        comp_data["reverse_id"] = comp_reverse_id
        if "app" in comp_data:
            if "ops" in comp_data["app"]:
                comp_data["app"]["ops"] = [
                    self._parse_raw_op(op_core_id, op_data).dict()
                    for op_core_id, op_data in comp_data["app"]["ops"].items()
                ]
            if "cfg" in comp_data["app"]:
                comp_data["app"]["cfg"] = [
                    self._parse_raw_cfg(cfg_core_id, cfg_data).dict()
                    for cfg_core_id, cfg_data in comp_data["app"]["cfg"].items()
                ]
        if "flow" in comp_data and "components" in comp_data["flow"]:
            comps = []
            if (
                "components" in comp_data["flow"]
                and comp_data["flow"]["components"] is not None
            ):
                for alias, data in comp_data["flow"]["components"].items():
                    if "reverse_id" not in data:
                        reverse_id = alias
                    else:
                        reverse_id = data["reverse_id"]
                    parsed_comp = self._parse_in_flow_component(
                        alias=alias,
                        component_reverse_id=reverse_id,
                        component_data=data,
                    )
                    comps.append(parsed_comp)
            comp_data["flow"] = FlowSchema(
                is_demo=comp_data["flow"].get("is_demo", False), components=comps
            )
        if "collection" in comp_data:
            core_id = None
            path = None
            schema_core_id = comp_data["collection"].get("schema_core_id", None)
            if "path" in comp_data["collection"]:
                path = comp_data["collection"]["path"]
            comp_data["collection"] = CollectionAliasSchema(
                path=path,
                core_id=core_id,
                core_alias=comp_data["collection"].get("core_alias"),
                schema_core_id=schema_core_id,
            )
        if "schema_metadata" in comp_data:
            comp_data["required_schema"] = [
                SchemaMetadata(
                    core_id=core_id,
                    schema_data=YAMLParser._get_path(
                        f"{comp_dir}/{metadata['raw_path']}"
                    ),
                )
                for core_id, metadata in comp_data["schema_metadata"].items()
            ]
        try:
            return ComponentSchema(**comp_data)
        except Exception as e:
            logging.exception(e)
        return None

    def _parse_in_flow_component(
        self, alias: str, component_reverse_id: str, component_data: dict[str, Any]
    ) -> InFlowComponentSchema:
        component_data["reverse_id"] = component_reverse_id
        component_data["alias"] = alias
        if "app" in component_data and "active_op" in component_data["app"]:
            component_data["app"]["active_op"] = [
                parsed_op
                for type, op_core_id in component_data["app"]["active_op"].items()
                for parsed_op in self._parse_raw_active_op(op_core_id, op_type=type)
            ]
        if "active_cfg" in component_data:
            cfg = component_data["active_cfg"]
            if cfg is not None and not isinstance(cfg, str):
                parsed = [
                    self._parse_raw_cfg(cfg_core_id, cfg_data).dict()
                    for cfg_core_id, cfg_data in cfg.items()
                ]
                if parsed:
                    component_data["active_cfg"] = parsed[0]
        if "depends" in component_data:
            for alias, dep in component_data["depends"].items():
                schema_aliases = None
                if dep and "schema_aliases" in dep and dep["schema_aliases"]:
                    schema_aliases = [
                        SchemaAlias(src=key, target=value)
                        for key, value in dep["schema_aliases"].items()
                    ]
                component_data["depends"][alias] = InFlowDependency(
                    alias=alias,
                    schema_aliases=schema_aliases,
                    as_collection=dep.get("as_collection") if dep else None,
                )
        try:
            return InFlowComponentSchema(**component_data)
        except Exception as e:
            logging.exception(e)
            raise e

    def parser_iterator(self, base_path: str, comp_dir: str, parser_fun):
        out = []
        raw = self.parse_yaml(base_path)
        for reverse_id, raw_data in raw.items():
            parsed = parser_fun(reverse_id, raw_data, comp_dir)
            if parsed:
                out.append(parsed)
        return out

    def _parse_comp_file(self, path: str, comp_dir: str) -> list[ComponentSchema]:
        return self.parser_iterator(path, comp_dir, self._parse_raw_comp)

    def parse_dir_iterator(self, path: str, parser_fun) -> dict[str, Any]:
        out = {}
        for file in glob.glob(f"{path}/**/*.yaml", recursive=True):
            parsed = parser_fun(file, path)
            for p in parsed:
                out[p.reverse_id] = p
        return out

    @staticmethod
    def parse_yaml(path: str):
        return yaml.safe_load(YAMLParser._get_path(path))

    @staticmethod
    def dump_yaml(path: str, data: dict[str, Any]):
        dir = os.path.dirname(path)
        if not os.path.exists(dir):
            os.makedirs(dir)
        with open(path, "w", encoding="utf8") as outfile:
            yaml.dump(data, outfile, default_flow_style=False, allow_unicode=True)

    def parse(self, comp_dir: str) -> dict[str, ComponentSchema]:
        return self.parse_dir_iterator(comp_dir, self._parse_comp_file)

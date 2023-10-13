import json
import logging

import pandas as pd

import malevich_space.schema as schema
import malevich_space.constants as constants

from .service import BaseService
from .component_provider import BaseComponentProvider


class ComponentManager:
    default_version_update_md = constants.DEFAULT_VERSION_UPDATE_MD
    default_branch_name = constants.DEFAULT_BRANCH_NAME
    default_branch_status = constants.DEFAULT_BRANCH_STATUS
    default_version_name = constants.DEFAULT_VERSION_NAME
    default_version_status = constants.DEFAULT_VERSION_STATUS

    def __init__(
        self,
        space: BaseService,
        host: schema.LoadedHostSchema,
        comp_dir: str,
        component_provider: BaseComponentProvider | None = None
    ) -> None:
        self.space = space
        self.host = host
        self.comp_dir = comp_dir
        self.component_provider = component_provider

    @staticmethod
    def increment_version(previous: str | None, mode: str):
        if not previous:
            previous = "0.0.0"
        broken = previous.split(".")
        if mode == "major":
            broken[0] = str(int(broken[0]) + 1)
            broken[1] = str(0)
            broken[2] = str(0)
        elif mode == "minor":
            broken[1] = str(int(broken[1]) + 1)
            broken[2] = str(0)
        elif mode == "patch":
            broken[2] = str(int(broken[2]) + 1)
        return ".".join(broken)

    def _app2version(
        self, reverse_id: str, app: schema.AppSchema, attach2version_id: str, preload_op: bool = True
    ) -> schema.LoadedComponentSchema:
        app_id = self.space.create_app_in_version(
            version_id=attach2version_id,
            container_ref=app.container_ref,
            container_user=app.container_user,
            container_token=app.container_token,
            preload_op=preload_op
        )
        if app.cfg:
            for cfg in app.cfg:
                cfg_id = self.space.create_cfg_standalone(
                    readable_name=cfg.readable_name,
                    cfg_json=json.dumps(cfg.cfg_json),
                    core_name=cfg.core_name,
                )
                self.space.add_cfg_2_av(app_id=app_id, cfg_id=cfg_id)
        if app.ops:
            for op in app.ops:
                op_space_id = self.space.create_op(
                    core_id=op.core_id,
                    input_schema=op.input_schema,
                    output_schema=op.output_schema,
                )
                self.space.add_op_2_av(app_id=app_id, op_id=op_space_id, op_type=op.type)
                if op.requires:
                    for dep in op.requires:
                        self.space.add_dep_2_op(op_id=op_space_id, dep_key=dep.key, dep_type=dep.type)
        return self.space.get_parsed_component_by_reverse_id(reverse_id=reverse_id)

    def select_op(self, flow_id: str, comp_id: str, ops: list[schema.LoadedOpSchema]):
        for op in ops:
            self.space.select_active_op(
                flow_id=flow_id, comp_id=comp_id, op_type=op.type, op_id=op.uid
            )

    def handle_reverse_id(self, reverse_id: str) -> schema.ComponentSchema | None:
        if self.component_provider:
            local = self.component_provider.get_by_reverse_id(reverse_id)
            if local:
                return local
        remote = self.space.get_parsed_component_by_reverse_id(reverse_id=reverse_id)
        if not remote:
            raise ValueError(f"{reverse_id} has not usable component")
        return remote

    def _flow2version(
        self,
        src_comp_reverse_id: str,
        flow: schema.FlowSchema,
        attach2version_id: str,
        is_demo: bool = False,
    ) -> schema.LoadedComponentSchema:
        flow_id = self.space.create_flow_in_version(
            version_id=attach2version_id, is_demo=is_demo
        )
        loaded_comps = {}
        for comp in flow.components:
            loaded_comp = self.component(
                comp=self.handle_reverse_id(comp.reverse_id),
                version_mode=schema.VersionMode.DEFAULT,
            )
            loaded_comp_type = loaded_comp.type()
            version_id = loaded_comp.version.uid
            comp_in_flow_id = self.space.add_comp_in_flow(
                flow_id=flow_id,
                target_comp_version_id=version_id,
                offset_x=comp.offsetX,
                offset_y=comp.offsetY,
                version_id=version_id,
            )
            loaded_comps[comp.alias] = {
                "component": loaded_comp,
                "in_flow_id": comp_in_flow_id,
            }
            if loaded_comp_type == schema.ComponentType.APP:
                app = loaded_comp.app
                if comp.app and comp.app.active_op:
                    active_op_core_id = [op.core_id for op in comp.app.active_op]
                    active_op = [
                        op for op in app.ops if op.core_id in active_op_core_id
                    ]
                    self.select_op(flow_id, comp_in_flow_id, active_op)
            if comp.active_cfg:
                if isinstance(comp.active_cfg, str):
                    cfg = comp.active_cfg
                else:
                    cfg = comp.active_cfg.core_name
                    self.space.create_cfg_standalone(
                        readable_name=comp.active_cfg.readable_name,
                        cfg_json=json.dumps(comp.active_cfg.cfg_json),
                        core_name=comp.active_cfg.core_name,
                    )
                self.space.set_in_flow_component_cfg(flow_id=flow_id, comp_id=comp_in_flow_id, cfg_core_id=cfg)
        for comp in flow.components:
            if not comp.depends:
                continue
            for _, dep in comp.depends.items():
                if not dep.alias:
                    continue
                if dep.alias not in loaded_comps:
                    raise KeyError(
                        "Dep alias definition is not present in flow definition"
                    )
                start_id = loaded_comps[dep.alias].get("in_flow_id", None)
                target_id = loaded_comps[comp.alias].get("in_flow_id", None)

                assert start_id and target_id

                self.space.link(
                    flow_id=flow_id,
                    start_id=start_id,
                    target_id=target_id,
                    schema_adapter_id=None,
                    as_collection=dep.as_collection,
                )

                if not dep.schema_aliases:
                    continue

                for schema_alias in dep.schema_aliases:
                    self.space.add_schema_alias(
                        flow_id=flow_id,
                        start_id=start_id,
                        target_id=target_id,
                        src_schema=schema_alias.src,
                        target_schema=schema_alias.target,
                    )
        return self.space.get_parsed_component_by_reverse_id(reverse_id=src_comp_reverse_id)

    def _get_df(self, file: str) -> pd.DataFrame:
        return pd.read_csv(file)

    def _get_json_docs(self, df: pd.DataFrame) -> list[str]:
        return [row.to_json() for _, row in df.iterrows()]

    def _collection_alias2version(
        self,
        reverse_id: str,
        collection: schema.CollectionAliasSchema,
        attach2version_id: str,
    ) -> schema.LoadedComponentSchema | None:
        src_collection_at_path = f"{self.comp_dir}/{collection.path}"
        docs = self._get_json_docs(self._get_df(src_collection_at_path))
        ca_id = self.space.create_collection(
            host_id=self.host.uid,
            core_alias=collection.core_alias,
            schema_core_id=collection.schema_core_id,
            docs=docs
        )
        self.space.create_collection_in_version(version_id=attach2version_id, ca_id=ca_id)
        return self.space.get_parsed_component_by_reverse_id(reverse_id=reverse_id)

    def component2version(self, comp: schema.ComponentSchema, attach2version_id: str):
        created = None
        if comp.app:
            created = self._app2version(comp.reverse_id, comp.app, attach2version_id)
            logging.debug(f"New app instance uid: {created.app.uid}")
        if comp.flow:
            created = self._flow2version(
                src_comp_reverse_id=comp.reverse_id,
                flow=comp.flow,
                attach2version_id=attach2version_id,
                is_demo=comp.flow.is_demo,
            )
            logging.debug(f"New flow instance uid: {created.flow.uid}")
        if comp.collection:
            created = self._collection_alias2version(comp.reverse_id, comp.collection, attach2version_id)
        return created

    def _create_schema(self, schema_metadata: list[schema.SchemaMetadata]):
        for schema in schema_metadata:
            exists = self.space.get_schema(core_id=schema.core_id)
            if exists:
                continue
            self.space.create_scheme(core_id=schema.core_id, raw=json.dumps(json.loads(schema.schema_data)))

    def _attach_use_case(self, comp_uid: str, uc: schema.UseCaseSchema, designed: bool):
        use_case = self.space.create_use_case(title=uc.title, body=uc.body, is_public_example=uc.is_public_example)
        self.space.attach_use_case(comp_uid=comp_uid, use_case_uid=[use_case], designed=designed)

    def component(
        self, comp: schema.ComponentSchema, version_mode: schema.VersionMode
    ) -> schema.LoadedComponentSchema:
        loaded = self.space.get_parsed_component_by_reverse_id(
            reverse_id=comp.reverse_id
        )
        if comp.required_schema:
            self._create_schema(comp.required_schema)
        branch_status = self.default_branch_status
        version_status = self.default_version_status
        version_name = None
        version_update_md = self.default_version_update_md
        if comp.version:
            if comp.version.readable_name:
                version_name = comp.version.readable_name
            if comp.version.updates_markdown:
                version_update_md = comp.version.updates_markdown
            if comp.version.status:
                version_status = comp.version.status
        if loaded:
            if version_mode == schema.VersionMode.DEFAULT:
                return loaded
            else:
                old_version_name = None
                if comp.branch and comp.branch.name:
                    branch = self.space.get_branch_by_name(
                        component_id=loaded.uid, branch_name=comp.branch.name
                    )
                    if branch:
                        branch_id = branch.uid
                        if branch.active_version:
                            old_version_name = branch.active_version.readable_name
                    else:
                        branch_id = self.space.create_branch(
                            component_id=loaded.uid,
                            name=comp.branch.name,
                            status=branch_status,
                            comp_rel_status=branch_status,
                        )
                else:
                    old_version: schema.LoadedVersionSchema = loaded.version
                    old_version_name = old_version.readable_name
                    branch_id = loaded.branch.uid
                if not version_name:
                    version_name = self.increment_version(
                        old_version_name, mode=version_mode.value
                    )
        else:
            kwargs = comp.model_dump()
            kwargs["type"] = comp.type().value
            kwargs["org_id"] = self.space.org_id()
            comp_id = self.space.create_component(**kwargs)
            if comp.designed_for_use_case:
                for uc in comp.designed_for_use_case:
                    self._attach_use_case(comp_uid=comp_id, uc=uc, designed=True)
            if comp.not_designed_for_use_case:
                for uc in comp.not_designed_for_use_case:
                    self._attach_use_case(comp_uid=comp_id, uc=uc, designed=False)
            branch_name = self.default_branch_name
            if comp.branch:
                if comp.branch.name:
                    branch_name = comp.branch.name
                if comp.branch.status:
                    branch_status = comp.branch.status
            branch_id = self.space.create_branch(
                component_id=comp_id,
                name=branch_name,
                status=branch_status,
                comp_rel_status=branch_status,
            )
            if not version_name:
                version_name = self.default_version_name

        new_version_id = self.space.create_version(
            branch_id=branch_id,
            readable_name=version_name,
            updates_markdown=version_update_md,
            branch_version_status=version_status,
        )

        logging.info(f"New version uid: {new_version_id}")

        return self.component2version(comp, new_version_id)

    def create_config_for_app(self, app_id: str, cfgs: list[schema.CfgSchema]):
        for readable_name, cfg in cfgs:
            cfg_id = self.space.create_cfg_standalone(
                readable_name=readable_name, cfg_json=json.dumps(cfg)
            )
            self.space.add_cfg_2_av(app_id=app_id, cfg_id=cfg_id)

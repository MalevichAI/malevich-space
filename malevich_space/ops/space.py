from typing import Any, Optional

import requests

from gql import Client
from gql.transport.aiohttp import AIOHTTPTransport
from gql.transport.websockets import WebsocketsTransport

import malevich_space.gql as client
import malevich_space.schema as schema

from .service import BaseService


class SpaceOps(BaseService):
    def __init__(self, space_setup: schema.SpaceSetup) -> None:
        self.space_setup = space_setup
        self.token = self.auth(self.space_setup.username, self.space_setup.password)
        self.client, self.ws_client = self.init_graphql()
        self.org = self.get_org(reverse_id=self.space_setup.org)

    def org_id(self) -> str | None:
        if self.org:
            return self.org.uid
        return None

    def auth(self, username: str, password: str):
        fields = {"username": username, "password": password}
        response = requests.post(self.space_setup.auth_url, fields)
        return response.json()["access_token"]

    def init_graphql(self) -> tuple[Client, Client]:
        headers = {"Authorization": "Bearer " + self.token}

        transport = AIOHTTPTransport(url=self.space_setup.gql_url, headers=headers)

        ws_transport = Client(
            transport=WebsocketsTransport(url=self.space_setup.ws_url), fetch_schema_from_transport=True, execute_timeout=60
        ) if self.space_setup.ws_url else None

        return Client(
            transport=transport, fetch_schema_from_transport=True, execute_timeout=600
        ), ws_transport

    def get_org(self, *args, **kwargs) -> schema.LoadedOrgSchema | None:
        result = self.client.execute(client.get_org, variable_values=kwargs)
        if result["org"]:
            org = result["org"]["details"]
            # TODO what is name and slug here, and what is the proper type for schema?
            return schema.LoadedOrgSchema(
                uid=org["uid"],
                # name=org["name"],
                # slug=org["reverseId"],
            )
        return None

    def _parse_raw_sa(self, raw: dict[str, Any]) -> schema.LoadedSASchema:
        return schema.LoadedSASchema(
            uid=raw["details"]["uid"],
            alias=raw["details"]["alias"],
            core_username=raw["details"]["coreUsername"],
            core_password=raw["details"]["corePassword"],
        )

    def _parse_raw_host(self, raw: dict[str, Any]) -> schema.LoadedHostSchema:
        return schema.LoadedHostSchema(
            uid=raw["details"]["uid"],
            alias=raw["details"]["alias"],
            conn_url=raw["details"]["connUrl"],
            sa=[self._parse_raw_sa(sa["node"]) for sa in raw["mySaOnHost"]["edges"]],
        )

    def create_host(self, *args, **kwargs) -> str:
        result = self.client.execute(client.host_create, variable_values=kwargs)
        return result["hosts"]["create"]["details"]["uid"]

    def create_sa(self, *args, **kwargs) -> str:
        result = self.client.execute(client.sa_create, variable_values=kwargs)
        return result["host"]["createSa"]["details"]["uid"]

    def get_my_hosts(self, *args, **kwargs) -> list[schema.LoadedHostSchema]:
        result = self.client.execute(client.get_host, variable_values=kwargs)
        return [
            self._parse_raw_host(host["node"])
            for host in result["user"]["me"]["hosts"]["edges"]
        ]

    def create_use_case(self, *args, **kwargs) -> str:
        result = self.client.execute(client.create_use_case, variable_values=kwargs)
        return result["useCases"]["create"]["details"]["uid"]

    def attach_use_case(self, *args, **kwargs) -> bool:
        result = self.client.execute(client.attach_use_case, variable_values=kwargs)
        return result["component"]["attachUseCase"] is not None

    def create_component(self, *args, **kwargs) -> str:
        result = self.client.execute(client.create_component, variable_values=kwargs)
        return result["components"]["create"]["details"]["uid"]

    def create_branch(self, *args, **kwargs) -> str:
        result = self.client.execute(client.create_branch, variable_values=kwargs)
        return result["component"]["createBranch"]["uid"]

    def create_version(self, *args, **kwargs) -> str:
        result = self.client.execute(client.create_version, variable_values=kwargs)
        return result["branch"]["createVersion"]["uid"]

    def create_tag(self, *args, **kwargs) -> str:
        result = self.client.execute(client.create_tag, variable_values=kwargs)
        return result["tags"]["create"]["details"]["uid"]

    def attach_tag_to_comp(self, *args, **kwargs) -> str:
        result = self.client.execute(client.tag_to_comp, variable_values=kwargs)
        return result["component"]["addTag"]

    def create_app_in_version(self, *args, **kwargs) -> str:
        result = self.client.execute(client.app_comp, variable_values=kwargs)
        return result["version"]["addUnderlyingApp"]["uid"]

    def create_flow_in_version(self, *args, **kwargs) -> str:
        result = self.client.execute(client.flow_comp, variable_values=kwargs)
        return result["version"]["addUnderlyingFlow"]["uid"]

    def create_collection(self, *args, **kwargs) -> str:
        result = self.client.execute(client.create_collection_alias, variable_values=kwargs)
        return result["collectionAliases"]["create"]["details"]["uid"]

    def create_collection_in_version(self, *args, **kwargs) -> str:
        result = self.client.execute(client.ca_comp, variable_values=kwargs)
        return result["version"]["addUnderlyingCa"]["uid"]

    def get_branch_by_name(self, *args, **kwargs) -> schema.LoadedBranchSchema | None:
        result = self.client.execute(client.branch_by_name, variable_values=kwargs)
        if result["component"]["branches"]["edges"]:
            branch = result["component"]["branches"]["edges"][0]["node"]
            active_version = None
            if branch["activeVersion"] is not None:
                active_version = schema.LoadedVersionSchema(
                    uid=branch["activeVersion"]["details"]["uid"],
                    readable_name=branch["activeVersion"]["details"]["readableName"],
                    updates_markdown=None,
                )
            out = schema.LoadedBranchSchema(
                uid=branch["details"]["uid"],
                name=branch["details"]["name"],
                active_version=active_version,
            )
            return out
        return None

    def add_comp_in_flow(self, *args, **kwargs):
        result = self.client.execute(client.add_comp_to_flow, variable_values=kwargs)
        return result["flow"]["addComponent"]["details"]["uid"]

    def add_app_to_comp_flow(self, *args, **kwargs) -> str:
        result = self.client.execute(client.set_app_in_flow, variable_values=kwargs)
        return result["flow"]["inFlowComponent"]["updateApp"]["details"]["uid"]

    def add_ca_to_comp_flow(self, *args, **kwargs) -> str:
        result = self.client.execute(client.set_ca_in_flow, variable_values=kwargs)
        return result["flow"]["inFlowComponent"]["updateCollectionAlias"]["details"][
            "uid"
        ]

    def link(self, *args, **kwargs) -> str:
        result = self.client.execute(client.link_components, variable_values=kwargs)
        return result["flow"]["linkComponents"]["schemaAdapter"]["details"]["uid"]

    def add_schema_alias(self, *args, **kwargs) -> str:
        result = self.client.execute(client.add_schema_alias, variable_values=kwargs)
        return result["flow"]["addSchemaAlias"]

    def create_cfg_standalone(self, *args, **kwargs) -> str:
        result = self.client.execute(client.create_cfg, variable_values=kwargs)
        return result["configs"]["update"]["uid"]

    def create_scheme(self, *args, **kwargs) -> str:
        result = self.client.execute(client.create_scheme, variable_values=kwargs)
        return result["schemas"]["create"]["details"]["uid"]

    def create_op(self, *args, **kwargs) -> str:
        result = self.client.execute(client.create_op, variable_values=kwargs)
        return result["ops"]["create"]["details"]["uid"]

    def add_op_2_av(self, *args, **kwargs) -> str:
        result = self.client.execute(client.add_op_to_av, variable_values=kwargs)
        return result["app"]["addOp2Av"]["details"]["uid"]

    def select_active_op(self, *args, **kwargs) -> str:
        result = self.client.execute(client.select_op, variable_values=kwargs)
        return result["flow"]["inFlowComponent"]["selectOp"]["details"]["uid"]

    def set_in_flow_component_cfg(self, *args, **kwargs):
        result = self.client.execute(client.set_in_flow_comp_cfg, variable_values=kwargs)
        return result["flow"]["inFlowComponent"]["updateConfig"]["details"]["uid"]

    def get_schema(self, *args, **kwargs) -> schema.LoadedSchemaSchema | None:
        result = self.client.execute(client.get_schema, variable_values=kwargs)
        if result["schema"]:
            raw = result["schema"]["details"]
            raw["core_id"] = raw["coreId"]
            return schema.LoadedSchemaSchema(**raw)
        return None

    def add_cfg_2_av(self, *args, **kwargs):
        result = self.client.execute(client.add_cfg_2_av, variable_values=kwargs)
        return result["app"]["addCfg2Av"]["details"]["uid"]

    def add_dep_2_op(self, *args, **kwargs):
        result = self.client.execute(client.add_dep_to_op, variable_values=kwargs)
        return result["op"]["addDep"]["details"]["uid"]

    def get_component_by_reverse_id(self, *args, **kwargs) -> dict[str, Any]:
        if not self:
            raise RuntimeError("self is None in get_component_by_reverse_id")
        result = self.client.execute(client.get_comp_with_reverse_id, variable_values=kwargs)
        return result["component"]

    def _parse_loaded_deps(
        self, raw_deps: list[dict[str, Any]]
    ) -> list[schema.LoadedDepSchema]:
        return [
            schema.LoadedDepSchema(
                uid=dep["details"]["uid"],
                key=dep["details"]["key"],
                type=dep["details"]["type"],
            )
            for dep in raw_deps
        ]

    def _parse_loaded_ops(self, raw_ops: list[dict[str, Any]]) -> list[schema.LoadedOpSchema]:
        out = []
        for op in raw_ops:
            op_node = op["node"]
            op_rel = op["rel"]

            def _parse_schema(key):
                loaded_schema = op_node.get(key)
                if loaded_schema:
                    return loaded_schema
                return []

            input_schema = _parse_schema("inputSchema")
            output_schema = _parse_schema("outputSchema")

            out.append(
                schema.LoadedOpSchema(
                    core_id=op_node["details"]["coreId"],
                    type=op_rel["type"],
                    input_schema=[s["details"]["coreId"] for s in input_schema],
                    output_schema=[s["details"]["coreId"] for s in output_schema],
                    uid=op_node["details"]["uid"],
                    requires=self._parse_loaded_deps(op_node.get("deps", [])),
                )
            )
        return out

    def _parse_in_flow_app(self, app_data) -> schema.LoadedInFlowAppSchema | None:
        if app_data:
            return schema.LoadedInFlowAppSchema(app_id=app_data["details"]["uid"])
        return None

    def _parse_in_flow_prompt(self, prompt_data) -> schema.LoadedPromptSchema | None:
        if prompt_data:
            return schema.LoadedPromptSchema(**prompt_data["details"])
        return None

    def _parse_in_flow_component(
        self, in_flow_data: dict[str, Any]
    ) -> schema.LoadedInFlowComponentSchema:
        base_data = {
            "uid": in_flow_data["node"]["details"]["uid"],
            "app": self._parse_in_flow_app(in_flow_data["node"]["app"])
            if "app" in in_flow_data["node"]
            else None,
            "prompt": self._parse_in_flow_prompt(in_flow_data["node"]["prompt"])
            if "prompt" in in_flow_data["node"]
            else None,
        }
        if (
            "component" in in_flow_data["node"]
            and in_flow_data["node"]["component"] is not None
        ):
            base_data["reverse_id"] = in_flow_data["node"]["component"]["details"][
                "reverseId"
            ]
            base_data["comp_id"] = in_flow_data["node"]["component"]["details"]["uid"]
        if "prev" in in_flow_data["node"]:
            base_data["prev"] = [
                self._parse_in_flow_component(prev["node"])
                for prev in in_flow_data["node"]["prev"]["edges"]
            ]
        return schema.LoadedInFlowComponentSchema(**base_data)

    def _parse_comp(self, comp: dict[str, Any]) -> schema.LoadedComponentSchema:
        version = comp["activeBranchVersion"]
        parsed_version = None
        if version:
            details: dict[str, Any] = version["details"]
            version_base_data = {
                "uid": details["uid"],
                "readable_name": details["readableName"],
                "updates_markdown": details["updatesMarkdown"],
            }
            parsed_version = schema.LoadedVersionSchema(**version_base_data)
        details = comp["details"]
        base_data = {
            "uid": details["uid"],
            "name": details["name"],
            "reverse_id": details["reverseId"],
            "branch": schema.LoadedBranchSchema(**comp["activeBranch"]["details"]),
            "version": parsed_version,
            "description": details["descriptionMarkdown"],
        }
        if version and "app" in version and version["app"]:
            base_data["app"] = schema.LoadedAppSchema(
                uid=version["app"]["details"]["uid"],
                container_ref=version["app"]["details"]["containerRef"],
                container_user=version["app"]["details"]["containerUser"],
                container_token=version["app"]["details"]["containerToken"],
                ops=self._parse_loaded_ops(version["app"]["avOp"]["edges"]),
            )
        if version and "flow" in version and version["flow"]:
            base_data["flow"] = schema.LoadedFlowSchema(
                uid=version["flow"]["details"]["uid"],
                components=[
                    self._parse_in_flow_component(in_flow_data)
                    for in_flow_data in version["flow"]["inFlowComponents"]["edges"]
                ],
            )
        if version and "collection" in version and version["collection"]:
            base_data["collection"] = schema.LoadedCollectionAliasSchema(
                uid=version["collection"]["details"]["uid"]
            )
        return schema.LoadedComponentSchema(**base_data)

    def get_parsed_component_by_reverse_id(
        self, *args, **kwargs
    ) -> schema.LoadedComponentSchema | None:
        comp = self.get_component_by_reverse_id(*args, **kwargs)
        if not comp:
            return None
        return self._parse_comp(comp)

    def get_flow(self, uid: str) -> schema.LoadedFlowSchema:
        results = self.client.execute(client.get_flow, variable_values={"flow_id": uid})
        return schema.LoadedFlowSchema(
            uid=results["flow"]["details"]["uid"],
            components=[
                self._parse_in_flow_component(in_flow_data)
                for in_flow_data in results["flow"]["inFlowComponents"]["edges"]
            ]
        )

    def malevich(self, prompt: str, max_depth: int = 1) -> tuple[str, str]:
        res = self.client.execute(
            client.add_pt_2_malevich,
            variable_values={"prompt": prompt, "max_depth": max_depth},
        )

        pt_id = res["malevich"]["addPt"]["details"]["uid"]
        thought_id = res["malevich"]["addPt"]["thoughts"]["edges"][0]["node"][
            "details"
        ]["uid"]

        return pt_id, thought_id

    def generate_flow(self, *args, **kwargs) -> schema.LoadedFlowSchema:
        result = self.client.execute(client.generate_workflow, variable_values=kwargs)

        flow_node = result["malevich"]["pt"]["generateFlow"]["edges"][0]["node"]

        return schema.LoadedFlowSchema(
            uid=flow_node["details"]["uid"],
            components=[
                self._parse_in_flow_component(in_flow_data)
                for in_flow_data in flow_node["inFlowComponents"]["edges"]
            ],
        )

    def build_task(self, *args, **kwargs) -> list[str]:
        result = self.client.execute(client.build_task, variable_values=kwargs)
        return [
            created["details"]["uid"] for created in result["flow"]["buildCoreTask"]
        ]

    def boot_task(self, *args, **kwargs) -> str:
        result = self.client.execute(client.boot_task, variable_values=kwargs)
        return result["task"]["boot"]["details"]["uid"]

    def change_task_state(self, *args, **kwargs) -> str:
        result = self.client.execute(client.change_task_state, variable_values=kwargs)
        return result["task"]["changeState"]["details"]["uid"]

    def update_ca(self, *args, **kwargs) -> str:
        result = self.client.execute(client.update_collection_alias, variable_values=kwargs)
        return result["collectionAlias"]["update"]["uid"]

    def run_task(self, *args, **kwargs) -> str:
        result = self.client.execute(client.run_task, variable_values=kwargs)
        return result["runWithStatus"]["details"]["uid"]

    def wipe_component(self, uid: Optional[str] = None, reverse_id: Optional[str] = None) -> bool:
        kwargs = {
            "uid": uid,
            "reverse_id": reverse_id
        }
        result = self.client.execute(client.wipe_component, variable_values=kwargs)
        return result["component"]["wipe"]

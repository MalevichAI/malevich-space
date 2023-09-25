import malevich_space.schema as schema
import malevich_space.constants as constants

from malevich_space.ops.service import BaseService
from malevich_space.ops.component_provider import BaseComponentProvider
from malevich_space.parser import YAMLParser

from .report import CIReportSetup, CIReport, CIPlatform


class CIManager:

    default_var_name = {
        "comp_dir": "COMPONENT_DIR",
        "status": "APP_CI_STATUS"
    }

    required_commands = [
        "pip install malevich-space"
    ]

    PATCH_FLAG = "space ci report"

    def __init__(
        self,
        space: BaseService,
        host: schema.LoadedHostSchema,
        sa: schema.LoadedSASchema,
        component_provider: BaseComponentProvider
    ) -> None:
        self.space = space
        self.host = host
        self.sa = sa
        self.component_provider = component_provider

    @staticmethod
    def flag(name: str, var_name: str | None = None, value: str | None = None) -> str:
        assert var_name or value
        if var_name:
            return f"--{name}=" + "${" + var_name + "}" + (value if value else "")
        elif value:
            return f"--{name}={value}"

    @staticmethod
    def report_command(setup: CIReportSetup, var_name: dict[str, str]) -> str:
        blocks = [
            "space",
            "ci",
            "report",
            CIManager.flag("comp_dir", value=setup.comp_dir),
            CIManager.flag("branch", var_name=var_name.get("branch")),
            CIManager.flag("commit", var_name=var_name.get("commit")),
            CIManager.flag("commit_message", var_name=var_name.get("commit_message")),
            CIManager.flag("status", value="success"),
            CIManager.flag("image", var_name=var_name.get("image"), value=":latest"),
        ]
        return " ".join(blocks)

    @staticmethod
    def verify_patch(script: list[str]) -> bool:
        for s in script:
            if CIManager.PATCH_FLAG in s:
                return True
        return False

    @staticmethod
    def _patch_gitlab(setup: CIReportSetup):
        gitlab = {
            "branch": "CI_COMMIT_REF_NAME",
            "commit": "CI_COMMIT_SHA",
            "commit_message": "CI_COMMIT_MESSAGE",
            "image": "CI_REGISTRY_IMAGE"
        }
        var_name = {**CIManager.default_var_name, **gitlab}
        command = CIManager.report_command(setup, var_name)
        ci_data = YAMLParser.parse_yaml(setup.config_path)
        ci_steps = [key for key in ci_data.keys() if "build" in key]
        edited = False
        for ci_step in ci_steps:
            scirpt = ci_data[ci_step].get("script")
            if not scirpt:
                continue
            already_patched = CIManager.verify_patch(scirpt)
            if already_patched:
                continue
            for required_command in CIManager.required_commands:
                scirpt.append(required_command)
            scirpt.append(command)
            ci_data[ci_step]["script"] = scirpt
            edited = True
        if edited:
            YAMLParser.dump_yaml(setup.config_path, ci_data)

    @staticmethod
    def add_ci_callback(setup: CIReportSetup):
        match setup.platform:
            case CIPlatform.GITLAB:
                CIManager._patch_gitlab(setup)

    def _report_ci_reverse_id(self, reverse_id: str, report: CIReport):
        comp = self.space.get_parsed_component_by_reverse_id(reverse_id=reverse_id)
        if not comp:
            return
        branch = self.space.get_branch_by_name(component_id=comp.uid, branch_name=report.branch)
        if not branch:
            branch = self.space.create_branch(
                component_id=comp.uid, name=report.branch, status="created", comp_rel_status="default"
            )
        else:
            branch = branch.uid
        self.space.create_version(
            branch_id=branch,
            readable_name=report.commit_digest,
            updates_markdown=report.commit_message,
            branch_version_status=constants.DEFAULT_VERSION_STATUS
        )

    def report_ci_status(self, report: CIReport):
        for reverse_id, _ in self.component_provider.get_all():
            self._report_ci_reverse_id(reverse_id, report)

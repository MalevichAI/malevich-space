import malevich_space.schema as schema
import malevich_space.constants as constants

from malevich_space.ops.roller import RollerOps
from malevich_space.parser import YAMLParser

from .report import CIReportSetup, CIReport, CIPlatform, CIStatus


class CIManager:

    main_branch_name = ["main", "master"]
    default_space_branch_status = "default"

    default_var_name = {
        "comp_dir": "COMPONENT_DIR",
        "status": "APP_CI_STATUS"
    }

    required_commands = [
        "pip install malevich-space"
    ]

    PATCH_FLAG = "space ci report"

    def __init__(self, roller: RollerOps) -> None:
        self.roller = roller

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

    def _report_ci_reverse_id(self, local_definition: schema.ComponentSchema, report: CIReport):
        if report.status != CIStatus.DONE or not local_definition.is_type(schema.ComponentType.APP):
            return

        if not self.roller.space.get_parsed_component_by_reverse_id(
            reverse_id=local_definition.reverse_id
        ):
            vmode = schema.VersionMode.DEFAULT
        else:
            vmode = schema.VersionMode.MINOR

        branch_status = constants.DEFAULT_BRANCH_STATUS \
            if report.branch in self.main_branch_name else self.default_space_branch_status

        local_definition.branch = schema.BranchSchema(
            name=report.branch,
            status=branch_status
        )
        local_definition.version = schema.VersionSchema(
            commit_digest=report.commit_digest,
            readable_name=report.commit_digest[:4],
            updates_markdown=report.commit_message,
            status=constants.DEFAULT_VERSION_STATUS
        )
        if local_definition.app:
            local_definition.app.container_ref = report.image
            local_definition.app.container_user = report.image_user
            local_definition.app.container_token = report.image_token
        else:
            local_definition.app = schema.AppSchema(
                container_ref=report.image,
                container_user=report.image_user,
                container_token=report.image_token
            )

        self.roller.component(
            comp=local_definition,
            version_mode=vmode
        )

    def report_ci_status(self, report: CIReport):
        for _, local_definition in self.roller.comp_provider.get_all().items():
            self._report_ci_reverse_id(local_definition, report)

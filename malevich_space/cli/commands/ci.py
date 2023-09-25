from typing import Optional

import typer

import malevich_space.schema as schema
import malevich_space.constants as constants

from malevich_space.ci import CIPlatform, CIStatus, CIReport, CIReportSetup, CIManager
from malevich_space.ops import RollerOps


app = typer.Typer()


@app.command()
def add(config_path: str, platform: CIPlatform, comp_dir: str):
    setup = CIReportSetup(config_path=config_path, comp_dir=comp_dir, platform=platform)
    CIManager.add_ci_callback(setup)


@app.command()
def report(
        comp_dir: str,
        branch: str,
        commit_digest: str,
        commit_message: str,
        status: CIStatus,
        image: str,
        space_username: Optional[str] = None,
        space_password: Optional[str] = None,
        space_token: Optional[str] = None,
        space_auth_url: str = constants.SPACE_AUTH_URL,
        space_gql_url: str = constants.SPACE_GQL_URL
):
    setup = schema.Setup(
        space=schema.SpaceSetup(
            auth_url=space_auth_url,
            gql_url=space_gql_url,
            username=space_username,
            password=space_password,
            token=space_token
        )
    )

    roller = RollerOps(setup, comp_dir)

    report_instance = CIReport(
        branch=branch,
        commit_digest=commit_digest,
        commit_message=commit_message,
        status=status,
        image=image
    )

    manager = CIManager(
        roller.space,
        roller.host,
        roller.sa,
        roller.comp_provider
    )

    manager.report_ci_status(report_instance)

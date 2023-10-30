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
        api_url: str,
        image_user: Optional[str] = typer.Option(None),
        image_token: Optional[str] = typer.Option(None),
        space_username: Optional[str] = typer.Option(None),
        space_password: Optional[str] = typer.Option(None),
        space_org: Optional[str] = typer.Option(None),
        space_token: Optional[str] = typer.Option(None),
):
    assert (space_username and space_password) or space_token
    setup = schema.Setup(
        space=schema.SpaceSetup(
            api_url=api_url,
            username=space_username,
            password=space_password,
            token=space_token,
            org=space_org
        )
    )

    roller = RollerOps(setup, comp_dir, path=comp_dir)
    report_instance = CIReport(
        branch=branch,
        commit_digest=commit_digest,
        commit_message=commit_message,
        status=status,
        image=image,
        image_user=image_user,
        image_token=image_token
    )

    manager = CIManager(roller=roller)
    manager.report_ci_status(report_instance)

import os
import logging

import pytest

import malevich_space.schema as schema
import malevich_space.constants as constants

from malevich_space.ops import RollerOps
from malevich_space.ops.env import get_active


TEST_COMP_DIR = "./tests/data"


def _get_local_active() -> schema.Setup | None:
    try:
        return get_active(constants.ACTIVE_SETUP_PATH)
    except:
        return None


def _get_from_env() -> schema.Setup | None:
    space_api_url = os.environ.get("TEST_SPACE_API_URL")
    space_username = os.environ.get("TEST_SPACE_USERNAME")
    space_password = os.environ.get("TEST_SPACE_PASSWORD")
    space_token = os.environ.get("TEST_SPACE_TOKEN")
    core_host = os.environ.get("TEST_CORE_CONN_URL")

    assert space_api_url
    assert space_token or (space_username and space_password)

    config = schema.Setup(
        space=schema.SpaceSetup(
            api_url=space_api_url,
            host=schema.HostSchema(conn_url=core_host)
        )
    )

    return config


def _test_roller(comp_dir: str):
    active = _get_local_active()
    if not active:
        active = _get_from_env()
    assert active
    return RollerOps(active, comp_dir=comp_dir, path=comp_dir)


def add_component(roller: RollerOps, reverse_id: str):
    comp = roller.comp_provider.get_by_reverse_id(reverse_id)
    assert comp
    return roller.component(comp, version_mode=schema.VersionMode.MINOR)


@pytest.fixture(scope="session")
def roller():
    logging.info(f"Creating test roller in dir: {TEST_COMP_DIR}")
    return _test_roller(TEST_COMP_DIR)


@pytest.fixture(autouse=True)
def component_cleanup(request, roller):
    reverse_id = request.param
    yield reverse_id
    logging.info(f"Wiping component: {reverse_id}")
    roller.space.wipe_component(reverse_id=reverse_id)

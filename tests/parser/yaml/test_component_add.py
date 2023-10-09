import os
import logging

import pytest

import malevich_space.schema as schema
import malevich_space.constants as constants

from malevich_space.ops import RollerOps
from malevich_space.ops.env import get_active


TEST_COMP_DIR = "./tests/data"
TEST_APP_REVERSE_ID = "test.io.whywhy.rss"
TEST_COLLECTION_REVERSE_ID = "test.io.whywhy.sources"
TEST_FLOW_REVERSE_ID = "test.io.whywhy.preprocess"

TEST_COMPONENTS = [TEST_APP_REVERSE_ID, TEST_COLLECTION_REVERSE_ID, TEST_FLOW_REVERSE_ID]


def _get_local_active() -> schema.Setup | None:
    try:
        return get_active(constants.ACTIVE_SETUP_PATH)
    except:
        return None


def _get_from_env() -> schema.Setup | None:

    print("GETTING FROM ENV: ")
    
    auth_url = os.environ.get("TEST_SPACE_AUTH_URL")
    gql_url = os.environ.get("TEST_SPACE_GQL_URL")
    space_username = os.environ.get("TEST_SPACE_USERNAME")
    space_password = os.environ.get("TEST_SPACE_PASSWORD")
    space_token = os.environ.get("TEST_SPACE_TOKEN")
    core_host = os.environ.get("TEST_CORE_CONN_URL")
    core_username = os.environ.get("TEST_SPACE_SA_USERNAME")
    core_password = os.environ.get("TEST_SPACE_SA_PASSWORD")

    assert auth_url and gql_url
    assert space_token or (space_username and space_password)
    assert core_host and core_username and core_password
    print(core_username, core_password)
    config = schema.Setup(
        space=schema.SpaceSetup(
            auth_url=auth_url,
            gql_url=gql_url,
            host=schema.HostSchema(
                conn_url=core_host,
                sa=schema.SASchema(
                    alias="test",
                    core_username=core_username,
                    core_password=core_password,
                    override=True
                )
            )
        )
    )
    print(config.space)
    return config


def _test_roller(comp_dir: str):
    active = _get_local_active()
    if not active:
        active = _get_from_env()
    assert active
    return RollerOps(active, path=comp_dir)


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


def add_component(roller: RollerOps, reverse_id: str):
    comp = roller.comp_provider.get_by_reverse_id(reverse_id)
    assert comp
    return roller.component(comp, version_mode=schema.VersionMode.MINOR)


@pytest.mark.parametrize("component_cleanup", TEST_COMPONENTS, indirect=True)
def test_component_add(component_cleanup, roller):
    param = component_cleanup
    added: schema.LoadedComponentSchema | None = add_component(roller, param)
    assert added
    assert added.version

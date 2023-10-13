from tests.utility import *


TEST_APP_REVERSE_ID = "test.io.whywhy.rss"
TEST_COLLECTION_REVERSE_ID = "test.io.whywhy.sources"
TEST_FLOW_REVERSE_ID = "test.io.whywhy.preprocess"

TEST_COMPONENTS = [TEST_APP_REVERSE_ID, TEST_COLLECTION_REVERSE_ID, TEST_FLOW_REVERSE_ID]


@pytest.mark.parametrize("component_cleanup", TEST_COMPONENTS, indirect=True)
def test_component_add(component_cleanup, roller):
    param = component_cleanup
    added: schema.LoadedComponentSchema | None = add_component(roller, param)
    assert added
    assert added.version

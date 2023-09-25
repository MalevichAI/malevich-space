from malevich_space.schema import Stand


STAND = Stand.PROD

DEV_SPACE_AUTH_URL = "https://api.onjulius.co/api/v1/login/access-token"
DEV_SPACE_GQL_URL = "https://api.onjulius.co/api/v1/graphql"

PROD_SPACE_AUTH_URL = "https://api.onjulius.co/api/v1/login/access-token"
PROD_SPACE_GQL_URL = "https://api.onjulius.co/api/v1/graphql"

SPACE_AUTH_URL = PROD_SPACE_AUTH_URL if STAND == Stand.PROD else DEV_SPACE_AUTH_URL
SPACE_GQL_URL = PROD_SPACE_GQL_URL if STAND == Stand.PROD else DEV_SPACE_GQL_URL

ACTIVE_SETUP_PATH = "active_space.yaml"

DEFAULT_BRANCH_NAME = "MAIN"
DEFAULT_BRANCH_STATUS = "active"

DEFAULT_VERSION_NAME = "0.1.0"
DEFAULT_VERSION_STATUS = "active"

DEFAULT_VERSION_UPDATE_MD = "It ain't much and it ain't working..."

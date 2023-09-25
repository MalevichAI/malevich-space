from gql import gql


add_cfg_2_av = gql(
    """
    mutation AddCfgToApp($app_id: String!, $cfg_id: String!) {
        app(uid: $app_id) {
            addCfg2Av(input: {
                cfgId: $cfg_id
            }) {
                details {
                    uid
                }
            }
        }
    }
    """
)

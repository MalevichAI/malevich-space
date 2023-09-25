from gql import gql


set_in_flow_comp_cfg = gql(
    """
    mutation SetInFlowCompCfg($flow_id: String!, $comp_id: String!, $cfg_id: String, $cfg_core_id: String) {
        flow(uid: $flow_id) {
            inFlowComponent(uid: $comp_id) {
                updateConfig(cfgId: $cfg_id, cfgCoreId: $cfg_core_id) {
                    details {
                        uid
                    }
                }
            }
        }
    }
    """
)

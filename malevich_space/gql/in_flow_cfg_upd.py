from gql import gql


set_cfg_in_flow = gql(
    """
    query SetCfgInFlow($flow_id: String!, $comp_id: String!, $cfg_id: String!) {
      flow(uid: $flow_id) {
        inFlowComponent(uid: $comp_id) {
          updateConfig(input: $cfg_id) {
            details {
              uid
            }
          }
        }
      }
    }
    """
)

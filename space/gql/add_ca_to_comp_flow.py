from gql import gql


set_ca_in_flow = gql(
    """
    query SetCAInFlow($flow_id: String!, $comp_id: String!, $ca_id: String!, $status: String) {
      flow(uid: $flow_id) {
        inFlowComponent(uid: $comp_id) {
          updateCollectionAlias(input: {
            node: {
            },
            rel: {
              status: $status
            }
            caId: $ca_id
          }) {
            details {
              uid
            }
          }
        }
      }
    }
    """
)

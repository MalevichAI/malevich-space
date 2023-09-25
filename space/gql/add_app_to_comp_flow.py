from gql import gql


set_app_in_flow = gql(
    """
    query SetAppInFlow($flow_id: String!, $comp_id: String!, $app_id: String!, $status: String) {
      flow(uid: $flow_id) {
        inFlowComponent(uid: $comp_id) {
          updateApp(input: {
            node: {
            },
            rel: {
              status: $status
            }
            appId: $app_id
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

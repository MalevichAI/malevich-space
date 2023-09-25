from gql import gql


flow_comp = gql(
    """
    mutation AddFlow($version_id: String!, $is_demo: Boolean, $version_flow: String) {
      version(uid: $version_id) {
        addUnderlyingFlow(
          input: {
            node: {
                isDemo: $is_demo
            },
            rel: {
              status: $version_flow
            }
          }
        ) {
          uid
        }
      }
    }
    """
)

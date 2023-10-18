from gql import gql


get_flow_by_version_id = gql(
    """
    query GetFlowByVersion($version_id: String!) {
      version(uid: $version_id) {
        flow {
          details {
            uid
          }
        }
      }
    }
    """
)

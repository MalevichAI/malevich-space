from gql import gql


ca_comp = gql(
    """
    mutation AddCA($version_id: String!, $ca_id: String!, $version_ca_status: String) {
      version(uid: $version_id) {
        addUnderlyingCa(
          input: {
            nodeId: $ca_id
            rel: {
              status: $version_ca_status
            }
        }
        ) {
          uid
        }
      }
    }
    """
)

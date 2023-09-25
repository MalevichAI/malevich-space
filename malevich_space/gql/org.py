from gql import gql


get_org = gql(
    """
    query GetOrg($reverse_id: String) {
      org(reverseId: $reverse_id) {
        details {
          uid
          name
          reverseId
        }
      }
    }
    """
)

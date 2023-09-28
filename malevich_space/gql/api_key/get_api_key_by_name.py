from gql import gql


api_key_by_name = gql(
    """
    query GetAPIKeyByName($name: String!) {
      apiKey {
        byName(name: $name) {
          details {
            uid
          }
        }
      }
    }
    """
)

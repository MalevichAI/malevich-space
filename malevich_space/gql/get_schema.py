from gql import gql


get_schema = gql(
    """
    query GetSchema($uid: String, $core_id: String) {
      schema(uid: $uid, coreId: $core_id) {
        details {
          uid
          name
          coreId
          raw
        }
      }
    }
    """
)

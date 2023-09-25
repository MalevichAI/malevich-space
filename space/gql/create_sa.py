from gql import gql


sa_create = gql(
    """
    query CreateSA($host_id: String!, $alias: String, $core_username: String, $core_password: String) {
      host(uid: $host_id) {
        createSa(input:{
          node: {
            alias: $alias
            coreUsername: $core_username
            corePassword: $core_password
          }
        }) {
          details {
            uid
            alias
            coreUsername
            corePassword
          }
        }
      }
    }
    """
)

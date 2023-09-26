from gql import gql


get_host = gql(
    """
    query GetHosts($url: String, $sa_core_id: String) {
      user {
        me {
          hosts(url: $url) {
            edges {
              node {
                details {
                  uid
                  alias
                  connUrl
                }
                mySaOnHost(coreId: $sa_core_id) {
                  edges {
                    node {
                      details {
                        uid
                        alias
                        coreUsername
                        corePassword
                      }
                    }
                  }
                }
              }
            }
          }
        }
      }
    }
    """
)

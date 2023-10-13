from gql import gql


get_host = gql(
    """
    query GetHosts($url: String) {
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
                mySaOnHost {
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

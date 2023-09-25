from gql import gql


get_flow = gql(
    """
    query GetFlow($flow_id: String!) {
      flow(uid: $flow_id) {
        details {
          uid
        }
        inFlowComponents {
          edges {
            node {
              details {
                uid
              }
              prompt {
                details {
                  uid
                  name
                  body
                  preconditions
                  postcondition
                }
              }
              prev {
                edges {
                  node {
                    details {
                      uid
                    }
                    prompt {
                        details {
                          uid
                          name
                          body
                          preconditions
                          postcondition
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

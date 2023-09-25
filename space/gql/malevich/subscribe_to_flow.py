from gql import gql


dynamic_flow = gql(
    """
    subscription Subscribe2Flow($flow_id: String!) {
      dynamicInFlow(uid: $flow_id) {
        details {
          uid
        }
        prompt {
          details {
            uid
            body
            preconditions
            preconditions
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
    """
)

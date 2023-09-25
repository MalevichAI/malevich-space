from gql import gql


generate_workflow = gql(
    """
    mutation Generate($pt_id: String!, $thought_id: String!, $sensitivity: Float) {
      malevich {
        pt(uid: $pt_id) {
          generateFlow(finalThoughtFlowUid: $thought_id, matchingConfidence: $sensitivity) {
            edges {
              node {
                details {
                  uid
                }
                inFlowComponents {
                  edges {
                    node {
                      component {
                        details {
                          uid
                          reverseId
                          descriptionMarkdown
                          designedFor
                          notDesignedFor
                          name
                        }
                      }
                      details {
                        uid
                      }
                      flow {
                        details {
                          uid
                        }
                      }
                      collectionAlias {
                        details {
                          uid
                        }
                      }
                      prompt {
                        details {
                          uid
                          name
                          preconditions
                          body
                          postcondition
                        }
                      }
                      app {
                        details {
                          uid
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
    }
    """
)

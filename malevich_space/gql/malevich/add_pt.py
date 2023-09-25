from gql import gql


add_pt_2_malevich = gql(
    """
    mutation AddPT2Malevich($prompt: String!, $max_depth: Int) {
      malevich {
        addPt(input: {
          prompt: {
            body: $prompt
          },
          maxDepth: $max_depth
        }) {
          details {
            uid
          }
          thoughts {
            edges {
              node {
                details {
                  uid
                }
                inFlowComponents {
                  edges {
                    node {
                      prompt {
                        details {
                          uid
                          body
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

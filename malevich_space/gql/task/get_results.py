from gql import gql


get_in_flow_results = gql(
    """
query GetResult($run_id: String!, $in_flow_id: String!) {
  run(uid: $run_id) {
    interCa(inFlowId: $in_flow_id) {
      edges {
        node {
          details {
            uid
          }
          ca {
            coreTable {
              edges {
                node {
                  rawJson
                }
              }
            }
            details {
              coreAlias
              coreId
              uid
            }
            schema {
              details {
                uid
                coreId
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

from gql import gql

subscribe_to_status = gql(
"""
  subscription GetRunStatus($run_id: String!) {
    runStatus(runId: $run_id) {
      app {
        status
        inFlowCompUid
        inFlowAppId
      }
      task {
        status
      }
    }
  }
"""
)


get_run_status = gql(
  """
  query GetRunStatus($run_id: String!) {
    run(uid: $run_id) {
      details {
        uid
        state
      }
      state {
        edges {
          node {
            uid
            alias
          }
          rel {
            status
          }
        }
      }
    }
  }
  """
)

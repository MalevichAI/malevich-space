from gql import gql

subscribe_to_status = gql(
    """
# subscription SubscribeToRunStatus($run_id: String!) {
#   runStatus(runId: $run_id) {
#     app {
#       inFlowCompUid
#       inFlowAppId
#       status
#     }
#   }
# }
subscription GetRunStatus($run_id: String!) {
  runStatus(runId: $run_id) {
    app {
      status
    }
    task {
      status
    }
  }
}
"""
)

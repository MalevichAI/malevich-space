from gql import gql


build_task = gql(
    """
    mutation BuildTask($flow_id: String!, $sa_id: String!) {
      flow(uid: $flow_id) {
        buildCoreTask(saId: $sa_id) {
          details {
            uid
            coreId
          }
        }
      }
    }
    """
)

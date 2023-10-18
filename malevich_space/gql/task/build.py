from gql import gql


build_task = gql(
    """
    mutation BuildTask($flow_id: String!, $host_id: String!, $org_id: String) {
      flow(uid: $flow_id) {
        buildCoreTask(hostId: $host_id, orgId: $org_id) {
          uid
          coreId
        }
      }
    }
    """
)

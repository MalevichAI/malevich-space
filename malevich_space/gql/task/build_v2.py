from gql import gql


build_task_v2 = gql(
    """
    mutation BuildTaskV2($flow_id: String!, $host_id: String!, $org_id: String) {
      flow(uid: $flow_id) {
        buildV2(hostId: $host_id, orgId: $org_id) {
          uid
          coreId
        }
      }
    }
    """
)

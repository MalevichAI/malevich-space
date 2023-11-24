from gql import gql


link_components = gql(
    """
    mutation LinkComponents(
        $flow_id: String!,
        $start_id: String,
        $start_version_id: String,
        $target_id: String,
        $target_version_id: String,
        $schema_adapter_id: String,
        $status: String,
        $as_collection: String,
        $start_terminal_id: String,
        $target_terminal_id: String
        $order: Int
    ) {
      flow(uid: $flow_id) {
        linkComponents(
          input: {
            startUid: $start_id
            startVersionId: $start_version_id
            targetUid: $target_id
            targetVersionId: $target_version_id
            rel: {
              asCollection: $as_collection
              schemaAdapterId: $schema_adapter_id,
              status: $status,
              order: $order
            },
            startTerminalId: $start_terminal_id,
            targetTerminalId: $target_terminal_id
          }
        ) {
          schemaAdapter {
            details {
              uid
            }
          }
        }
      }
    }
    """
)

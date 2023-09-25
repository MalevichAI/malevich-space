from gql import gql


add_schema_alias = gql(
    """
    mutation AddSchemaAlias(
        $flow_id: String!,
        $start_id: String,
        $start_version_id: String,
        $target_id: String,
        $target_version_id: String,
        $src_schema: String!
        $target_schema: String!
    ) {
      flow(uid: $flow_id) {
        addSchemaAlias(
          input: {
            startUid: $start_id
            startVersionId: $start_version_id
            targetUid: $target_id
            targetVersionId: $target_version_id
            srcSchema: $src_schema,
            targetSchema: $target_schema
          }
        ) {
            srcSchema
            targetSchema
        }
      }
    }
    """
)

from gql import gql


create_collection_alias = gql(
    """
    mutation CreateCollectionAlias(
        $sa_id: String!,
        $core_id: String,
        $core_alias: String,
        $schema_core_id: String
    ) {
      collectionAliases {
        create(saId: $sa_id, input: {
          node: {
            coreId: $core_id
            coreAlias: $core_alias
          }
          schemaCoreId: $schema_core_id
        }) {
          details {
            uid
            coreId
          }
        }
      }
    }
    """
)

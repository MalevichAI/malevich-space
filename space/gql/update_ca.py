from gql import gql


update_collection_alias = gql(
    """
    mutation UpdateCA($ca_id: String!, $core_id: String!) {
      collectionAlias(uid: $ca_id) {
        update(input: {
            coreId: $core_id
        }) {
          uid
        }
      }
    }
    """
)

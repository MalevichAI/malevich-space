from gql import gql


tag_to_comp = gql(
    """
    mutation AddTagToComp($comp_id: String!, $tag_ids: [String!]!) {
      component(uid: $comp_id) {
        addTag(tagIds: $tag_ids){
          uid
        }
      }
    }
    """
)

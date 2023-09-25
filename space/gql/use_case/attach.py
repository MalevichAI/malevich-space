from gql import gql


attach_use_case = gql(
    """
    mutation AttachUseCase($comp_uid: String!, $use_case_uid: [String!]!, $designed: Boolean!) {
      component(uid: $comp_uid) {
        attachUseCase(uids: $use_case_uid, designed: $designed) {
          details {
            uid
          }
        }
      }
    }
    """
)

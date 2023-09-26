from gql import gql


branch_by_name = gql(
    """
    query GetBranchByName($component_id: String!, $branch_name: String!) {
      component(uid: $component_id) {
        branches(name: $branch_name) {
          edges {
            node {
              details {
                uid
                name
                createdAt
                status
              }
              activeVersion {
                details {
                  uid
                  readableName
                }
              }
            }
          }
        }
      }
    }
    """
)

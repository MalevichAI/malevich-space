from gql import gql


invite_to_org = gql(
    """
    mutation Invite2Org($reverse_id: String!, $members: [String!]!) {
        org(reverseId: $reverse_id) {
            addUserByEmail(email: $members) {
                ... on StatusInfo {
                    __typename
                    detail
                }
            }
        }
    }
    """
)

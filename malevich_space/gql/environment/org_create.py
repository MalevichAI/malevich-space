from gql import gql


create_org = gql(
    """
    mutation CreateOrg($name: String!, $reverse_id: String!) {
        orgs {
            create(input: {name: $name, reverseId: $reverse_id}) {
            ... on OrgType {
                __typename
                details {
                        uid
                        name
                    }
                }
            }
        }
    }
    """
)

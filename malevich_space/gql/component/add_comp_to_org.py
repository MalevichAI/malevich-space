from gql import gql


comp_to_org = gql(
    """
    mutation AddCompToOrg($comp_id: String!, $org_id: String!) {
        component(uid: $comp_id) {
            addToOrg(orgId: $org_id) {
                details {
                    uid
                }
            }
        }
    }
    """
)

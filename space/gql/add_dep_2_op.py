from gql import gql


add_dep_to_op = gql(
    """
    mutation AddDepToOp($op_id: String!, $dep_key: String!, $dep_type: [String!]!) {
        op(uid: $op_id) {
            addDep(input: {
                node: {
                    key: $dep_key,
                    type: $dep_type
                }
            }) {
                details {
                uid
              }
            }
        }
    }
    """
)

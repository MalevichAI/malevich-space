from gql import gql


add_op_to_av = gql(
    """
    mutation AddOp2Av($app_id: String!, $op_id: String!, $op_type: String!) {
        app(uid: $app_id) {
            addOp2Av(input: {
                nodeId: $op_id,
                rel: {
                    type: $op_type
                }
            }) {
                details {
                    id
                    uid
                }
            }
        }
    }
    """
)

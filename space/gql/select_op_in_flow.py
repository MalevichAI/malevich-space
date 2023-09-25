from gql import gql


select_op = gql(
    """
    mutation SelectOp($flow_id: String!, $comp_id: String!, $op_id: String!, $op_type: String!) {
        flow(uid: $flow_id) {
            inFlowComponent(uid: $comp_id) {
                selectOp(opId: $op_id, opType: $op_type) {
                    details {
                        id
                        uid
                    }
                }
            }
        }
    }
    """
)

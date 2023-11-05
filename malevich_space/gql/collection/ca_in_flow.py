from gql import gql


get_ca_in_flow = gql(
    """
    query MyQuery($flow_id: String!, $in_flow_id: String!) {
        flow(uid: $flow_id) {
            inFlowComponent(uid: $in_flow_id) {
                collectionAlias {
                    collection {
                        details {
                            uid
                        }
                    }
                }
            }
        }
    }
    """
)

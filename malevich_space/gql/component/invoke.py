from gql import gql


invoke_component = gql(
    """
    mutation InvokeComponent(
        $component: String!,
        $branch: String,
        $payload: [InvokeFlowRunPayload!]!,
        $webhook: [String!]
    ) {
        invoke(
            componentId: $component,
            branch: $branch,
            input: {
                webhook: $webhook
                payload: $payload
            }
        ) {
            task {
                details {
                    uid
                }
            }
            run {
                details {
                    uid
                }
            }
        }
    }
    """
)

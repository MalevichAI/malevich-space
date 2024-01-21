from gql import gql


invoke_component = gql(
    """
    mutation InvokeComponent(
        $component: String!,
        $branch: String,
        $payload: [InvokeFlowRunPayload!]!,
        $webhook: [String!],
        $org_id: String
    ) {
        invoke(
            metadata: {
                componentId: $component,
                branchName: $branch
            }
            input: {
                webhook: $webhook
                payload: $payload
            },
            orgId: $org_id
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

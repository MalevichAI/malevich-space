from gql import gql


create_op = gql(
    """
    mutation CreateOp($core_id: String!, $input_schema: [String!], $output_schema: [String!]) {
        ops {
            create(input: {
                coreId: $core_id
                inputSchema: $input_schema
                outputSchema: $output_schema
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

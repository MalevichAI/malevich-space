from gql import gql


create_scheme = gql(
    """
    mutation CreateSchema($core_id: String!, $raw: String!, $name: String) {
        schemas {
            create(input: {
                coreId: $core_id
                raw: $raw,
                name: $name
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

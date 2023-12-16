from gql import gql


get_user_env_secret = gql(
    """
    query GetEnvSecret($env_name: String!, $key: String!) {
        user {
            me {
                env(name: $env_name) {
                    details {
                        uid
                        name
                    }
                    key(raw: $key) {
                        details {
                            uid
                            key
                            value
                        }
                    }
                }
            }
        }
    }
    """
)

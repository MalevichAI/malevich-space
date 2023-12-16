from gql import gql


add_user_env_secret = gql(
    """
    mutation AddEnvSecret($env_name: String!, $key: String!, $value: String!) {
        user {
            me {
                env(name: $env_name) {
                    details {
                        uid
                        name
                    }
                    addSecret(
                        input: {
                            key: $key,
                            value: $value
                        }
                    ) {
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

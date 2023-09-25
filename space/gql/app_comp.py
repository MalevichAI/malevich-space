from gql import gql


app_comp = gql(
    """
    mutation AddApp($version_id: String!, $container_ref: String, $container_user: String, $container_token: String, $version_app_status: String) {
      version(uid: $version_id) {
        addUnderlyingApp(
          input: {
            node: {
                containerRef: $container_ref
                containerUser: $container_user
                containerToken: $container_token
            },
            rel: {
              status: $version_app_status
            }
        }
        ) {
          uid
        }
      }
    }
    """
)

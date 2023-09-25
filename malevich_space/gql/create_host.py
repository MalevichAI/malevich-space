from gql import gql


host_create = gql(
    """
    mutation CreateHost($alias: String!, $conn_url: String!) {
      hosts {
        create(input: {
          node: {
            alias: $alias,
            connUrl: $conn_url
          }
        }) {
          details {
            uid
          }
        }
      }
    }
    """
)

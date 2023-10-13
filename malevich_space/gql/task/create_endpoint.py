from gql import gql


create_task_endpoint = gql(
    """
    mutation CreateTaskEndpoint($task_id: String!, $alias: String, $method: String, $api_key: [String!]!) {
      task(uid: $task_id) {
        createEndpoint(
          input: {
            alias: $alias,
            method: $method
          }
        ) {
          details {
            uid
          }
          addApiKey(apiKeyIds: $api_key) {
            details {
              uid
            }
          }
        }
      }
    }
    """
)

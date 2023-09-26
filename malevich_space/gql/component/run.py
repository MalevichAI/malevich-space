from gql import gql


run_task = gql(
    """
    mutation RunCoreTask($task_id: String!, $raw: String) {
      runWithStatus(
        taskId: $task_id,
        input: {
          raw: $raw
        }
      ) {
        details {
          uid
        }
      }
    }
    """
)

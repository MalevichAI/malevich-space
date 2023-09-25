from gql import gql


change_task_state = gql(
    """
    mutation ChangeTaskState($task_id: String!, $target_state: String!) {
      task(uid: $task_id) {
        changeState(target: $target_state) {
          details {
            uid
          }
        }
      }
    }
    """
)

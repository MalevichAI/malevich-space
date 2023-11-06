from gql import gql


get_task_start_schema = gql(
    """
    query GetTaskStartSchema($task_id: String!) {
      task(uid: $task_id) {
        startSchema {
          inFlowId
          caAlias
          injectedAlias
        }
      }
    }
    """
)

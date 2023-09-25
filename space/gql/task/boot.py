from gql import gql


boot_task = gql(
    """
    mutation BootTask($task_id: String!, $cfgs: [String!], $exec_mode: String) {
      task(uid: $task_id) {
        boot(
          cfgs: $cfgs,
          execMode: $exec_mode
        ) {
          details {
            uid
            bootState
          }
        }
      }
    }
    """
)

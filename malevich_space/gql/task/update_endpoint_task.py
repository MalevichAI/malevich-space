from gql import gql


update_endpoint_in_task = gql(
    """
    mutation UpdateEndpointTask($endpoint_id: String!, $task_id: String!) {
        endpoint(uid: $endpoint_id) {
            updateUnderlyingTask(taskId: $task_id)
        }
    }
    """
)

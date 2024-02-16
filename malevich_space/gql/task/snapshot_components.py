from gql import gql


get_run_snapshot_components = gql(
    """
    query GetRunSnapshotComponents($run_id: String!) {
        run(uid: $run_id) {
            task {
            snapshot {
                inFlowComponents {
                edges {
                    node {
                    details {
                        uid
                        alias
                    }
                    }
                }
                }
            }
            }
        }
    }
    """
)

get_task_snapshot_component = gql(
    """
    query GetTaskSnapshotComponents($task_id: String!) {
        task(uid: $task_id) {
            snapshot {
                inFlowComponents {
                    edges {
                        node {
                            details {
                                uid
                                alias
                            }
                        }
                    }
                }
            }
        }
    }
    """
)

from gql import gql


create_version = gql(
    """
    mutation CreateVersion($branch_id: String!, $readable_name: String!, $branch_version_status: String!, $updates_markdown: String!) {
      branch(uid: $branch_id) {
        createVersion(
          input: {
            node: {
              readableName: $readable_name
              updatesMarkdown: $updates_markdown
            },
            rel: {
              status: $branch_version_status
            }
          }
        ) {
          uid
          readableName
        }
      }
    }
    """
)

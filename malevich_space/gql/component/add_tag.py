from gql import gql


create_tag = gql(
    """
    mutation CreateTag($title: String!) {
      tags {
        create(input: {
          title: $title
        }) {
          details {
            uid
            title
          }
        }
      }
    }
    """
)

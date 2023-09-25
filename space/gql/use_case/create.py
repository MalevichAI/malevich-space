from gql import gql


create_use_case = gql(
    """
    mutation CreateUseCase($body: String, $title: String, $is_public_example: Boolean) {
      useCases {
        create(input: {
          body: $body,
          title: $title,
          isPublicExample: $is_public_example
        }) {
          details {
            uid
          }
        }
      }
    }
    """
)

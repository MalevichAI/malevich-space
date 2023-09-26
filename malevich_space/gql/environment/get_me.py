from gql import gql


get_me = gql(
    """
    query GetMe {
      user {
        me {
          details {
            uid
          }
        }
      }
    }
"""
)

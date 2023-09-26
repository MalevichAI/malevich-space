from gql import gql


wipe_component = gql(
    """
    mutation WipeComponent($uid: String, $reverse_id: String) {
      component(uid: $uid, reverseId: $reverse_id) {
        wipe
      }
    }
    """
)

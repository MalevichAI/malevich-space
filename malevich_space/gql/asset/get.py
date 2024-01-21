from gql import gql


get_asset = gql(
    """
    query GetAsset($uid: String!) {
        asset(uid: $uid) {
            details {
                uid
                corePath
                isComposite
            }
            downloadUrl
            uploadUrl
        }
    }
    """
)

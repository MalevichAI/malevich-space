from gql import gql


create_asset = gql(
    """
    query CreateAsset(
        $core_path: String!,
        $is_composite: Boolean,
        $org_id: String,
        $host_id: String
    ) {
        assets {
            create(
                input: {
                    corePath: $core_path,
                    isComposite: $is_composite
                },
                orgId: $org_id,
                hostId: $host_id
            ) {
                details {
                    uid
                    checksum
                    corePath
                    isComposite
                }
                uploadUrl
            }
        }
    }
    """
)

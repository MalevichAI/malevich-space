from gql import gql


create_asset_in_version = gql(
    """
    mutation CreateAssetInVersion(
        $version_id: String!,
        $core_path: String!,
        $is_composite: Boolean,
        $checksum: String,
        $org_id: String,
        $host_id: String
    ) {
      version(uid: $version_id) {
        createUnderlyingAsset(
          input: {
            node: {
                corePath: $core_path
                isComposite: $is_composite
                checksum: $checksum
            },
            hostId: $host_id
          },
          orgId: $org_id
        ) {
          details {
            uid
            corePath
            checksum
            isComposite
          }
          uploadUrl
        }
      }
    }
    """
)

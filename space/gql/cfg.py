from gql import gql


create_cfg = gql(
    """
    mutation CreateConfig($readable_name: String!, $cfg_json: String!, $core_name: String) {
      configs {
        update(
          input: {
          readableName: $readable_name,
          coreName: $core_name
          cfgJson: $cfg_json
        }) {
          uid
          readableName
        }
      }
    }
    """
)

from gql import gql


create_component = gql(
    """
    mutation CreateComponent(
        $name: String!,
        $type: String!,
        $description: String!,
        $reverse_id: String!,
        $hf_url: String,
        $designed_for: String,
        $not_designed_for: String,
        $visibility: [String!],
        $anticipated_python_deps: [String!],
        $anticipated_default_required_entities: [String!],
        $anticipated_api_call: String,
        $anticipated_api_name: String,
        $org_id: String
    ) {
      components {
        create(
            orgId: $org_id,
            input: {
              name: $name
              type: $type
              descriptionMarkdown: $description,
              reverseId: $reverse_id
              hfUrl: $hf_url,
              designedFor: $designed_for,
              notDesignedFor: $not_designed_for,
              visibility: $visibility,
              anticipatedPythonDeps: $anticipated_python_deps,
              anticipatedDefaultRequiredEntities: $anticipated_default_required_entities,
              anticipatedApiCall: $anticipated_api_call,
              anticipatedApiName: $anticipated_api_name
            }
          ) {
            details {
                uid
                name
                createdAt
              }
            }
        }
    }
    """
)

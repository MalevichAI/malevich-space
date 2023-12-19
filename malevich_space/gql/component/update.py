from gql import gql


update_component = gql(
    """
    mutation UpdateComponent(
        $comp_id: String!,
        $name: String!,
        $description: String,
        $hf_url: String,
        $icon: String,
        $repo_url: String,
        $docs_url: String,
        $designed_for: String,
        $not_designed_for: String,
        $visibility: [String!],
        $anticipated_python_deps: [String!],
        $anticipated_default_required_entities: [String!],
        $anticipated_api_call: String,
        $anticipated_api_name: String
    ) {
      component(uid: $comp_id) {
        update(
            input: {
              name: $name
              descriptionMarkdown: $description,
              hfUrl: $hf_url,
              icon: $icon,
              repoUrl: $repo_url,
              docsUrl: $docs_url,
              designedFor: $designed_for,
              notDesignedFor: $not_designed_for,
              visibility: $visibility,
              anticipatedPythonDeps: $anticipated_python_deps,
              anticipatedDefaultRequiredEntities: $anticipated_default_required_entities,
              anticipatedApiCall: $anticipated_api_call,
              anticipatedApiName: $anticipated_api_name
            }
          ) {
              uid
              name
              createdAt
            }
        }
    }    
    """
)

from gql import gql


add_comp_to_flow = gql(
    """
    mutation AddComponentToFlow(
        $flow_id: String!,
        $target_comp_version_id: String!,
        $flow_comp_status: String,
        $comp_flow_comp_status: String,
        $offset_x: Float,
        $offset_y: Float,
        $alias: String,
        $version_id: String,
        $selected_op: [InFlowSelectedOp!]) {
      flow(uid: $flow_id) {
        addComponent(
          input: {
            node: {
              alias: $alias,
              offsetX: $offset_x,
              offsetY: $offset_y
            },
            rel: {
              status: $flow_comp_status,
              versionId: $version_id
            },
            componentVersionId: $target_comp_version_id,
            componentRel: {
              status: $comp_flow_comp_status
            }
            selectedOp: $selected_op
          }
        ) {
          details {
            uid
          }
        }
      }
    }
    """
)

from gql import gql


get_comp_with_reverse_id = gql(
    """
    query GetComponentByReverseID($reverse_id: String, $uid: String) {
      component(reverseId: $reverse_id, uid: $uid) {
        details {
          uid
          name
          reverseId
          type
          descriptionMarkdown
        }
        activeBranch {
          details {
            uid
            name
            status
          }
        }
        activeBranchVersion {
          details {
            uid
            readableName
            updatesMarkdown
          }
          collection {
            details {
              uid
              coreId
            }
          }
          flow {
            inFlowComponents {
              edges {
                rel {
                  versionId
                }
                node {
                  details {
                    uid
                  }
                  component {
                    details {
                      uid
                      reverseId
                    }
                  }
                  app {
                    details {
                      uid
                    }
                    op(opType: ["input", "processor", "output"]) {
                      edges {
                        node {
                          details {
                            uid
                          }
                        }
                      }
                    }
                  }
                  collectionAlias {
                    details {
                      uid
                    }
                  }
                  flow {
                    details {
                      uid
                    }
                  }
                }
              }
            }
          }
          flow {
            details {
              uid
            }
          }
          app {
            details {
              uid
              containerRef
              containerUser
              containerToken
            }
            avCfg {
              edges {
                node {
                  details {
                    uid
                    cfgJson
                    coreName
                    createdAt
                    readableName
                  }
                }
              }
            }
            avOp(opType: ["input", "processor", "output", "preinit"]) {
              edges {
                node {
                  details {
                    uid
                    coreId
                  }
                  deps {
                    details {
                      uid
                      key
                      type
                    }
                  }
                  inputSchema {
                    details {
                      uid
                      coreId
                    }
                  }
                  outputSchema {
                    details {
                      uid
                      coreId
                    }
                  }
                }
                rel {
                  type
                }
              }
            }
          }
        }
      }
    }
    """
)

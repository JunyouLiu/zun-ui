(function() {
    'use strict';

    angular
      .module('horizon.dashboard.container.bigdataClusters.actions')
      .factory('horizon.dashboard.container.bigdataClusters.actions.workflow2', workflow2);
  
    workflow2.$inject = [
      'horizon.dashboard.container.bigdataClusters.basePath',
      'horizon.framework.util.i18n.gettext'
    ];
  
    function workflow2(basePath, gettext) {
      var workflow2 = {
        init: init
      };
  
      function init(actionType, title, submitText, imageNameList) {
        var schema, form, model;
        var imageNameList = imageNameList || [];
        var imagenames = [];
        var imageValue = '';

        if (imageNameList.length !== 0) {
          imageValue = imageNameList[0];
          for (let i = 0; i < imageNameList.length; i++) {
            var name = imageNameList[i];
            imagenames.push({
              name: gettext(name),
              value: name
            });
          }
        }
        if (actionType === 'update') {
            // schema
            schema = {
                type: "object",
                properties: {
                  // info
                  name: {
                    title: gettext("Name"),
                    type: "string",
                    readonly: actionType === "update"
                  },
                  namespace: {
                    title: gettext("Namespace"),
                    type: "string",
                    readonly: actionType === "update"
                  },
                  pods_number: {
                    title: gettext("Pods number"),
                    type: "string"
                  },
                  'env-name': {
                    title: gettext("Env-name"),
                    type: "string",
                    readonly: actionType === "update"
                  },
                  CPU: {
                    title: gettext("CPU"),
                    type: "string",
                    readonly: actionType === "update"
                  },
                  memory: {
                    title: gettext("Memory"),
                    type: "string",
                    readonly: actionType === "update"
                  },
                }
            };

            // form
            form = [
                {
                    type: "tabs",
                    tabs: [
                      {
                        title: gettext("Info"),
                        //help: basePath + "containers/actions/workflow/info.help.html",
                        type: "section",
                        htmlClass: "row",
                        items: [
                          {
                            type: "section",
                            htmlClass: "col-xs-12",
                            items: [
                              {
                                key: "name",
                                placeholder: gettext("Name of the bigdataCluster to create.")
                              },
                              {
                                key: "namespace",
                                placeholder: gettext("Namespace of the bigdataCluster."),
                              }
                            ]
                          },
                          {
                            type: "section",
                            htmlClass: "col-xs-12",
                            items: [
                              {
                                key: "pods_number",
                                placeholder: gettext("Pods number of the bigdataCluster."),
                              }
                            ]
                          },
                          {
                            type: "section",
                            htmlClass: "col-xs-12",
                            items: [
                              {
                                key: "env-name",
                                placeholder: gettext("The name of env."),
                              }
                            ]
                          },

                          {
                            type: "section",
                            htmlClass: "col-xs-12",
                            items: [
                              {
                                key: "CPU",
                                placeholder: gettext("The number of cpu."),
                              }
                            ]
                          },

                          {
                            type: "section",
                            htmlClass: "col-xs-12",
                            items: [
                               {
                                 key: "memory",
                                 placeholder: gettext("The size of memory , such as:4Gi."),
                               }
                            ]
                          },

                        ]
                      }
                    ]
                  }
            ];

            model = {
                name: "",
                namespace: "",
                pods_number: "",
                action: "property",
                image: "",
                "env-name": "",
                CPU: "",
                memory: ""
            };
        }
        else {
            // schema
            schema = {
                type: "object",
                properties: {
                  // info
                  name: {
                    title: gettext("Name"),
                    type: "string",
                    readonly: actionType === "update"
                  },
                  namespace: {
                    title: gettext("Namespace"),
                    type: "string",
                    readonly: actionType === "update"
                  },
                  pods_number: {
                    title: gettext("Pods number"),
                    type: "string"
                  },
                  image: {
                    title: gettext("Image"),
                    type: "string"
                  },
                  'env-name': {
                    title: gettext("Env-name"),
                    type: "string",
                    readonly: actionType === "update"
                  },
                  CPU: {
                    title: gettext("CPU"),
                    type: "string",
                    readonly: actionType === "update"
                  },
                  memory: {
                    title: gettext("Memory"),
                    type: "string",
                    readonly: actionType === "update"
                  },
                }
            };

            // form
            form = [
                {
                    type: "tabs",
                    tabs: [
                      {
                        title: gettext("Info"),
                        //help: basePath + "containers/actions/workflow/info.help.html",
                        type: "section",
                        htmlClass: "row",
                        items: [
                          {
                            type: "section",
                            htmlClass: "col-xs-12",
                            items: [
                              {
                                key: "name",
                                placeholder: gettext("Name of the bigdataCluster to create.")
                              },
                              {
                                key: "namespace",
                                placeholder: gettext("Namespace of the bigdataCluster."),
                              }
                            ]
                          },
                          {
                            type: "section",
                            htmlClass: "col-xs-12",
                            items: [
                              {
                                key: "pods_number",
                                placeholder: gettext("Pods number of the bigdataCluster."),
                              }
                            ]
                          },

                          {
                            type: "section",
                            htmlClass: "col-xs-12",
                            items: [
                              {
                                key: "image",
                                type: "select",
                                titleMap: imagenames,
                              }
                            ]
                          },

                          {
                            type: "section",
                            htmlClass: "col-xs-12",
                            items: [
                              {
                                key: "env-name",
                                placeholder: gettext("The name of env."),
                              }
                            ]
                          },

                          {
                            type: "section",
                            htmlClass: "col-xs-12",
                            items: [
                              {
                                key: "CPU",
                                placeholder: gettext("The number of cpu."),
                              }
                            ]
                          },

                          {
                            type: "section",
                            htmlClass: "col-xs-12",
                            items: [
                               {
                                 key: "memory",
                                 placeholder: gettext("The size of memory, such as:4Gi."),
                               }
                            ]
                          },

                        ]
                      }
                    ]
                  }
            ];

            model = {
                name: "",
                namespace: "",
                pods_number: "",
                action: "property",
                image: imageValue,
                "env-name": "",
                CPU: "",
                memory: ""
            };
        }
  
        var config = {
          title: title,
          submitText: submitText,
          schema: schema,
          form: form,
          model: model
        };
        return config;
      }
      return workflow2;
    }
  })();
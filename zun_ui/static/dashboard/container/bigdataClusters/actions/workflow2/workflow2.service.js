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
  
      function init(actionType, title, submitText) {
        var schema, form, model;
        var images = [
          {value: "hadoop", name: gettext("hadoop")},
          {value: "hadoop2", name: gettext("hadoop2")}
        ]
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
                title: gettext("env-name"),
                type: "string"
              }
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
                            titleMap: images,
                          }
                        ]
                      },

                      {
                        type: "section",
                        htmlClass: "col-xs-12",
                        items: [
                          {
                            key: "env-name",
                            placeholder: gettext("env's name"),
                          }
                        ]
                      }

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
            image: "hadoop2",
            "env-name": ""
        };
  
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
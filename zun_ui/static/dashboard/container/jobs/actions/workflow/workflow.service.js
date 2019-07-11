(function() {
    'use strict';

    angular
      .module('horizon.dashboard.container.jobs.actions')
      .factory('horizon.dashboard.container.jobs.actions.workflow', workflow);
  
    workflow.$inject = [
      'horizon.dashboard.container.jobs.basePath',
      'horizon.framework.util.i18n.gettext',
      'horizon.app.core.openstack-service-api.zun'
    ];
  
    function workflow(basePath, gettext, zun) {
      var workflow = {
        init: init
      };

      // var clusterNameList = [];
      // // load the list of bigdataCluster
      // function onLoad(response) {
      //   var clusterInfo = response.data['hadoop_cluster_deployment_infos'];  
      //   for (let i = 0; i < clusterInfo.length; i++) {
      //     clusterNameList[i]= clusterInfo[i].name;
      //   }
      // }
      // zun.getBigdataClusters().then(onLoad);

      function init(actionType, title, submitText, clusterNameList) {
        var schema, form, model;
        var clusternames = [];
        for (let i = 0; i < clusterNameList.length; i++) {
          var name = clusterNameList[i];
          clusternames.push({
            name: gettext(name),
            value: name
          });
        }
        var jobtemplates = [
          {value: "wordcount", name: gettext("wordcount")},
          {value: "terasort", name: gettext("terasort")}
        ];

        // schema
        schema = {
            type: "object",
            properties: {
              // info
              jobname: {
                title: gettext("Job name"),
                type: "string"
              },
              clustername: {
                title: gettext("Cluster name"),
                type: "string"
              },
              jobtemplate: {
                title: gettext("Job Template"),
                type: "string"
              },
              inputfile: {
                title: gettext("Input File"),
                type: "string"
              },
              outputfilename: {
                title: gettext("Output File Name"),
                type: "string"
              },
              jar: {
                title: gettext("Jar"),
                type: "string"
              },
              template: {
                title: gettext('Template'),
                type: 'string'
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
                            key: "jobname",
                            placeholder: gettext("Name of the job to create.")
                          },
                          {
                            key: "clustername",
                            type: "select",
                            titleMap: clusternames
                          }
                        ]
                      },
                      {
                        type: "section",
                        htmlClass: "col-xs-12",
                        items: [
                          {
                            key: "jobtemplate",
                            type: "select",
                            titleMap: jobtemplates
                          }
                        ]
                      },
                      {
                        type: 'section',
                        htmlClass: 'col-sm-12',
                        items: [
                          {
                            key: "outputfilename",
                            placeholder: gettext("Name of the output file.")
                          }
                        ]
                      },
                      {
                        type: 'section',
                        htmlClass: 'col-sm-12',
                        items: [
                          {
                            type: 'template',
                            templateUrl: basePath + 'actions/workflow/file-upload.html',
                          }
                        ]
                      }
                    ]
                  }
                ]
            }
        ];

        model = {
          jobname: "",
          clustername: clusternames[0].value,
          jobtemplate: "wordcount",
          outputfilename: "",
          template: ""
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
      return workflow;
    }
  })();
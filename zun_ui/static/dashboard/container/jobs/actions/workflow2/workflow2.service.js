(function() {
    'use strict';

    angular
      .module('horizon.dashboard.container.jobs.actions')
      .factory('horizon.dashboard.container.jobs.actions.workflow2', workflow2);

    workflow2.$inject = [
      'horizon.dashboard.container.jobs.basePath',
      'horizon.framework.util.i18n.gettext',
      'horizon.app.core.openstack-service-api.zun'
    ];

    function workflow2(basePath, gettext, zun) {
      var workflow2 = {
        init: init
      };

      function init(actionType, title, submitText, jobNameList) {
        var schema, form, model;

        var jobnames = [];
        for (let i = 0; i < jobNameList.length; i++) {
          var name = jobNameList[i];
          jobnames.push({
            name: gettext(name),
            value: name
          });
        }

        // schema
        schema = {
            type: "object",
            properties: {
              // info
              jobname: {
                title: gettext("Choose a job to download the outputfile"),
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
                    title: gettext("Download"),
                    type: "section",
                    htmlClass: "row",
                    items: [
                      {
                        type: 'section',
                        htmlClass: 'col-sm-12',
                        items: [
                          {
                            key: "jobname",
                            type: "select",
                            titleMap: jobnames
                          }
                        ]
                      },
                    ]
                  }
                ]
            }
        ];
        if (jobnames.length === 0){
          model = {
            jobname: "",
          };
        }
        else {
          model = {
            jobname: jobnames[0].name,
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
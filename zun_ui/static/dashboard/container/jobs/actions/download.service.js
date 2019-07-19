(function() {
    'use strict';

    angular
      .module('horizon.dashboard.container.jobs.actions')
      .factory('horizon.dashboard.container.jobs.actions.download.service', downloadService);

    downloadService.$inject = [
      'horizon.app.core.openstack-service-api.policy',
      'horizon.app.core.openstack-service-api.zun',
      'horizon.dashboard.container.jobs.actions.workflow2',
      'horizon.dashboard.container.jobs.resourceType',
      'horizon.framework.util.actions.action-result.service',
      'horizon.framework.util.i18n.gettext',
      'horizon.framework.util.q.extensions',
      'horizon.framework.widgets.form.ModalFormService',
      'horizon.framework.widgets.toast.service'
    ];

    function downloadService(
      policy, zun, workflow2, resourceType,
      actionResult, gettext, $qExtensions, modal, toast
    ) {

      var message = {
        success: gettext('Download.')
      };

      var service = {
        initAction: initAction,
        perform: perform,
        allowed: allowed
      };

      return service;

      //////////////

      function initAction() {
      }

      function perform() {
        var title, submitText;
        title = gettext('Download');
        submitText = gettext('Download');
        var jobNameList = [];
        // load the list of bigdataCluster
        function onLoad(response) {
          var jobInfo = response.data['jobs'];  
          for (let i = 0; i < jobInfo.length; i++) {
            jobNameList[i]= jobInfo[i].jobname;
          }
          return jobNameList;
        }
        zun.getJobs().then(onLoad).then(value => {
          var config = workflow2.init('create', title, submitText, value);
          return modal.open(config).then(submit);
        });  
      }

      function allowed() {
        return policy.ifAllowed({ rules: [['job', 'download']] });
      }

      function submit(context) {
        console.log(context.model);
        window.open('http://10.10.87.59/dashboard/project/container/jobs');
        //return zun.downloadFile(context.model, true)
        // return zun.downloadFile(context.model, true).then(success, true);
      }

      function success(response) {
        toast.add('success', interpolate(message.success, [response.data.id]));
        var result = actionResult.getActionResult().created(resourceType, response.data.name);
        return result.result;
      }
    }
  })();
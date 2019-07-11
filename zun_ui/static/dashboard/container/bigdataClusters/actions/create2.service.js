(function() {
    'use strict';

    angular
      .module('horizon.dashboard.container.bigdataClusters.actions')
      .factory('horizon.dashboard.container.bigdataClusters.actions.create2.service', createBigdataClusterService2);
  
    createBigdataClusterService2.$inject = [
      'horizon.app.core.openstack-service-api.policy',
      'horizon.app.core.openstack-service-api.zun',
      'horizon.app.core.openstack-service-api.glance',
      'horizon.dashboard.container.bigdataClusters.actions.workflow2',
      'horizon.dashboard.container.bigdataClusters.resourceType',
      'horizon.framework.util.actions.action-result.service',
      'horizon.framework.util.i18n.gettext',
      'horizon.framework.util.q.extensions',
      'horizon.framework.widgets.form.ModalFormService',
      'horizon.framework.widgets.toast.service'
    ];
  
    function createBigdataClusterService2(
      policy, zun, glance, workflow2, resourceType,
      actionResult, gettext, $qExtensions, modal, toast
    ) {
  
      var message = {
        success: gettext('Request to create bigdataCluster %s has been accepted.')
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
        title = gettext('Create BigdataCluster');
        submitText = gettext('Create');
        var imageNameList = [];
        function onLoad(response) {
          var imageList = response.data.items;
          for (let i = 0; i < imageList.length; i++) {
            imageNameList[i]= imageList[i].name;
          }
          return imageNameList;
        }
        glance.getImages().then(onLoad).then(value => {
          var config = workflow2.init('create', title, submitText, value);
          return modal.open(config).then(submit);
        });
      }
  
      function allowed() {
        return policy.ifAllowed({ rules: [['bigdataCluster', 'create_bigdataCluster']] });
      }
  
      function submit(context) {
        return zun.createBigdataCluster2(context.model, true).then(success, true);
      }
  
      function success(response) {
        console.log(response);
        toast.add('success', interpolate(message.success, [response.data.id]));
        var result = actionResult.getActionResult().created(resourceType, response.data.name);
        return result.result;
      }
    }
  })();
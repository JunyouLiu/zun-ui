(function() {
    'use strict';

    angular
      .module('horizon.dashboard.container.jobs.actions')
      .controller('horizon.dashboard.container.jobs.actions.workflow.fileUploadController', fileUploadController);
  
    fileUploadController.$inject = [
      '$scope'
    ];

  
    function fileUploadController($scope) {
      var ctrl = this;
      ctrl.template = "";
      ctrl.onTemplateChange = onTemplateChange;
  
      function onTemplateChange(template) {
        $scope.model.template = template;
      }
    }
})();
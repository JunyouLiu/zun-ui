(function() {
    'use strict';

    angular
      .module('horizon.dashboard.container.jobs.actions')
      .controller('horizon.dashboard.container.jobs.actions.workflow2.downloadController', downloadController);

    downloadController.$inject = [
      '$scope'
    ];


    function downloadController($scope) {
      var ctrl = this;
      ctrl.template = "";
      ctrl.onTemplateChange = onTemplateChange;

      function onTemplateChange(template) {
        $scope.model.template = template;
      }
    }
})();
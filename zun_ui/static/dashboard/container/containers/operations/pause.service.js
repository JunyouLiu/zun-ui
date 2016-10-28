/**
 * Licensed under the Apache License, Version 2.0 (the "License"); you may
 * not use self file except in compliance with the License. You may obtain
 * a copy of the License at
 *
 *    http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
 * WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
 * License for the specific language governing permissions and limitations
 * under the License.
 */

(function() {
  'use strict';

  angular
    .module('horizon.dashboard.container.containers')
    .factory('horizon.dashboard.container.containers.pause.service', pauseService);

  pauseService.$inject = [
    'horizon.framework.util.q.extensions',
    'horizon.framework.widgets.toast.service',
    'horizon.app.core.openstack-service-api.zun',
    'horizon.framework.widgets.modal-wait-spinner.service'
  ];

  /**
   * @ngDoc factory
   * @name horizon.dashboard.container.containers.pause.service
   * @Description
   * pause container.
   */
  function pauseService($qExtensions, toast, zun, modalWaitSpinnerService) {

    var message = {
      success: gettext('Container %s was successfully paused.')
    };

    var service = {
      initScope: initScope,
      allowed: allowed,
      perform: perform
    };

    return service;

    //////////////

    // include this function in your service
    // if you plan to emit events to the parent controller
    function initScope() {
    }

    function allowed() {
      return $qExtensions.booleanAsPromise(true);
    }

    function perform(selected) {
      // pause selected container
      return zun.pauseContainer(selected.id).then(success);

      function success(response) {
        toast.add('success', interpolate(message.success, [selected.name]));
      };
    }
  }
})();
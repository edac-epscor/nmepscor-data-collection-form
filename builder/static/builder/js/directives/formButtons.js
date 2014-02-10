'use strict';

directives.directive('quitButton', function () {
    return {
        restrict:'E',
        //templateUrl: '/static/builder/partials/quitButton.html'
        template: [
          '<a class="btn btn-danger"',
          'href="#/quit"',
          'ng-click="save(formData)"',
          'tooltip="Save my work, I\'m done for now">Quit</a>'
        ].join(" ")
    };
});

directives.directive('resetButton', function () {
    return {
        restrict:'E',
        //templateUrl: '/static/builder/partials/quitButton.html'
        template: [
          '<a class="btn btn-danger"',
          'ng-click="reset()"',
          'tooltip="Behave as if you have just entered this page">Reset this step</a>'
        ].join(" ")
    };
});

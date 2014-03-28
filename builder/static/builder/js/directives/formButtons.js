'use strict';

directives.directive('quitButton', function () {
    return {
        restrict:'E',
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
        template: [
          '<a class="btn btn-danger"',
          'ng-click="reset()"',
          'tooltip="Behave as if you have just entered this page">Reset this step</a>'
        ].join(" ")
    };
});

directives.directive('nextButton', function($rootScope) {
    return {
        restrict:'E',
        scope: {
            update: '=',
            nextPage: '='
        },
        link: function(scope, elem, attrs){
            scope.nextStep = function(up, ur) {
                $rootScope.nextStep(up, ur);
            };
        },
        template: [
          '<a class="btn btn-primary"',
          'ng-click="nextStep(update, {{url}})"',
          'tooltip="Move forward to the next step">Next Step</a>'
        ].join(" ")
    };
});

'use strict';

/*
 * Directives creating new tags for use.  Should probably namespace
 *
 * We have odd behavior going on with scope, link and transclude, so the
 * desired behavior of being able to write
 *
 *  <step-list record="{{formData.META.id}}" next="#/step2">
 *    Step 2: Files To Document
 *  </step-list>
 *
 *  Is not functioning ...
 *
 */

// a step-list tag. (partials/nav-steps)
//directives.directive('stepList', ['$location', function($location) {
directives.directive('stepList', function() {
    return {
        restrict:'E',
        templateUrl: 'builder/static/builder/js/directives/step-list.html',
        scope: {
            record: '@',
            next: '@',  // copy & update when parent changes, as text/string
            mypath: '@',
            // Below should really be...not needed
            content: '@txt'
        }
        //link: function(scope, element, attrs) {
        //    var record = attrs.record;
        //    var next = attrs.next;
        //    var active = !! record; // cast to bool

        //    scope.active = active;
        //    scope.next = next;

        //    scope.current = attrs.current;

        //    //scope.myPath = $location.path();
        //    //scope.setWell = (scope.myPath == scope.current);
        //},
    };
});

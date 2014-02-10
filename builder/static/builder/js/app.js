'use strict';

// declare top-level module which depends on filters,and services
var epscorForm = angular.module('epscorForm',
    [   'epscorForm.filters',
        'epscorForm.directives', // custom directives
        'xeditable',
        //'controllers',
        'ngGrid', // angular grid
        'ui', // angular ui
        'ngCookies', // cookie support
        'ngSanitize', // for html-bind in ckeditor
        'ui.ace', // ace code editor
        'ui.bootstrap', // jquery ui bootstrap
        '$strap.directives' // angular strap
    ]);


var filters = angular.module('epscorForm.filters', []);
var directives = angular.module('epscorForm.directives', []);

// bootstrap angular
epscorForm.config(['$routeProvider', '$locationProvider', '$httpProvider', function ($routeProvider, $locationProvider, $httpProvider) {

    // TODO use html5 *no hash) where possible
    // $locationProvider.html5Mode(true);

    // App Exploratory Routes
    $routeProvider.when('/', {
        templateUrl:'/static/builder/partials/home.html',
        controller:'homeController'
    });
    $routeProvider.when('/contact', {
        templateUrl:'/static/builder/partials/contact.html'
    });
    $routeProvider.when('/about', {
        templateUrl:'/static/builder/partials/about.html'
    });
    $routeProvider.when('/faq', {
        templateUrl:'/static/builder/partials/faq.html'
    });


    // Form Routes
    $routeProvider.when('/loadForm/:subID', {
        templateUrl:'/static/builder/partials/steps/step0.html',
        controller:'loadController'
    });

    $routeProvider.when('/step0', {
        templateUrl:'/static/builder/partials/steps/step0.html',
        controller: 'submissionsController'
    });

    $routeProvider.when('/step1', {
        templateUrl:'/static/builder/partials/steps/step1.html',
        controller: 's1Form'
    });

    $routeProvider.when('/step2', {
        templateUrl:'/static/builder/partials/steps/step2.html',
        controller: 's2Form'
    });

    $routeProvider.when('/step3', {
        templateUrl:'/static/builder/partials/steps/step3_for_all_ds.html',
        controller: 's3Form'
    });

    $routeProvider.when('/step4', {
        templateUrl:'/static/builder/partials/steps/step4_tagging.html',
        controller: 's4Form'
    });

    // Step 5 varies, if we're in anything *BUT* basic field, it's desc your workflow
    //  if it's field, it's sites...


    $routeProvider.when('/descSites', {
        templateUrl:'/static/builder/partials/steps/descSites.html',
        controller: 'siteForm'
    });

    $routeProvider.when('/descWorkflow', {
        templateUrl:'/static/builder/partials/steps/descWorkflow.html',
        controller: 'workflowForm'
    });

    $routeProvider.when('/descAttributes', {
        templateUrl:'/static/builder/partials/steps/descAttributes.html',
        controller: 'attributeForm'
    });

    $routeProvider.when('/timeInfo', {
        templateUrl:'/static/builder/partials/steps/timeInfo.html',
        controller: 'timeForm'
    });

    $routeProvider.when('/embargo', {
        templateUrl:'/static/builder/partials/steps/embargo.html',
        controller: 'embargoForm'
    });

    $routeProvider.when('/publish', {
        templateUrl:'/static/builder/partials/steps/publish.html',
        controller: 'publishForm'
    });

    $routeProvider.when('/dumpData', {
        templateUrl:'/static/builder/partials/steps/dumpData.html',
        controller: 'longForm'
    });

    // note that to minimize playground impact on app.js, we
    // are including just this simple route with a parameterized
    // partial value (see playground.js and playground.html)
    $routeProvider.when('/playground/:widgetName', {
        templateUrl:'/static/builder/playground/playground.html',
        controller:'PlaygroundCtrl'
    });

    // by default, redirect to site root
    $routeProvider.otherwise({
        redirectTo:'/'
    });

}]);

// this is run after angular is instantiated and bootstrapped
epscorForm.run(function (
        $rootScope,
        $location,
        $http,
        $timeout,
        AuthService,
        SubmissionService,
        RESTService,
        formService,
        editableOptions,
        $modal) {


    // *****
    // Eager load some data using simple REST client
    // *****

    editableOptions.theme = 'bs3';

    $rootScope.progressBar = 1; // visible, > 0

    $rootScope.restService = RESTService;

    //$rootScope.submissions = [];
 
    // async load constants
    $rootScope.constants = [];
    $rootScope.restService.get('/static/builder/data/constants.json', function (data) {
        $rootScope.constants = data[0];
    });

    $rootScope.blankForm = {};
    $rootScope.formData = {};
    $rootScope.restService.get('/static/builder/mock_json/blankForm.json', function(data){
        // blankform holds the uninitialized to full-reset to.
        // formData holds the copy that persists between ng pages.
        $rootScope.blankForm = data;
        $rootScope.formData = angular.copy($rootScope.blankForm); // empty object we'll populate later.
    });

    // TODO move this out to a more appropriate place
    $rootScope.faq = [{
            key: "What is Angular-Enterprise-Seed?",
            alue: "A starting point for server-agnostic, REST based or /static/mashup UI."
        },{
            key: "What are the pre-requisites for running the seed?",
            value: "Just an HTTP server.  Add your own backend."
        },{
            key: "How do I change styling (css)?",
            value: "Change Bootstrap LESS and rebuild with the build.sh script.  This will update the appropriate css/image/font files."
        }
    ];

    /* Navigation Methods */
    $rootScope.go2 = function(path) {
        $location.path(path);
    };

    // Update
    $rootScope.save = function(updated) {
        // Save our step for base reset
        $rootScope.master = angular.copy(updated);
        // Save our form model

        SubmissionService.update(updated, function(data) {
            // This doesn't return anything, but the times
            // are changed...
            //  Unmodal the dialog from nextstep
            $rootScope.formData = data;
            // Rewrite to get updated TS
            $rootScope.spinnerOff();
        });
    };

    // Save and go2 next step
    $rootScope.nextStep = function(updated, newPage) {
        // Modal the dialog
        $rootScope.spinnerOn();
        $rootScope.save(updated);
        $rootScope.go2(newPage);
        // Must unmodal later
    };

    // Reset this step
    $rootScope.reset = function() {
        $rootScope.formData = angular.copy($rootScope.master);
    };

    $rootScope.fullReset = function() {
        $rootScope.formData = angular.copy($rootScope.blankForm);
    };

    $rootScope.spinner = false;
    $rootScope.spinnerOn = function() {
        $rootScope.spinner = true;
        $('#spinner').modal ({
            backdrop: 'static',
            keyboard: true
        }).show();
    };

    $rootScope.spinnerOff = function() {
        $rootScope.spinner = false;
        $('#spinner').modal('hide');
    };

    // *****
    // Initialize authentication
    // *****
    $rootScope.authService = AuthService;

    // text input for login/password (only)
    /*
    $rootScope.loginInput = 'user@gmail.com';
    $rootScope.passwordInput = 'complexpassword';
    */
    $rootScope.loginInput = 'epscor';
    $rootScope.passwordInput = 'changeme';

    $rootScope.$watch('authService.authorized()', function () {

        // if never logged in, do nothing (otherwise bookmarks fail)
        if ($rootScope.authService.initialState()) {
            // we are public browsing
            return;
        }

        // instantiate and initialize an auth notification manager
        $rootScope.authNotifier = new NotificationManager($rootScope);

        // when user logs in, redirect to home
        if ($rootScope.authService.authorized()) {
            $location.path("/");
            $rootScope.authNotifier.notify('success', 'Welcome ' + $rootScope.authService.currentUser() + "!");
            $rootScope.authNotifier.notify('information', $rootScope.authService.loginMsg());

        }

        // when user logs out, redirect to home
        if (!$rootScope.authService.authorized()) {
            // Zero out submissions.
            $location.path("/");
            $rootScope.authNotifier.notify('information', 'Thanks for visiting.  You have been signed out.');
        }

    }, true);

    $rootScope.$watch('authService.numFails()', function() {
        // instantiate and initialize an auth notification manager
        $rootScope.failNotifier = new NotificationManager($rootScope);

        if ( $rootScope.authService.numFails() > 0) {
            $rootScope.failNotifier.notify('error', 'Failed Login');
        }

    }, true);


    // If you aren't logged in, go home.  No matter what.
    $rootScope.$watch(
        // Listener
        function() {
            return $location.path(); 
        }, 
        // Change handler
        function(newValue, oldValue) {
            if ( $rootScope.authService.isLoggedIn() === false && newValue != '/') {
                $location.path('/');
            }
        }
    );

});
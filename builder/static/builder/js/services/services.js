'use strict';

// simple stub that could use a lot of work...
epscorForm.factory('RESTService', function ($http) {
    return {
        get:function (url, callback) {
            return $http({method:'GET', url:url}).
                success(function (data, status, headers, config) {
                    callback(data);
                    //console.log(data.json);
                }).
                error(function (data, status, headers, config) {
                    console.log("failed to retrieve data");
                });
        }
    };
});

// 2x Check that this is used....
epscorForm.factory('formService', function formService($rootScope, $http) {
    var thisForm = null;
    var onStep = 0;

    return {
        init: function() {
            thisForm = angular.copy($rootScope.blankForm);
            return thisForm;
        },
        //just for comma flow
        nothing: function() {
            return null;
        }
    };
});


epscorForm.factory('SubmissionService',
    function ($http, $cookies, $rootScope) {

        var userSubmissions = [];

        return {
            create: function(form, callback) {
                $http({
                    method: 'POST',
                    url: 'submissions/new',
                    data: form
                }).success(function(data, status, headers, config) {
                    console.log("Server created/updated document");
                    callback(data);
                }).
                error(function (data, status, headers, config) {
                    console.log("Failed to make new document");
                });
            },
            list: function(username, callback) {
                return $http({
                    method: 'POST',
                    url: 'submissions/list',
                    data: {
                        'username' : username
                    }
                }).
                success(function (data, status, headers, config) {
                    userSubmissions = data.submissions; // cache
                    callback(data);
                })
                .error(function (data, status, headers, config) {
                    console.log("failed to list");
                });

            },
            update: function(form, callback) {
                $http({
                    method: 'POST',
                    url: 'submissions/update',
                    data: form
                }).success(function(data, status, headers, config) {
                    console.log("Server updated document");
                    callback(data);
                }).
                error(function (data, status, headers, config) {
                    console.log("Failed to update document");
                });
            },
            getById: function(lookupID) {
                // Look up a submission by the id
                //  May have idempotence issues in multi edit
                var found = false;
                var submit = null;
                for(var loop=0; loop < userSubmissions.length; loop ++) {
                    submit = userSubmissions[loop];
                    if (lookupID ==  submit.fullForm.META.id) {
                        found = true;
                        return angular.copy(
                            submit
                        );
                    }
                }
                // What do do if they request an ID they can't have?
            },
            finalize: function(ID, callback) {
                // Mark the form as immutable
                $http({
                    method: 'POST',
                    url: 'submissions/finalize',
                    data: {'id' : ID}
                }).success(function(data, status, headers, config) {
                    console.log("Server finalized document");
                    callback(data);
                }).
                error(function (data, status, headers, config) {
                    console.log("Failed to make new document");
                });
            }
        };
});

// TODO: Drupal/Django HOOK
// simple auth service that can use a lot of work...
epscorForm.factory('AuthService',
    function ($http, $cookies, $rootScope, $location) {
        // Using $cookieStore not seeming to work according to docs, could be
        // old version.  $cookies is an object...so

        var currentUser = null;
        var loginMsg = null;
        var numFailures = 0;

        // Write to this and django will 500
        function getSignedCookie(cname) {
            // Hope it don' have a ":" in it...
            return $cookies[cname].split(":")[0].slice(1);
        }

        $rootScope.authorized = false;
        // If the cookie is set true, we're authorized
        if (_.has($cookies, 'c_authenticated')) {
            // Quote stripping with slice
             $rootScope.authorized = getSignedCookie('c_authenticated') == "True";
             currentUser = getSignedCookie('c_username');
        }

        // initMaybe it wasn't meant to work for mpm?ial state says we haven't logged in or out yet...
        // this tells us we are in public browsing
        var initialState = true;

        // Django CSRF fix
        $http.defaults.csrfCookieName = 'csrftoken';
        $http.defaults.xsrfHeaderName = 'X-CSRFToken';
        $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;

        return {
            initialState:function () {
                return initialState;
            },
            login:function (name, password) {
                // Need CSRF header
                console.log('cookies: + ' + $cookies.text);
                $http.post(
                    'signin',
                    {
                        'username':  name,
                        'password':  password
                    }
                )
                .success(function(data, status, headers, config) {
                    currentUser = name;

                    if (data.status === true) {
                        $rootScope.authorized = true;
                        console.log("Logged in as " + name);
                        loginMsg = data.msg;
                        // Previous modal is not yet dismissed!
                    } else {
                        // Notify ?  How...
                        numFailures = numFailures +1;
                        $rootScope.authorized = false;  // already false
                    }
                    $location.path('/');
                })
                .error(function(data, status, headers, config) {
                    console.log("Failed log in as " + name);
                });

               initialState = false;
                // TODO: XHR ->  username, password
            },
            logout:function () {
                currentUser = null;
                $rootScope.authorized = false;

                $http.get(
                    'logout'
                )
                .success(function(data, status, headers, config) {
                    $location.path('/');
                });
            },
            isLoggedIn:function () {
                return $rootScope.authorized;
            },
            currentUser:function () {
                return currentUser;
            },
            loginMsg:function() {
                return loginMsg;
            },
            numFails:function() {
                return numFailures;
            },
            authorized:function () {
                return $rootScope.authorized;
            },
            keepalive: function() {
                //console.log("KeepAlive request");
                $http.get('keepAlive')
                .success(function() {
                    console.log("KeepAlive request good");
                })
                .error(function() {
                    console.log("KeepAlive request bad");
                });
            }
        };
    }
);

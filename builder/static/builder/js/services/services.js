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
        //var PREFIX = '/builder/';
        var PREFIX = '/';

        return {
            create: function(form, callback) {
                $http({
                    method: 'POST',
                    url: PREFIX + 'submissions/new',
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
                    url: PREFIX + 'submissions/list',
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
                    url: PREFIX + 'submissions/update',
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
                    url: PREFIX + 'submissions/finalize',
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
        var PREFIX = '/';
        //var PREFIX = '/builder/';


        var currentUser = null;
        var loginMsg = null;
        var failMsg = null;
        var numFailures = 0;

        function updateCSRF(value) {
            // Django CSRF fix
            if( typeof value === 'undefined') {
                $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;
            } else {
                $http.defaults.headers.post['X-CSRFToken'] = value;
            }

            $http.defaults.csrfCookieName = 'csrftoken';
            $http.defaults.xsrfHeaderName = 'X-CSRFToken';
            // Using $cookieStore not seeming to work according to docs, could be
            // old version.  $cookies is an object...so
        }

        updateCSRF();

        // Write to this and django will 500
        function getSignedCookie(cname) {
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

        return {
            initialState:function () {
                return initialState;
            },
            login:function (name, password) {
                // Need CSRF header
                console.log('cookies: + ' + $cookies.text);
                $http.post(
                    PREFIX + 'signin',
                    {
                        'username':  name,
                        'password':  password
                    }
                )
                .success(function(data, status, headers, config) {
                    currentUser = name;

                    if (data.status === true) {

                        updateCSRF(data.csrf_token);

                        $rootScope.authorized = true;
                        console.log("Logged in as " + name);
                        loginMsg = data.msg;
                        // Previous modal is not yet dismissed!
                    } else {
                        // Notify ?  How...
                        failMsg = data.msg;
                        numFailures = numFailures +1;
                        $rootScope.authorized = false;  // already false
                    }
                    $location.path('/');
                })
                .error(function(data, status, headers, config) {
                    console.log("Failed log in as " + name);
                    failMsg = data.msg;
                    numFailures = numFailures +1;
                    $rootScope.authorized = false;  // already false
                });

               initialState = false;
                // TODO: XHR ->  username, password
            },
            logout:function () {
                currentUser = null;
                $rootScope.authorized = false;

                $http.get(
                    PREFIX + 'logout'
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
            failMsg:function() {
                return failMsg;
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
                $http.get(PREFIX + 'keepAlive')
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


epscorForm.factory('ProfileService',
    function ($http, $cookies, $rootScope) {

        var PREFIX = '/users';

        // List does not change
        var INSTITUTIONS = [];
        var myProfile = null;


        return {
            getProfile: function() {
                return myProfile;
            },
            getInstitutions: function(callback) {
                return INSTITUTIONS;
            },
            listInstitutions: function(callback) {
                return $http({
                    method: 'GET',
                    url: PREFIX + '/institutions/list'
                }).
                success(function(data, status, headers, config) {
                    INSTITUTIONS = [];
                    for(var loop=0;loop < data.length;loop++) {
                        INSTITUTIONS.push({
                            value: data[loop][0],
                            text: data[loop][1]
                        });
                    }
                    callback(data);
                })
                .error(function (data, status, headers, config) {
                    console.log("failed to list institutions");
                });
            },
            read: function(callback) {
                return $http({
                    method: 'GET',
                    url: PREFIX + '/read'
                }).
                success(function (data, status, headers, config) {
                    myProfile = data.profile; // cache
                    callback(data);
                })
                .error(function (data, status, headers, config) {
                    console.log("failed to list");
                });
            },
            update: function(form, callback) {
                $http({
                    method: 'POST',
                    url: PREFIX + '/update',
                    data: form
                }).success(function(data, status, headers, config) {
                    console.log("Server updated document");
                    myProfile = data.profile;
                    callback(data);
                }).
                error(function (data, status, headers, config) {
                    console.log("Failed to update document");
                });
            },
            deletePI: function(pid, callback) {
                $http({
                    method: 'POST',
                    url: PREFIX + '/pis/delete',
                    data: {'pid' : pid}
                }).success(function(data, status, headers, config) {
                    console.log("Server PI: " + pid);
                    callback(data);
                }).
                error(function (data, status, headers, config) {
                    console.log("Failed to delete PI: " + pid);
                });
            }
        };
});


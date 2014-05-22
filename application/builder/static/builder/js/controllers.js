( function() {

	'use strict';

	/* Controllers */

	//var module = angular.module( 'controllers', [] );
    //


    epscorForm.controller('homeController', function homeController( $rootScope)
    {
        // Zero out form for a brand new clean one
        $rootScope.fullReset(); 
        $rootScope.progressBar = 0;
        $rootScope.authService.keepalive();
    });


    epscorForm.controller('userProfileReadController', function userProfileController(
            $scope,
            ProfileService)
    {

        ProfileService.read(function(data) {
            //callback
            $scope.profile=angular.copy(ProfileService.getProfile());
        });

    });


    // User profile info.  
    epscorForm.controller('userProfileController', function userProfileController(
            $rootScope,
            $scope,
            $location,
            $routeParams,
            $filter,
            ProfileService)
    {
        // TODO:
        //
        //  Some big changes needed.  The profile needs to change to an event
        //  queue, adduser, delete user with save/cancel relaying
        //  corresponding events.

        $rootScope.progressBar = 0;  // Not here..
        // Not actually needed, but looks good
        var userID = $routeParams.userID;

        ProfileService.read(function(data) {
            //callback
            $scope.profile=angular.copy(ProfileService.getProfile());
        });

        ProfileService.listInstitutions(function(data) {
            $scope.INSTITUTION_OPTIONS = ProfileService.getInstitutions();
        });

        ProfileService.listComponents(function(data) {
            $scope.COMPONENT_OPTIONS = ProfileService.getComponents();
        });


        $scope.addRow = function() {
            $scope.profile.investigators.push({
                'id': null,
                'email': null,
                'institution': 'UNM',  // default
                'name': null,
                'component': 'UNKNOWN' // default
            });
        };

        $scope.checkEmail = function(addr, form) {
            // Reuse angular email validator via copy regex.  Need to find a
            // way to call directly
            var eName = 'email';
            var EMAIL_REGEXP = /^[a-z0-9!#$%&'*+/=?^_`{|}~.-]+@[a-z0-9-]+(\.[a-z0-9-]+)*$/i;

            if (EMAIL_REGEXP.test(addr)) {
                form.$setError(eName, '');
                return;
            }
            else {
                var msg = 'Invalid email address';
                form.$setError(eName,  msg);
                return msg;
            }
        };

        $scope.deleteRow = function(recIdx) {
            var myID = $scope.profile.investigators[recIdx].id;
            var needsXHR = myID !== null;
            if (needsXHR) {
                ProfileService.deletePI(myID, function(data) {
                    ;  // Notifier service?
                });
            }
            $scope.profile.investigators.splice(recIdx, 1);
       };

        $scope.saveTable = function() {
            ProfileService.update($scope.profile, function(data) {
                // We'll get back an object with IDs, that we should
                //  then replace the current table with, in case
                //  they now wish to delete something
                $scope.profile = angular.copy(ProfileService.getProfile() );
            });
        };

        $scope.showInstitution = function(pi) {
            var selected = [];
            if(pi.institution) {
                selected = $filter('filter')(
                    $scope.INSTITUTION_OPTIONS, 
                    {value: pi.institution}
                );
            }
            return selected.length ? selected[0].text : 'Not Set';
        };

        $scope.showComponent = function(pi) {
            var selected = [];
            if(pi.component) {
                selected = $filter('filter')(
                    $scope.COMPONENT_OPTIONS, 
                    {value: pi.component}
                );
            }
            return selected.length ? selected[0].text : 'Not Set';
        };
    });


    epscorForm.controller('previewController', function previewController(
            $rootScope,
            $scope,
            $location,
            $routeParams,
            SubmissionService)
    {
        // Todo: need a 'isComplete' to see if this is publishable

        var submissionID = $routeParams.subID;
        $scope.previewData = null;

        SubmissionService.list($rootScope.authService.currentUser(), function(data) {
            // callback
            $scope.previewData = SubmissionService.getById(submissionID).fullForm;
        });

        /*
         * wfStep: previewData.WORKFLOW.steps[i]
         *   maybe make this a directive?
         */
        $scope.selfOrOtherLabel = function(wfStep) {
            var performed = wfStep.performed_by.self;
            if (performed === true) {
                return 'myself';
            }
            var other = wfStep.performed_by.other;

            return other.name + '( at ' + other.institution + ')';
        };

        $scope.go2Publish = function() {
            $location.path( '/publish/' + submissionID);
        };

    });
                


    /*
     *  Given a DS id, load it into our rootform for editing
     */
    epscorForm.controller('loadController', function loadController(
            $rootScope,
            $scope,
            $location,
            $routeParams,
            SubmissionService)
    {
        // Ditch form
        $rootScope.formData = {};
        $rootScope.reset();  // Init form to blank.
        $rootScope.progressBar = 0;

        var sentID = $routeParams.subID;

        // Load provided ID
        $rootScope.formData = SubmissionService.getById(sentID).fullForm;

        // And copy this into the 'master' so reset will work just in 
        // case they ...try to reset before saving
        $rootScope.master = angular.copy($rootScope.formData);

        // Step 1 lets you create a new item...
        $location.path('/step2');

        //var found = false;
        //if (found) {
        //    // Be nice to figure out the step...
        //    $location.path('/step1');
        //}
        // error...
        // TODO: handle not found

    });

    // List of submissions in progress
    epscorForm.controller('submissionsController', function submissionsController(
                $rootScope, $scope, $location, SubmissionService) {

        $rootScope.progressBar = 0;
        $scope.submissionsList = [];

        SubmissionService.list($rootScope.authService.currentUser(),
            function(data) {
                // callback
                for (var i = 0; i< data.submissions.length;i++) {
                    $scope.submissionsList.push(data.submissions[i]);
                    // Copy our view out
                }
            }
        );

        // TODO:  Compute % done, and submitted (?)

        //var schema = $http.get('json/schema.json');
        // This needs to be in a .then...
    });

    epscorForm.controller('s1Form', function s1Form($rootScope, $scope, $location, SubmissionService) {
        //formData is in $rootScope
        $rootScope.progressBar = 10;

        $scope.newDocument = function() {
            SubmissionService.create($rootScope.formData, function(docWithID) {
                // Overwrite model with newdata
                $rootScope.formData = angular.copy(docWithID);
                console.log('Overwrote formData with server document');
                // only on success
                $location.path('/step2');
            });
        };
    });


    //File Add
    epscorForm.controller('s2Form', function s2Form($rootScope, $scope, $location) {
        $rootScope.progressBar = 20;

        // For table info -- hide if type != table
        $scope.hideTableInfo = (
            $rootScope.formData.DESCRIBE.choice != 'table' );

        $scope.addFile = function() {
            //hide
            $rootScope.formData.FILES.datatable.push({
                "file_name": '',
                "tabname": '',
                "title": ''
            });
        };

        // Delete a file from datatable
        $scope.delFile = function(idx) {
            $rootScope.formData.FILES.datatable.splice(idx, 1);
        };
    });


    epscorForm.controller('s3Form', function s3Form($rootScope, $scope, $location) {
        $rootScope.progressBar = 30;
    });


    epscorForm.controller('s4Form', function s4Form($rootScope, $scope, $location) {
        $rootScope.progressBar = 40;
    });


    epscorForm.controller('siteForm', function siteForm($rootScope, $scope, $location) {
        $rootScope.progressBar = 45;

        $scope.ELEVATION_UNITS = [
            "feet",
            "furlongs",
            "meters"
        ];

        $scope.PROJECTIONS = [
            "UTM13N",
            "WGS84"
        ];

        // I Have hereby concluded that formData.SITES is GeoJSON
        $scope.addSite = function() {
            //hide

            $rootScope.formData.SITES.features.push(
                angular.copy($scope.newSite)
            );
            $scope.resetNewSite();
            $scope.addingSite = true;
        };

        $scope.cancelAddSite = function() {
            $scope.resetNewSite();
            $scope.addingSite = false;
        };

        $scope.resetNewSite = function() {
            $scope.newSite = {
                "geometry": {
                    "coordinates": [null, null, null],
                    "type": "Point"
                },
                "properties": {
                    "id": null,
                    "description": null
                },
                "type": "Feature"
            };
        };

        // Delete a file from datatable
        $scope.delSite = function(idx) {
            $rootScope.formData.SITES.features.splice(idx, 1);
        };

        $scope.editSite = function(x,y,z,siteID,desc) {
            $scope.newSite = {
                "geometry": {
                    "coordinates": [x,y,z],
                    "type": "Point"
                },
                "properties": {
                    "id": siteID,
                    "description": desc
                },
                "type": "Feature"
            };
            $scope.addingSite = true;
        };

        $scope.addSiteDialog = function() {
            //todo: DIALOG TIME with a new controller...
            $scope.addingSite = true;

            // $modal.open isn't available and doesn't work.  No clue if it's a flaw in jQuery or angular.js
            //  time to move on and find a fscking solution.
            $scope.resetNewSite();
        };

    });


    epscorForm.controller('workflowForm', function workflowForm($rootScope, $scope, $location) {
        $rootScope.progressBar = 50;

        $scope.addWorkflow = function() {
            //hide

            $rootScope.formData.WORKFLOW.steps.push(
                angular.copy($scope.newWorkflow)
            );
            $scope.resetNewWorkflow();
            $scope.addingWorkflow = false;
        };

        $scope.cancelAddWorkflow = function() {
            $scope.resetNewWorkflow();
            $scope.addingWorkflow = false;
        };

        $scope.resetNewWorkflow = function() {
            $scope.newWorkflow = {
                "date_performed": null,
                "performed_by": {
                    "self": true,
                    "other": {
                        "name": '',
                        "institution": ''
                    }
                },
                "description": ''
            };
        };

        // Clear other info when they hit 'self'
        $scope.checkedSelf = function(value) {
            if(value === true) {
                $scope.newWorkflow.performed_by.other.name = '';
                $scope.newWorkflow.performed_by.other.institution = '';
            }
        };

        // Delete a file from datatable
        $scope.delWorkflow = function(idx) {
            $rootScope.formData.WORKFLOW.steps.splice(idx, 1);
        };

        $scope.editWorkflow = function(desc, dt, slf, name, institution) {
            $scope.newWorkflow = {
                "date_performed": dt,
                "performed_by": {
                    "self": slf,
                    "other": {
                        "name": name,
                        "institution": institution
                    }
                },
                "description": desc
            };
            $scope.addingWorkflow = true;
        };

        $scope.addWorkflowDialog = function() {
            //todo: DIALOG TIME with a new controller...
            $scope.addingWorkflow = true;
            $scope.resetNewWorkflow();
        };
    });


    epscorForm.controller('licenseForm', function licenseForm($rootScope, $scope, $location) {
        $rootScope.progressBar = 85;

        // If the user clears either checkbox we change the request on
        // them back to the default
        $scope.resetRequest = function() {
            if ($rootScope.formData.LICENSE.hasReadCircumstances === false) {
                //unset circumstance we unset your text
                $rootScope.formData.LICENSE.alternate = '';
            }
            if ($rootScope.formData.LICENSE.hasReadDataPolicy === false) {
                // Unset data policy, we unset your everything
                $rootScope.formData.LICENSE.choice = null;
            }
        };

        $scope.canSubmit = function() {
            var form = $rootScope.formData.LICENSE;

            if (! form.hasReadDataPolicy) {
                return false;
            }
            // form.choice == true...
            if(form.choice == 'CCBY_4') {
                return true;
            }
            else if (form.choice == 'other' &&  form.hasReadCircumstances) {
                // Other must agree to circumstances
                if (form.alternate && form.alternate.length > 30) {
                    return true;
                }
                return false;
            }
            else {
                return false;
            }
        };
    });


    epscorForm.controller('embargoForm', function embargoForm(
        $rootScope, 
        $scope, 
        $location,
        $routeParams,
        SubmissionService) 
    {
        $scope.EMBARGO_DURATIONS = [
            "Do Not Embargo"
        ];

        for(var i=1; i<=12; i++) {
            $scope.EMBARGO_DURATIONS.push(i + " Months");
        }

        var submissionID = $routeParams.subID;
        // Load if needed
        $rootScope.formData = SubmissionService.getById(submissionID).fullForm;

        $rootScope.progressBar = 90;

        // If the user clears either checkbox we change the request on
        // them back to the default
        $scope.resetRequest = function() {
            if ($rootScope.formData.EMBARGO.hasReadCircumstances === false) {
                //unset circumstanc,e we unset your text
                $rootScope.formData.EMBARGO.longer = null;
            }
            if ($rootScope.formData.EMBARGO.hasReadDataPolicy === false) {
                // Unset data policy, we unset your everything
                $rootScope.formData.EMBARGO.duration = $scope.EMBARGO_DURATIONS[0];
                $rootScope.formData.EMBARGO.longer = null;
                $rootScope.formData.EMBARGO.hasReadCircumstances = null;
            }
        };
    });


    epscorForm.controller('longForm', function longForm($rootScope, $scope, $location) {
        // TODO: Populate from JSON with stock empty object?
        $rootScope.master = angular.copy($rootScope.formData);
    });

    epscorForm.controller('attributeForm', function attributeForm($rootScope, $scope, $location) {

        $rootScope.progressBar = 60;

        // Blank/New Rows to clone
        
        var ATTRIBUTE_CONFIG = $rootScope.constants.attributeFormConfig;

        // safe alias, choice should never change 
        var TYPE_SELECTED = $scope.formData.DESCRIBE.choice;

        // Handy to F5 the table without loading document.  Should never
        // happen in prod.
        if (TYPE_SELECTED === 'undefined') {
            // Should never really happen though...
            console.log("Setting model type to 'basic' in attribute editor");
            TYPE_SELECTED = 'basic';
        }

        // A quick way to get a reference to the current table
        function getTableAlias() {
            return $rootScope.formData.ATTRIBUTES.userTable[
                TYPE_SELECTED
            ];
        }

        // Once was change table when selectable, now we just build on page load
        // scope.recordList IS the table on the page, but it is a reference
        // here.  Watch that it stays in sync with rootscope.formdata
        function buildTable(typ) {
            $scope.tableInfo = ATTRIBUTE_CONFIG[TYPE_SELECTED];
            $scope.recordList = getTableAlias();
        }

        // default table loaded.  
        buildTable(TYPE_SELECTED); 

        // Filter viewable rows to ones that aren't deleted
        $scope.notDeleted = function(row) {
            return row.isDeleted !== true;
        };

        // Blank Row copied into table model
        $scope.addRow = function() {
            $scope.inserted = angular.copy(
                ATTRIBUTE_CONFIG[TYPE_SELECTED]
            );
            $scope.inserted.isNew = true;
            $scope.recordList.push($scope.inserted);
        };

        $scope.localReset = function() {
            $rootScope.reset(); 
            $scope.recordList = getTableAlias();
        };

        // Cancel button (x), not reset.
        $scope.cancel = function() {
            // Remove all new elements (including new & deleted)
            //    e.g. while non-zero...
            for (var idx= $scope.recordList.length; idx--;) {
                var row = $scope.recordList[idx];

                // undelete
                if (row.isDeleted) {
                    delete row.isDeleted;
                }
                // un-add
                if (row.isNew) {
                    $scope.recordList.splice(idx, 1); // cull
                }
            }
        };

        // TODO: refactor pruner into generating prototype
        //  This method actually does server side update the table, but does
        //  not refresh the 'backup' for the refresh button
        $scope.saveTable= function() {
            var cellVal, found;
            var table = $scope.recordList;

            // backwards for idempotent
            
            var foundNonSparse = false;
            for ( var rowIdx = table.length; rowIdx--;)  {
                var row = table[rowIdx];

                if (row.isDeleted) {
                    table.splice(rowIdx, 1);
                    continue;
                }

                if (row.isNew) {
                    delete row.isNew; // Not new now that we saved it.
                }

                // It's not deleted, it may still be empty... two checks.
                // This way we skip entirely over it the first time we've
                // found non sparse rows
                if(! foundNonSparse) {
                    for(var col = 0; col < row.length; col ++) {
                        cellVal = row[col].value;
                        if (cellVal !== null && cellVal !== '') {
                            foundNonSparse = true;
                            break;
                        }
                    }
                    if(! foundNonSparse) {
                        table.splice(rowIdx, 1);
                        // Frag this row
                    }
                }
            }
            // We have deleted any deleted rows, or empty rows at the end

            // Changes pushed to server on mini save, 
            // no updating restore-copy
            $rootScope.save($rootScope.formData, false); 
        };

        // Purge out an entire row
        $scope.deleteRow = function(recIdx) {
            // find match in recordlist
            $scope.recordList[recIdx].isDeleted = true;
        };
    });


    epscorForm.controller('timeForm', function timeForm($rootScope, $scope, $location) {

        $scope.TIMEZONES = [
            'Mountain',
            'Arizona',
            'UTC',
            'Eastern',
            'Central',
            'Pacific'
        ];
        $scope.tz = $scope.TIMEZONES[0];

        $scope.recordList = $rootScope.formData.TIMEINFO.rows;

        // Blank Row
        $scope.addRow = function() {
            $scope.inserted = {
                'field': null,
                'format': null,
                'timezone': 'Mountain', //default, handy
                'DST': false
            };

            $scope.recordList.push($scope.inserted);
        };

        $rootScope.progressBar =  55;

    });


    epscorForm.controller('publishForm', function publishForm(
            $rootScope, 
            $scope, 
            $location, 
            $routeParams,
            SubmissionService) 
    {

        $rootScope.progressBar = 95;

        var submissionID = $routeParams.subID;

        if (_.isNull(submissionID) && _.isNull($rootScope.formData.META.id)) {
            $.location.path('/');  // Big trouble, log errors, warnings.
        }
        else if (_.isNull($rootScope.formData.META.id)) {

            SubmissionService.list($rootScope.authService.currentUser(), function(data) {
                $rootScope.formData = SubmissionService.getById(submissionID).fullForm;
            });
        }

        // And now... things should not be null...

        $scope.finalize = function(docID) {
            SubmissionService.finalize(docID, function(data) {
                $rootScope.progressBar = 100;
                $.location.path('/step0');  // Back to home
                $rootScope.progressBar = 0;
            });
        };
    });

} )();

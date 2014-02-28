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
                "file_name": "default.file.name.csv",
                "tabname": "DEFAULT_TAB",
                "title": "DEFAULT_FILE_TITLE"
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
                        "name": null,
                        "institution": null
                    }
                },
                "description": null
            };
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

            // $modal.open isn't available and doesn't work.  No clue if it's a flaw in jQuery or angular.js
            //  time to move on and find a fscking solution.
            $scope.resetNewWorkflow();
        };

    });

    epscorForm.controller('embargoForm', function embargoForm($rootScope, $scope, $location) {
        $scope.EMBARGO_DURATIONS = [
            "Do Not Embargo"
        ];

        for(var i=1; i<=12; i++) {
            $scope.EMBARGO_DURATIONS.push(i + " Months");
        }

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

        $scope.ATTRIBUTE_TYPES = [
            "tabular",
            "matrix",
            "gridded"
        ];

        var attributeFormConfig = {
            "tabular": [
                {"value": null, "name": "field", "label": "Field"},
                {"value": null, "name": "description", "label": "Description"},
                {"value": null, "name": "units", "label": "Units"},
                {"value": null, "name": "frequency", "label": "Frequency"},
                {"value": null, "name": "aggregation", "label": "Aggregation"},
                {"value": null, "name": "nodata", "label": "NODATA"},
                {"value": null, "name": "tabs", "label": "Tabs"}
            ],
            "matrix": [
                {"value": null, "name": "dimension", "label": "Dimension"},
                {"value": null, "name": "description", "label": "Description"},
                {"value": null, "name": "units", "label": "Units"},
                {"value": null, "name": "frequency", "label": "Frequency"},
                {"value": null, "name": "aggregation", "label": "Aggregation"},
                {"value": null, "name": "nodata", "label": "NODATA"}
            ],
            "gridded": [
                {"value": null, "name": "band", "label": "Dimension/Band Identifier"},
                {"value": null, "name": "name", "label": "Name"},
                {"value": null, "name": "description", "label": "Description"},
                {"value": null, "name": "units", "label": "Units"},
                {"value": null, "name": "frequency", "label": "Frequency"},
                {"value": null, "name": "aggregation", "label": "Aggregation"},
                {"value": null, "name": "nodata", "label": "NODATA"}
            ]
        };

        $scope.changeTableType = function(typ) {
            $scope.tableInfo = attributeFormConfig[$scope.formData.ATTRIBUTES.typeSelected];
            $scope.recordList = $rootScope.formData.ATTRIBUTES.userTable[
                $scope.formData.ATTRIBUTES.typeSelected
            ];
        };

        // Blank Row
        $scope.addRow = function() {
            $scope.inserted = angular.copy(
                attributeFormConfig[$scope.formData.ATTRIBUTES.typeSelected]
            );

            //records aliases to appropriate master
            $scope.recordList = $rootScope.formData.ATTRIBUTES.userTable[
                $scope.formData.ATTRIBUTES.typeSelected
            ];

            $scope.recordList.push($scope.inserted);
        };

        $scope.saveTable= function() {
            $rootScope.save($rootScope.formData); // Changes pushed to server on mini save
        };

        // User is irrecovably committed to this combination
        $scope.commitChoice = function() {
            var choice = $scope.formData.ATTRIBUTES.typeSelected;
            //tabular, matrix, gridded
            switch (choice) {
                case 'tabular':
                    $scope.formData.ATTRIBUTES.userTable.matrix = [];
                    $scope.formData.ATTRIBUTES.userTable.gridded = [];
                    break;
                case 'matrix':
                    $scope.formData.ATTRIBUTES.userTable.tabular = [];
                    $scope.formData.ATTRIBUTES.userTable.gridded = [];
                    break;
                case 'gridded':
                    $scope.formData.ATTRIBUTES.userTable.tabular = [];
                    $scope.formData.ATTRIBUTES.userTable.matrix = [];
                    break;
            }
            $scope.committed = true;
        };

        // Purge out an entire row
        $scope.deleteAttr = function(recIdx) {
            // find match in recordlist
             $scope.recordList.splice(recIdx, 1);
        };

        $scope.changeTableType("tabular"); // default loaded
        $scope.committed = false;

        $rootScope.progressBar = 60;

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


    epscorForm.controller('publishForm', function attributeForm($rootScope, $scope, $location, SubmissionService) {
        $rootScope.progressBar = 95;
        $scope.finalize = function(docID) {
            SubmissionService.finalize(docID, function(data) {
                $rootScope.progressBar = 100;
                // returns ?
            });
        };
    });

} )();

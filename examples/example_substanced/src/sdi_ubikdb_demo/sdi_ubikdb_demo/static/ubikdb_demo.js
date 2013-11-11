
/* global angular: true, _: true */
/* jshint globalstrict: true */

'use strict';

angular.module('ubikdb_demo', ['ubikDB']).controller('SimpleDemo', function($scope, ubikDB) {

    // define globals for the template
    $scope._ = _;
    $scope.rows = 1;

    // connect to the ubikDB, and bind 2-way sync of variables
    var db = ubikDB();
    db.child('boss').bind($scope, 'boss');
    db.child('agent').bind($scope, 'agent');

});

angular.module('ubikdb_demo').controller('TableDemo', function($scope, ubikDB) {

    // define globals for the template
    $scope._ = _;
    $scope.rows = 1;

    // connect to the ubikDB, and bind 2-way sync of variables
    var db = ubikDB();
    db.child('salary').bind($scope, 'salary');

    $scope.removeFromSalary = function(row) {
        $scope.salary.splice($scope.salary.indexOf(row), 1);
    };

});

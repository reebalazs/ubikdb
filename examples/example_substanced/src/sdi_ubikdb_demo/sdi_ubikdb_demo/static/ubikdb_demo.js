
/* global angular: true, _: true */
/* jshint globalstrict: true */

'use strict';

angular.module('ubikdb_demo', ['ubikDB']).controller('DocumentDemo', function($scope, ubikDB) {

    // define globals for the template
    $scope._ = _;
    $scope.rows = 1;

    // connect to the ubikDB and sync variables
    var db = ubikDB();
    db.child('boss').bind($scope, 'boss');
    db.child('agent').bind($scope, 'agent');

});

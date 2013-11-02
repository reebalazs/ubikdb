
/* global window: true, io: true, angular: true, ubikDB: true */
/* jshint globalstrict: true */

'use strict';

angular.module('ubikdb_demo', []).controller('DocumentDemo', function($scope, $window) {

    // connect to the ubikDB
    var db = ubikDB();

    db.child('boss').on('get', function(value, path) {
        $scope.$apply(function() {
            $scope.boss = value;
        });

    });
    $scope.$watch('boss', function(value, oldValue) {
        // ignore the initial trigger
        if (oldValue !== undefined) {
            db.child('boss').emit('set', value);
        }
    });

    db.child('agent').on('get', function(value, path) {
        $scope.$apply(function() {
            $scope.agent = value;
        });
    });


});

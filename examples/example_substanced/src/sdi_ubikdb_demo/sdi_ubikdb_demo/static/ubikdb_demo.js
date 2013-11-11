
/* global angular: true, _: true */
/* jshint globalstrict: true */

'use strict';

angular.module('ubikdb_demo', ['ubikDB', 'ngRoute']);

angular.module('ubikdb_demo').controller('SimpleDemo', function($scope, ubikDB) {

    // define globals for the template
    $scope.lodash = _;
    $scope.rows = 1;

    // connect to the ubikDB, and bind 2-way sync of variables
    var db = ubikDB();
    db.child('boss').bind($scope, 'boss');
    db.child('agent').bind($scope, 'agent');

});

angular.module('ubikdb_demo').controller('TableDemo', function($scope, ubikDB) {

    // define globals for the template
    $scope._ = _;

    // connect to the ubikDB, and bind 2-way sync of variables
    var db = ubikDB();
    db.child('salary').bind($scope, 'salary');

    $scope.removeFromSalary = function(row) {
        $scope.salary.splice($scope.salary.indexOf(row), 1);
    };

});

angular.module('ubikdb_demo').controller('Selector', function($scope, $location) {
    $scope.isActive = function(route) {
        return route === $location.path();
    }
});

angular.module('ubikdb_demo').config(function($routeProvider) {
    $routeProvider
        .when('/demos/simple', {
            templateUrl: '/static_sdi_ubikdb_demo/partials/simpledemo.html',
            controller: 'SimpleDemo'
        })
        .when('/demos/table', {
            templateUrl: '/static_sdi_ubikdb_demo/partials/tabledemo.html',
            controller: 'TableDemo'
        });

});

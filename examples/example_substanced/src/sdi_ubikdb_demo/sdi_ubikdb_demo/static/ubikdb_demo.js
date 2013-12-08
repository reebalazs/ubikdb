
/* global angular: true, _: true */
/* jshint globalstrict: true */

'use strict';

angular.module('ubikdb_demo', ['ubikDB', 'ngRoute']);

angular.module('ubikdb_demo').controller('SimpleDemo', function($scope, ubikDB) {

    // connect to the ubikDB, and bind 2-way sync of variables
    var db = ubikDB();
    db.child('boss').bind($scope, 'boss');
    db.child('agent').bind($scope, 'agent');

});

angular.module('ubikdb_demo').controller('TableDemo', function($scope, ubikDB) {

    var db = ubikDB();
    db.child('salary').bind($scope, 'salary');

    $scope.removeFromSalary = function(row) {
        $scope.salary.splice($scope.salary.indexOf(row), 1);
    };

});

angular.module('ubikdb_demo').controller('TableZDemo', function($scope, ubikDB) {

    var db = ubikDB('/@@tables', '/ubikdb-z');
    db.child('salary').bind($scope, 'salary');

    $scope.removeFromSalary = function(row) {
        $scope.salary.splice($scope.salary.indexOf(row), 1);
    };

});


angular.module('ubikdb_demo').controller('Selector', function($scope, $location, demos) {

    $scope.demos = demos;

    $scope.isActive = function(route) {
        return route === $location.path();
    };
});


angular.module('ubikdb_demo').controller('Index', function($scope, demos) {
    $scope.demos = demos;
});


angular.module('ubikdb_demo').config(function($routeProvider) {
    $routeProvider
        .when('/demos/demoindex/', {
            templateUrl: '/static_sdi_ubikdb_demo/partials/demoindex.html',
            controller: 'Index'
        })
        .when('/demos/simple/', {
            templateUrl: '/static_sdi_ubikdb_demo/partials/simpledemo.html',
            controller: 'SimpleDemo'
        })
        .when('/demos/table/', {
            templateUrl: '/static_sdi_ubikdb_demo/partials/tabledemo.html',
            controller: 'TableDemo'
        })
        .when('/demos/table-z/', {
            templateUrl: '/static_sdi_ubikdb_demo/partials/tabledemo.html',
            controller: 'TableZDemo'
        });
});

angular.module('ubikdb_demo').factory('demos', function() {
    return [{
        name: 'simple',
        title: 'Simple',
        descr: 'The hello world lf ubikDB: two fields, with memory storage. ' +
               'Its persistence lasts only until the server gets reloaded.'
    }, {
        name: 'table',
        title: 'Table',
        descr: 'List of records represented as a table, with memory storage'
    }, {
        name: 'table-z',
        title: 'table@ZODB',
        descr: 'List of records represented as a table, with ZODB storage as site property'
    }];
});

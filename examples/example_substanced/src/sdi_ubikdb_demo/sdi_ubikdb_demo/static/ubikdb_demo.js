
/* global angular: true, _: true */
/* jshint globalstrict: true */

'use strict';

angular.module('ubikdb_demo', ['ubikDB', 'ngRoute']);

/* demos */

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

angular.module('ubikdb_demo').controller('TableZSiteDemo', function($scope, ubikDB) {

    var db = ubikDB('/@@tables', '/ubikdb-z');
    db.child('salary').bind($scope, 'salary');

    $scope.removeFromSalary = function(row) {
        $scope.salary.splice($scope.salary.indexOf(row), 1);
    };

});

angular.module('ubikdb_demo').controller('TableZContextDemo', function($scope, ubikDB) {

    var db = ubikDB($scope.contextPath + '/@@tables', '/ubikdb-z');
    db.child('salary').bind($scope, 'salary');

    $scope.removeFromSalary = function(row) {
        $scope.salary.splice($scope.salary.indexOf(row), 1);
    };

});

angular.module('ubikdb_demo').controller('LiveTitleDemo', function($scope, ubikDB) {

    // Bind the title attribute of the current page
    var db = ubikDB($scope.contextPath + '/@@/', '/ubikdb-z');
    db.child('title').bind($scope, 'title');

    // Update the real title manually, since it's outside the controller.
    $scope.$watch('title', function(title) {
        document.getElementById('document-title').innerHTML = title;
    });

});

/* Toolbars */

angular.module('ubikdb_demo').controller('Selector', function($scope, $location, demos) {
    $scope.demos = demos();
    $scope.isActive = function(route) {
        return route === $location.path();
    };
});

angular.module('ubikdb_demo').controller('Index', function($scope, demos) {
    $scope.demos = demos();
});


angular.module('ubikdb_demo').config(function($routeProvider, demos) {
    $routeProvider
        .when('/demos/demoindex/', {
            templateUrl: '/static_sdi_ubikdb_demo/partials/demoindex.html',
            controller: 'Index'
        });
    _.each(demos(), function(demo) {
        $routeProvider.when('/demos/' + demo.name + '/', {
            templateUrl: demo.templateUrl,
            controller: demo.controller
        });
    });
});


angular.module('ubikdb_demo').constant('demos', function() {
    var partials = '/static_sdi_ubikdb_demo/partials/';
    return [{
        name: 'hello',
        title: 'Hello',
        descr: 'The hello world lf ubikDB: two fields, with memory storage. ' +
               'Its persistence lasts only until the server gets reloaded.',
        templateUrl: partials + 'simpledemo.html',
        controller: 'SimpleDemo'
    }, {
        name: 'table',
        title: 'Table (volatile)',
        descr: 'List of records represented as a table, with memory storage.',
        templateUrl: partials + 'tabledemo.html',
        controller: 'TableDemo'
    }, {
        name: 'table-zsite',
        title: 'Table in ZODB site',
        descr: 'List of records represented as a table, with ZODB storage as site property.' +
               'This demonstrates a per-site shared storage.',
        templateUrl: partials + 'tablezsitedemo.html',
        controller: 'TableZSiteDemo'
     }, {
        name: 'table-zcontext',
        title: 'Table in context',
        descr: 'List of records represented as a table, with ZODB storage as context property.' +
               'This demonstrate a per-page storage.',
        templateUrl: partials + 'tablezcontextdemo.html',
        controller: 'TableZContextDemo'
     }, {
        name: 'live-title',
        title: 'Live title',
        descr: 'Title is directly linked to the document title in the ZODB.',
        templateUrl: partials + 'livetitledemo.html',
        controller: 'LiveTitleDemo'
   }];

});

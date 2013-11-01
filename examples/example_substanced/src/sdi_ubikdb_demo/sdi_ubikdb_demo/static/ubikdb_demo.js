
/* global window: true, io: true, angular: true */
/* jshint globalstrict: true */

'use strict';

angular.module('ubikdb_demo', []);


angular.module('ubikdb_demo').controller('DocumentDemo', function($scope, $window) {

    // connect to the websocket
    var socket = io.connect('/ubikdb');

    $window.beforeunload = function() {
        socket.disconnect();
    };

    socket.emit('get', '/boss', function(data) {
        $scope.$apply(function() {
            $scope.boss = data;
        });
    });
    socket.emit('get', '/agent', function(data) {
        $scope.$apply(function() {
            $scope.agent = data;
        });
    });

});

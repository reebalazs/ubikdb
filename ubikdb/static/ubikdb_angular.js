
/* global angular: true, ubikDB: true, _: true */
/* jshint globalstrict: true */

'use strict';

angular.module('ubikDB', []).provider('ubikDB', function() {

    function UbikDBAngular() {}

    UbikDBAngular.prototype = new ubikDB.prototype.constructor();
    UbikDBAngular.prototype.constructor = UbikDBAngular;

    UbikDBAngular.prototype.bind = function(scope, name, options) {
        var self = this;
        var lastReceivedValue;
        options = options || {};
        this.on('get', function(value, path) {
            scope.$apply(function() {
                scope[name] = value;
                lastReceivedValue = angular.copy(value);
            });
        });
        if (! options.readonly) {
            scope.$watch(name, function(value, oldValue) {
                // ignore the initial trigger
                // also, avoid circular triggering by
                // never sending back the same value
                if (oldValue !== undefined && ! angular.equals(value, lastReceivedValue)) {
                    self.emit('set', value);
                    lastReceivedValue = null;
                }
            }, true);
        }
    };

    // The same socket is used between all instances.
    var ubikSocket;

    this.$get = function() {
        var ubikDBAngular = function ubikDBAngular(context) {
            var root = new UbikDBAngular();
            root.init(context, ubikSocket);
            ubikSocket = root.socket;
            return root;
        };
        ubikDBAngular.prototype.constructor = UbikDBAngular;
        return ubikDBAngular;
    };

    return this;

});

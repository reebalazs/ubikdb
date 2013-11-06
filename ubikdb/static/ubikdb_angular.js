
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
                scope[name] = lastReceivedValue = value;
            });
        });
        if (! options.readonly) {
            scope.$watch(name, function(value, oldValue) {
                // ignore the initial trigger
                // also, avoid circular triggering by
                // never sending back the same value
                if (oldValue !== undefined && value != lastReceivedValue) {
                    self.emit('set', value);
                    lastReceivedValue = null;
                }
            });
        }
    };

    this.$get = function() {
        return function(context) {
            return new UbikDBAngular(context);
        };
    };

    return this;

});

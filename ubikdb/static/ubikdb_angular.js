
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
            if (value === undefined || value === null) {
                value = []; // XXX XXX XXX temp. collection default
            }
            scope.$apply(function() {
                scope[name] = value;
                lastReceivedValue = angular.copy(value);
            });
        });
        if (! options.readonly) {
            scope.$watch(name, function(value, oldValue) {
                // get rid of $$hashKey
                var clearedValue = angular.copy(value);
                if (clearedValue) {
                    delete clearedValue['$$hashKey'];
                }
                // ignore the initial trigger
                // also, avoid circular triggering by
                // never sending back the same value
                if (oldValue !== undefined &&
                        ! angular.equals(clearedValue, lastReceivedValue)) {
                    if (clearedValue == []) {
                        clearedValue = null; // XXX XXX XXX back from temp. default
                    }
                    self.emit('set', clearedValue);
                    lastReceivedValue = null;
                }
            }, true);
        }
    };

    this.$get = function() {
        var ubikDBAngular = function ubikDBAngular(path, nsName) {
            var root = new UbikDBAngular();
            root.init(path, nsName);
            return root;
        };
        ubikDBAngular.prototype.constructor = UbikDBAngular;
        return ubikDBAngular;
    };

    return this;

});

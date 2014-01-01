
/* global angular: true, ubikDB: true */
/* jshint globalstrict: true */

'use strict';

angular.module('ubikDB', []).provider('ubikDB', function() {

    function UbikDBAngular() {}

    UbikDBAngular.prototype = new ubikDB.prototype.constructor();
    UbikDBAngular.prototype.constructor = UbikDBAngular;

    UbikDBAngular.prototype.bind_readonly = function(scope, name, options) {
        var self = this;
        options = options || {};
        var eBindReadonly = {};
        this.on('watch_context', function(value, path, options) {
            if (value === undefined || value === null) {
                value = []; // XXX XXX XXX temp. collection default
            }
            scope.$apply(function() {
                // Traverse down in memory, in case we got a partial.
                var extraSplit = path.split('/');
                var next = scope;
                var segment = name;
                for (var i=0; i<extraSplit.length; i++) {
                    var nextSegment = extraSplit[i];
                    if (nextSegment !== '') {
                        next = next[segment];
                        segment = nextSegment;
                    }
                }
                // Set the value
                next[segment] = value;
                eBindReadonly.lastReceivedValue = angular.copy(scope[name]);
            });
        });
        return eBindReadonly;
    };

    UbikDBAngular.prototype.bind_default = function(scope, name, options) {
        var self = this;
        var eBindReadonly = this.bind_readonly(scope, name, options);
        eBindReadonly.lastReceivedValue = null;
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
                    ! angular.equals(clearedValue, eBindReadonly.lastReceivedValue)) {
                if (clearedValue == []) {
                    clearedValue = null; // XXX XXX XXX back from temp. default
                }
                self.emit('set', clearedValue);
                eBindReadonly.lastReceivedValue = null;
            }
        }, true);
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

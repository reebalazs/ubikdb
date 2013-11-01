
/* global window: true, io: true */
/* jshint globalstrict: true */

'use strict';

+function() {

    //window.WEB_SOCKET_SWF_LOCATION = "/static/WebSocketMain.swf";
    window.WEB_SOCKET_DEBUG = true;

    function UbikDB(url) {
        this.url = url;
    }

    UbikDB.prototype.init = function() {
        // connect to the websocket
        var socket = this.socket = io.connect('/ubikdb');
        window.beforeunload = function() {
            socket.disconnect();
        };
        this.eventMap = {};
    };

    UbikDB.prototype.trigger = function(type) {
        var method = this['on_' + type];
        return method.apply(this, Array.prototype.slice(arguments, 1));
    };

    UbikDB.prototype.on = function(type) {

    };

    window.UbikDB = function() {
        var ubikDB = new UbikDB(Array.prototype.splice(arguments));
        ubikDB.init();
        return ubikDB;
    };

}();
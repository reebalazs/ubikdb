
/* global window: true, io: true */
/* jshint globalstrict: true */

'use strict';

+function() {

    //window.WEB_SOCKET_SWF_LOCATION = "/static/WebSocketMain.swf";
    window.WEB_SOCKET_DEBUG = true;

    function UbikDB() {}

    UbikDB.prototype.init = function(path, socket) {
        var self = this;
        // connect to the websocket
        if (socket === undefined) {
            this.socket = io.connect('/ubikdb');
        } else {
            // use a socket shared with an instance
            this.socket = socket;
        }
        window.beforeunload = function() {
            self.socket.disconnect();
        };
        this.eventMap = {};
        this.path = path;
    };

    UbikDB.prototype.canonicalPath = function(path) {
        // Return a canonical version of the path.
        // Important for prefix matching.
        path = path.replace(/\/+/g, '/');
        path = path.replace(/^\/|\/$/g,'');
        path = '/' + path;
        return path;
    };

    UbikDB.prototype.child = function(path) {
        var child = new UbikDB();
        path = this.canonicalPath(this.path + '/' + path);
        child.init(path, this.socket);
        return child;
    };

    UbikDB.prototype.trigger = function(type) {
        var method = this['on_' + type];
        return method.apply(this, Array.prototype.slice(arguments, 1));
    };

    UbikDB.prototype.on = function(type, handler) {
        var args = Array.prototype.slice(arguments, 1);
        if (type == 'get') {
            this.socket.emit('get', '/agent', handler);
            this.socket.emit('watch_context', '/my/interest', true);


        } else {
            throw new Error('Unknown event type: ' + type);
        }

    };

    // The same socket is used between all instances.
    var ubikSocket;

    window.UbikDB = function(path) {
        var root = new UbikDB();
        root.init(path, ubikSocket);
        ubikSocket = root.socket;
        return root;
    };

}();
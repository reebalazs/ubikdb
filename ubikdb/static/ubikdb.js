
/* global window: true, io: true */
/* jshint globalstrict: true */

'use strict';

+function() {

    //window.WEB_SOCKET_SWF_LOCATION = "/static/WebSocketMain.swf";
    window.WEB_SOCKET_DEBUG = true;

    function UbikDB() {}

    UbikDB.prototype.constructor = UbikDB;

    UbikDB.prototype.init = function(context, socket) {
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
        this.context = this.canonicalPath(context || '/');
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
        var child = new this.constructor();
        var childContext = this.canonicalPath(this.context + '/' + path);
        child.init(childContext, this.socket);
        return child;
    };

    UbikDB.prototype.bind = function(scope, name, options) {
        throw new Error('Not implemented. Perhaps you wanted to inject ubikDB into Angular?');
    };

    UbikDB.prototype.emit = function(/* type, ... */) {
        // dispatch to respective method
        return this._dispatch('emit', Array.prototype.slice.call(arguments));
    };

    UbikDB.prototype.on = function(/* type, handler, ... */) {
        // dispatch to respective method
        return this._dispatch('on', Array.prototype.slice.call(arguments));
    };

    UbikDB.prototype._dispatch = function(prefix, args) {
        var type = args[0];
        var method = this[prefix + '_' + type];
        if (method === undefined) {
            throw new Error('Unknown event type: ' + type);
        }
        return method.apply(this, args.slice(1));
    };

    UbikDB.prototype.on_get = function(handler) {
        var self = this;
        this.socket.emit('get', this.context, function(value) {
            // call handler with null as second parameter
            // this means this is the initial call
            // and it is always on the same context
            handler(value, null);
        });
        this.socket.emit('watch_context', this.context, {parent: true});
        this.socket.on('set', function(context, value) {
            if (context.indexOf(self.context) === 0) {
                // the event is in the subtree of the current context
                // call handler with the path as second parameter
                var path = context.substring(self.context.length);
                handler(value, path);
            }
        });
    };

    UbikDB.prototype.on_set = function(handler) {
        this.socket.on('set', handler);
    };

    UbikDB.prototype.emit_set = function(value) {
        this.socket.emit('set', this.context, value);
    };

    // The same socket is used between all instances.
    var ubikSocket;

    window.ubikDB = function(context) {
        var root = new UbikDB();
        root.init(context, ubikSocket);
        ubikSocket = root.socket;
        return root;
    };
    window.ubikDB.prototype.constructor = UbikDB;


}();

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
        this.context = this.canonicalPath(path || '/');
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
        var childContext = this.canonicalPath(this.context + '/' + path);
        child.init(childContext, this.socket);
        return child;
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
        this.socket.emit('get', this.context, function(value) {
            // call handler with null as second parameter
            // this means this is the initial call
            // and it is always on the same context
            handler(value, null);
        });
        this.socket.emit('watch_context', this.context, true);
        this.socket.on('changed', function(value, context) {
            if (context.indexOf(this.context) === 0) {
                // the event is in the subtree of the current context
                // call handler with the path as second parameter
                var path = context.substring(this.context.length);
                console.log('changed', value, this.context, path, context);
                handler(value, path);
            }
        });
    };

    // The same socket is used between all instances.
    var ubikSocket;

    window.ubikDB = function(path) {
        var root = new UbikDB();
        root.init(path, ubikSocket);
        ubikSocket = root.socket;
        return root;
    };

}();
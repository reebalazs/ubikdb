
/* global window: true, io: true */
/* jshint globalstrict: true */

'use strict';

+function() {

    //window.WEB_SOCKET_SWF_LOCATION = "/static/WebSocketMain.swf";
    window.WEB_SOCKET_DEBUG = true;

    function Events() {}

    Events.prototype.constructor = Events;

    Events.prototype.init = function() {
        this.events = [];
    };

    Events.prototype.add = function(event) {
        this.events.push(event);
    };

    Events.prototype.remove = function(event) {
        for (var i=0; i<this.events.length; i++) {
            if (this.events[i] == event) {
                this.events.splice(i, 1);
                return;
            }
        }
    };

    Events.prototype.reconnect = function() {
        var events = this.events;
        this.events = [];
        for (var i=0; i<events.length; i++) {
            console.log('reconnect:', i);
            events[i].reconnect();
        }
    };


    function UbikDB() {}

    UbikDB.prototype.constructor = UbikDB;

    UbikDB.prototype.init = function(path, nsNameOrSocket) {
        var self = this;
        if (! nsNameOrSocket) {
            // default namespace, if nothing specified
            // XXX by default, this is _not_ the global namespace.
            nsNameOrSocket = '/ubikdb';
        }
        if (typeof nsNameOrSocket == 'object') {
            // socket passed in from child(), just use it
            this.socket = nsNameOrSocket;
        } else {
            // connect to the websocket
            this.socket = io.connect().of(nsNameOrSocket);
        }
        //window.beforeunload = function() {
        //    self.socket.disconnect();
        //};
        this.path = this.canonicalPath(path || '/');
        this.socket.on('reconnect', function() {
            self.emit('reconnect');
        });
        this.events = new Events();
        this.events.init();
    };

    UbikDB.prototype.socketOn = function(type, handler) {
        var self = this;
        this.socket.on(type, handler);
        return {
            destroy: function() {
                self.socket.removeListener(type, handler);
            }
        };
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
        var childPath = this.canonicalPath(this.path + '/' + path);
        child.init(childPath, this.socket);
        return child;
    };

    UbikDB.prototype.bind = function(scope, name, options) {
        // dispatch to respective method, options.model specifies the type.
        options = options || {};
        options.model = options.model || 'default';
        return this._dispatch('bind', [options.model, scope, name, options]);
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

    UbikDB.prototype.on_watch_context = function(handler) {
        return this._on_watch_context(handler, false);
    };

    UbikDB.prototype._on_watch_context = function(handler, isReconnect) {
        var self = this;
        this.socket.emit('watch_context_and_get', this.path,
            {parent: true, children: true},
            function(value) {
                var options = isReconnect ? {isReconnect: true} : {isFirst: true};
                handler(value, '', options);
            }
        );
        var eSet = this.socketOn('set', function(path, value) {
            if (path.indexOf(self.path) === 0) {
                // the event is in the subtree of the current context
                // call handler with the path as second parameter
                var subPath = path.substring(self.path.length);
                handler(value, subPath, {});
            }
        });
        var eWatchContext = {
            destroy: function(){
                eSet.destroy();
                self.socket.emit('unwatch_context', self.path);
            },
            reconnect: function(){
                eSet.destroy();
                self._on_watch_context(handler, true);
            }
        };
        this.events.add(eWatchContext);
        return eWatchContext;
    };

    UbikDB.prototype.on_set = function(handler) {
        return this.socketOn('set', handler);
    };

    UbikDB.prototype.emit_set = function(value) {
        this.socket.emit('set', this.path, value);
    };

    UbikDB.prototype.emit_reconnect = function() {
        this.events.reconnect();
    };

    window.ubikDB = function(path, nsName) {
        var root = new UbikDB();
        root.init(path, nsName);
        return root;
    };
    window.ubikDB.prototype.constructor = UbikDB;


}();
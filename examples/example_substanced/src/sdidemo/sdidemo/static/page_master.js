
/* global window: true, io: true */
/* jshint globalstrict: true */

'use strict';

+function() {

    // connect to the websocket
    var socket = io.connect('/ubikdb');

    window.beforeunload = function() {
        socket.disconnect();
    };

    socket.on('message', function(context, msg) {
        console.log('message', context, msg);
    });

    socket.on('norecurse', function(context, msg) {
        console.log('norecurse', context, msg);
    });

    socket.emit('watch_context', '/my/interest', true);
    socket.emit('watch_context', '/my/other/interest', false);

    socket.emit('message', '/my/interest', 'Hello Ubik!');
    socket.emit('message', '/my/interest/too', 'Get it because of prefixed.');
    socket.emit('message', '/my/other/interest', 'Unprefixed.');

    socket.emit('message', '/NOSUCH', 'NEVER SEE THIS.');
    socket.emit('message', '/my/other/interest/NOSUCH', 'NEVER SEE THIS prefixed.');

    socket.emit('norecurse', '/my/interest', 'Hello Ubik for a second time!');
    socket.emit('norecurse', '/my/interest/too', 'DO NOT GET THIS, no recursion');
    socket.emit('norecurse', '/my/other/interest', 'Unprefixed, for a second time.');

    // --

    socket.emit('value', '/my/interest', function(data) {
        console.log('value /my/interest', data);
    });
    socket.emit('value', '/boss', function(data) {
        console.log('value /boss', data);
    });
    socket.emit('value', '/agent', function(data) {
        console.log('value /agent', data);
    });

}();
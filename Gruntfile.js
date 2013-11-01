
var collect = require('grunt-collection-helper');

module.exports = function(grunt) {

  // Project configuration.
  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),
    copy: {
      'default': {
        files: {
          'ubik/static/dist/': [
            collect.bower('socket.io-client').path('dist/socket.io.js'),
            collect.bower('socket.io-client').path('dist/WebSocketMainInsecure.swf'),
            collect.bower('socket.io-client').path('dist/WebSocketMain.swf')
          ]
        }
      }
    },
    watch: {
      options: {
        debounceDelay: 250
      },
      'default': {
        files: [
            collect.bower('socket.io-client').path('dist/socket.io.js'),
            collect.bower('socket.io-client').path('dist/WebSocketMainInsecure.swf'),
            collect.bower('socket.io-client').path('dist/WebSocketMain.swf')
        ],
        tasks: ['copy:default']
      }
    }
  });

  // Load the task plugins.
  grunt.loadNpmTasks('grunt-contrib-copy');
  grunt.loadNpmTasks('grunt-contrib-watch');

  // Default task(s).
  grunt.registerTask('default', ['copy:default']);

};

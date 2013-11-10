
var collect = require('grunt-collection-helper');

module.exports = function(grunt) {

  // Project configuration.
  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),
    allThirdParty: [
      collect.bower('socket.io-client').path('dist/socket.io.js'),
      collect.bower('socket.io-client').path('dist/WebSocketMainInsecure.swf'),
      collect.bower('socket.io-client').path('dist/WebSocketMain.swf')
    ],
    shell: {
      install: {
        command: 'node ./node_modules/bower/bin/bower install'
      }
    },
    copy: {
      'default': {
        files: {
          'ubikdb/static/dist/': '<%= allThirdParty %>'
        }
      }
    },
    connect: {
      options: {
        port: 8000,
        base: './app'
      },
      server: {
        options: {
          keepalive: true
        }
      }
    },
    karma: {
      unit: {
        configFile: './test/karma-unit.conf.js',
        autoWatch: false,
        singleRun: true
      },
      unit_auto: {
        configFile: './test/karma-unit.conf.js'
      }
    },

    watch: {
      options: {
        debounceDelay: 250
      },
      'default': {
        files: '<%= allThirdParty %>',
        tasks: ['copy']
      }
    }
  });

  // Load the task plugins.
  grunt.loadNpmTasks('grunt-contrib-copy');
  grunt.loadNpmTasks('grunt-contrib-watch');
  grunt.loadNpmTasks('grunt-contrib-connect');
  grunt.loadNpmTasks('grunt-karma');
  grunt.loadNpmTasks('grunt-shell');

  //installation-related
  grunt.registerTask('install', ['shell:install']);

  //defaults
  grunt.registerTask('default', ['dev']);

  //development
  grunt.registerTask('dev', ['install','copy','watch']);
  grunt.registerTask('server', ['connect:server']);
  grunt.registerTask('test', ['karma:unit']);
  grunt.registerTask('autotest', ['karma:unit_auto']);

};

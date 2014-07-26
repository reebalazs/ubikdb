
var path = require('path');
var phantomjs = require('phantomjs');


// simple helper for locating resources
var _path = function(prefix) {
  return {
    path: function(p) {
      return prefix + '/' + p;
    },
  };
};
var loc = {
  static: _path('ubikdb/static'),
  dist:  _path('ubikdb/static/dist'),
  npm: function(pkg) {
    return _path('node_modules/' + pkg);
  },
  bower: function(pkg) {
    return _path('bower_components/' + pkg);
  },
};

module.exports = function(grunt) {

  var opt = grunt.file.readJSON('etc/development.json');
  var karmaConfig = path.resolve('./frontend-test/karma.conf.js');

  // Project configuration.
  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),
    allThirdParty: [
      loc.bower('socket.io-client').path('dist/socket.io.js'),
      loc.bower('socket.io-client').path('dist/WebSocketMainInsecure.swf'),
      loc.bower('socket.io-client').path('dist/WebSocketMain.swf')
    ],
    mkdir: {
      skeleton: {
        options: {
          mode: 0700,
          create: ['bower_components'],
        },
      },
    },
    bower: {
      install: {
        options: {
          copy: false,
          verbose: true,
        },
      },
    },
    bgShell: {
      'xvfb': {
        cmd: 'Xvfb ' + opt.karmaServerDisplay + ' -ac',
        execOpts: {
        },
        stdout: true,
        stderr: true,
        bg: true,
        fail: false,
      },
      'karma-server': {
        cmd: 'node_modules/karma/bin/karma start ' + karmaConfig + ' --no-single-run',
        execOpts: {
        },
        stdout: true,
        stderr: true,
        bg: true,
        fail: false,
      },
      'deploy-production': {
        cmd: [
          'echo "\nPushing to production..."',
          'git push origin HEAD:production',
        ].join(';'),
        execOpts: {
        },
        stdout: true,
        stderr: true,
        bg: false,
        fail: true,
      }
    },
    env: {
      display: {
        DISPLAY: opt.karmaServerDisplay,
      },
      phantomjs: {
        PHANTOMJS_BIN: phantomjs.path,
      },
    },
    copy: {
      'default': {
        files: {
          'ubikdb/static/dist/': '<%= allThirdParty %>'
        }
      }
    },
    browserSync: {
      server: {
        bsFiles: {
          src: [
            // watch for browser files and templates
            'ubikdb/static/**/*.{pt,js,html,css,png,jpg,gif,tiff}',
            'ubikdb/static/dist/force-reload.stamp',
          ],
        },
        options: {
          open: false,
          watchTask: true,
          ghostMode: {
            clicks: true,
            location: true,
            forms: true,
            scroll: true,
            // links currently coincide with websockets
            links: false,
          },
          port: opt.proxyPort,
          proxy: '127.0.0.1:' + opt.pyramidPort,
          xip: true,
        }
      },
    },
    touch: {
      options: {
        force: true,
        mtime: true
      },
      // force a browser reload
      'force-reload': 'ubikdb/static/dist/force-reload.stamp',
    },
    jshint: {
      options: {
        reporter: require('jshint-stylish'),
      },
      'all': {
        src: 'ubikdb/static/*.js',
      },
    },
    karma: {
      options: {
        configFile: karmaConfig,
      },
      'unit': {
        detectBrowsers: {
          enabled: true,
          usePhantomJS: true
        },
      },
      'unit-phantomjs': {
        browsers: ['PhantomJS'],
      },
      'autounit-phantomjs': {
        autoWatch: true,
        singleRun: false,
        browsers: ['PhantomJS'],
      },
    },
    watch: {
      options: {
        debounceDelay: 50,
        spawn: false,
        atBegin: true,
      },
      'thirdparty': {
        files: '<%= allThirdParty %>',
        tasks: ['copy']
      },
    }
  });

  // Load the task plugins.
  require('load-grunt-tasks')(grunt);

  //installation-related
  grunt.registerTask('install', [
    'mkdir:skeleton',
    'copy',
    'bower:install',
  ]);

  //defaults
  grunt.registerTask('default', [
    'bgShell:karma-server', // needs a few sec to start up, so put this upfront.
    'browserSync',
    'env:phantomjs',
    'watch',
  ]);

  //development
  grunt.registerTask('test', [
    'bgShell:xvfb',
    'env:phantomjs',
    'karma:unit',
  ]);

  // demo related
  grunt.registerTask('demo-install', ['shell:demo-install']);

};

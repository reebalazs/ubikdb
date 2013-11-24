
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
            'install': {
                command: 'node ./node_modules/bower/bin/bower install'
            },
            'demo-serve': {
                command: [
                    'cd examples/example_substanced',
                    'bin/pserve --monitor-restart --pid-file=grunt-demo-serve.pid etc/development.ini'
                ].join(';'),
                options: {
                    stdout: true,
                    stderr: true
                }
            },
            'demo-server-reload': {
                command: [
                    'cd examples/example_substanced',
                    'kill `cat grunt-demo-serve.pid`'
                ].join(';'),
                options: {
                    stdout: true,
                    stderr: true
                }
            }
        },
        copy: {
            'default': {
                files: {
                    'ubikdb/static/dist/': '<%= allThirdParty %>'
                }
            },
            'nothing': {
                files: {
                }
            }
        },
        connect: {
            options: {
                port: 8000,
                base: './app'
            },
            'server': {
                options: {
                    keepalive: true
                }
            }
        },
        karma: {
            'unit': {
                configFile: './test/karma-unit.conf.js',
                autoWatch: false,
                singleRun: true
            },
            'unit-auto': {
                configFile: './test/karma-unit.conf.js'
            }
        },

        watch: {
            options: {
                debounceDelay: 250
            },
            'thirdparty': {
                files: '<%= allThirdParty %>',
                tasks: ['copy']
            },
            'demo-server': {
                files:  [
                    'examples/example_substanced/src/**/*.{py,zcml,conf}',
                    '!examples/example_substanced/src/*/demos/**',
                    '!examples/example_substanced/src/*/examples/**'
                ],
                tasks: ['shell:demo-server-reload']
            },
            'demo-static': {
                files:  [
                    // watch for browser files
                    'examples/example_substanced/src/**/*.{js,pt,html,css,png,jpg}',
                    'ubikdb/**/*.{js,pt,html,css,png,jpg}',
                    // exclusions to decrease number of files to watch unnecessarily
                    '!examples/example_substanced/src/*/node_modules/**',
                    '!examples/example_substanced/src/*/bower_components/**',
                    '!examples/example_substanced/src/*/demos/**',
                    '!examples/example_substanced/src/*/examples/**',
                    // watch for server reloads
                    'examples/example_substanced/grunt-demo-serve.pid'
                ],
                tasks: ['copy:nothing']
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
    grunt.registerTask('dev', ['install', 'copy', 'watch']);
    grunt.registerTask('server', ['connect:server']);
    grunt.registerTask('test', ['karma:unit']);
    grunt.registerTask('autotest', ['karma:unit-auto']);

    // run the demo server (pserve) in foreground
    grunt.registerTask('demo-serve', ['shell:demo-serve']);

};

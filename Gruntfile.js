
var PROXY_PORT = 6540;
var PYRAMID_PORT = 6541;
var LIVERELOAD_PORT = 36540;

var proxySnippet = require('grunt-connect-proxy/lib/utils').proxyRequest;
var lrSnippet = require('connect-livereload')({port: LIVERELOAD_PORT});
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
            'demo-install': {
                command: [
                    'test -f bin/buildout || (',
                        'rm -rf bin lib;',
                        'virtualenv -p python2.7 --no-setuptools .;',
                        'bin/python2.7 bootstrap.py',
                    ');',
                    'bin/buildout'
                ].join(''),
                options: {
                    stdout: true,
                    stderr: true,
                    execOptions: {
                        cwd: 'examples/example_substanced'
                    }
                }
            },
            'demo-server': {
                command: [
                    'bin/pserve --monitor-restart --pid-file=grunt-demo-server.pid etc/development.ini'
                ].join(''),
                options: {
                    stdout: true,
                    stderr: true,
                    execOptions: {
                        cwd: 'examples/example_substanced'
                    }
                }
            },
            'demo-server-reload': {
                command: [
                    'kill `cat grunt-demo-serve.pid`'
                ].join(';'),
                options: {
                    stdout: true,
                    stderr: true,
                    execOptions: {
                        cwd: 'examples/example_substanced'
                    }

                }
            }
        },
        connect: {
            proxies: [{
                context: '/',
                host: 'localhost',
                port: PYRAMID_PORT,
                https: false,
                changeOrigin: false,
                xforward: false
            }],
            'demo-proxy': {
                options: {
                    host: 'localhost',
                    port: PROXY_PORT,
                    middleware: function (connect, options) {
                        return [
                            lrSnippet,
                            proxySnippet
                        ];
                    }
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
                tasks: ['shell:demo-server-reload'],
                options: {
                    livereload: LIVERELOAD_PORT
                }
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
                options: {
                    livereload: LIVERELOAD_PORT
                }
            }

        }
    });

    // Load the task plugins.
    grunt.loadNpmTasks('grunt-contrib-copy');
    grunt.loadNpmTasks('grunt-contrib-watch');
    grunt.loadNpmTasks('grunt-contrib-connect');
    grunt.loadNpmTasks('grunt-connect-proxy');
    grunt.loadNpmTasks('grunt-karma');
    grunt.loadNpmTasks('grunt-shell');

    //installation-related
    grunt.registerTask('install', ['shell:install', 'copy']);

    //defaults
    grunt.registerTask('default', ['dev']);

    //development
    grunt.registerTask('dev', ['install', 'demo-proxy', 'watch']);
    grunt.registerTask('test', ['karma:unit']);
    grunt.registerTask('autotest', ['karma:unit-auto']);

    // demo related
    grunt.registerTask('demo-install', ['shell:demo-install']);
    grunt.registerTask('demo-server', ['shell:demo-server']);
    grunt.registerTask('demo-proxy', ['configureProxies', 'connect:demo-proxy']);

};

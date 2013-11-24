
var collect = require('grunt-collection-helper');

module.exports = function(grunt) {

    // Project configuration.
    grunt.initConfig({
        pkg: grunt.file.readJSON('package.json'),
        allThirdParty: Array.prototype.concat(
            collect.bower('lodash').select('main.js'),
            collect.bower('angular').select('main.js'),
            collect.bower('angular-route').select('main.js')
        ),
        shell: {
            install: {
                command: 'node ./node_modules/bower/bin/bower install'
            }
        },
        copy: {
            'default': {
                files: {
                    'sdi_ubikdb_demo/static/dist/': '<%= allThirdParty %>'
                }
            }
        },
        watch: {
            'default': {
                files:  '<%= allThirdParty %>',
                tasks: ['copy:default']
            }
        }
    });

    // Load the task plugins.
    grunt.loadNpmTasks('grunt-contrib-copy');
    grunt.loadNpmTasks('grunt-contrib-watch');
    grunt.loadNpmTasks('grunt-shell');

    //installation-related
    grunt.registerTask('install', ['shell:install']);

    //defaults
    grunt.registerTask('default', ['dev']);

    //development
    grunt.registerTask('dev', ['install', 'copy', 'serve', 'watch']);

};

var shared = require('./karma-shared.conf');

module.exports = function(config) {
  shared(config);

  config.files = shared.files.concat([
    //extra testing code
    'bower_components/angular-mocks/angular-mocks.js',

    //test files
    './test/unit/*.js'
  ]);
};
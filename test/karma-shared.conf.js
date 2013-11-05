var shared = function(config) {
  config.set({
    basePath: '../',
    frameworks: ['mocha'],
    reporters: ['progress'],
    browsers: ['Firefox'],
    autoWatch: true,

    // these are default values anyway
    singleRun: false,
    colors: true,
  });
};

shared.files = [
  'test/mocha.conf.js',

  //3rd Party Code
  'bower_components/angular/angular.js',

  //App-specific Code
  'ubikdb/static/*.js',

  //Test-Specific Code
  'node_modules/chai/chai.js',
  'test/lib/chai-should.js',
  'test/lib/chai-expect.js'
];

module.exports = shared;

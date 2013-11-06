var shared = function(config) {
  config.set({
    basePath: '../',
    frameworks: ['mocha', 'detectBrowsers'],
    reporters: ['progress'],
    browsers: ['Firefox', 'PhantomJS'],
    autoWatch: true,

    // these are default values anyway
    singleRun: false,
    colors: true,

    // browser detection
    detectBrowsers: {
      enabled: true,
      usePhantomJS: true
    },
    
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

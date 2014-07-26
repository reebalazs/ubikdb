module.exports = function(config) {
  config.set({
    // base path is set back to project root
    basePath: '..',
    files: [
      'frontend-test/mocha.conf.js',
      //3rd Party Code
      'bower_components/angular/angular.js',
      //App-specific Code
      'ubikdb/static/*.js',
      //Test-Specific Code
      'node_modules/chai/chai.js',
      'frontend-test/lib/chai-should.js',
      'frontend-test/lib/chai-expect.js',
      //extra testing code
      'bower_components/angular-mocks/angular-mocks.js',
      //test files
      'frontend-test/unit/*.js'
    ],
    browsers: ['PhantomJS'],
    // Use only ports here that are forwarded by Sauce Connect tunnel.
    // Check usable ports on http://saucelabs.com/docs/connect.
    port: 5050,
    frameworks: ['mocha', 'detectBrowsers', 'chai'],
    reporters: ['progress', 'junit'],
    junitReporter: {
      // this path is relative from the webapp
      outputFile: 'var/unit-test-results.xml',
      suite: 'frontend-unit'
    },
    autoWatch: false,
    singleRun: true,
    colors: true,
    // logLevel: config.LOG_DEBUG,
    detectBrowsers: {
      enabled: false,
    },
    // sauceLabs: {
    // username: 'xxxxx',
    // accessKey: 'xxxxx',
    // startConnect: false,
    // testName: 'iland portal client tests'
    // },
    // define SauceLabs browsers
    customLaunchers: {
      //sauce_chrome_linux: {
      //  base: 'SauceLabs',
      //  browserName: 'chrome',
      //  version: '',
      //  platform: 'linux',
      //}
    }
  });
};

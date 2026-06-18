const Mocha = require('mocha');
const fs = require('fs');
const path = require('path');
const { generateExcelReport } = require('./utils/excelReporter');

// Instantiate a Mocha instance.
const mocha = new Mocha({
    timeout: 30000,
    reporter: 'spec'
});

const testDir = path.join(__dirname, 'tests');

// Add each .js file to the mocha instance
fs.readdirSync(testDir).filter(function(file) {
    // Only keep the .js files
    return file.substr(-3) === '.js';
}).forEach(function(file) {
    mocha.addFile(
        path.join(testDir, file)
    );
});

// Run the tests.
const testResults = [];

const runner = mocha.run(function(failures) {
    process.exitCode = failures ? 1 : 0;  // exit with non-zero status if there were failures
});

runner.on('pass', function(test) {
    testResults.push({
        name: test.title,
        suite: test.parent.title,
        status: 'Pass',
        duration: test.duration,
        error: null
    });
});

runner.on('fail', function(test, err) {
    testResults.push({
        name: test.title,
        suite: test.parent.title,
        status: 'Fail',
        duration: test.duration,
        error: err.message
    });
});

runner.on('end', async function() {
    console.log('Tests completed. Generating Excel report...');
    await generateExcelReport(testResults);
    console.log('Report generation complete.');
});

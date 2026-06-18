const chrome = require('selenium-webdriver/chrome');

/**
 * Returns Chrome options configured for CI/headless environments.
 * In CI (GITHUB_ACTIONS=true or HEADLESS=true) Chrome runs headless.
 */
function getChromeOptions(extraArgs = []) {
    const options = new chrome.Options();
    const isCI = process.env.GITHUB_ACTIONS === 'true' || process.env.HEADLESS === 'true';

    if (isCI) {
        options.addArguments(
            '--headless=new',
            '--no-sandbox',
            '--disable-dev-shm-usage',
            '--disable-gpu',
            '--window-size=1280,1024',
            '--disable-extensions',
            '--disable-setuid-sandbox'
        );
    }

    extraArgs.forEach(arg => options.addArguments(arg));
    return options;
}

module.exports = { getChromeOptions };

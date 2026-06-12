const { Builder, By, until, Key } = require('selenium-webdriver');
const { expect } = require('chai');
const chrome = require('selenium-webdriver/chrome');

// Target URL for live testing
const TARGET_URL = process.env.TARGET_URL || 'https://www.google.com';

describe('End-to-End Web UI Tests (Live)', function () {
  this.timeout(40000); // Increased timeout for live interaction
  let driver;

  before(async function () {
    // Setup Chrome Options
    let options = new chrome.Options();
    // Removed '--headless' so you can see the browser window live!
    options.addArguments('--start-maximized'); 
    options.addArguments('--disable-gpu');
    options.addArguments('--no-sandbox');

    driver = await new Builder()
      .forBrowser('chrome')
      .setChromeOptions(options)
      .build();
  });

  after(async function () {
    if (driver) {
      // Pause briefly so you can see the final state before closing
      await driver.sleep(2000);
      await driver.quit();
    }
  });

  it('TC-E2E-001: Verify live application interaction', async function () {
    try {
      // 1. Navigate to URL
      await driver.get(TARGET_URL);
      
      // Wait for body to be present
      await driver.wait(until.elementLocated(By.css('body')), 10000);
      
      // 2. Sample interaction: If it's Google, let's do a search!
      if (TARGET_URL.includes('google.com')) {
          const searchBox = await driver.findElement(By.name('q'));
          await searchBox.sendKeys('Brain Battle game', Key.RETURN);
          
          // Wait for search results
          await driver.wait(until.elementLocated(By.id('search')), 10000);
      } else {
          // Generic wait
          await driver.sleep(2000);
      }

      const pageTitle = await driver.getTitle();
      expect(pageTitle).to.not.be.undefined;
    } catch (e) {
      console.error(`Failed to load ${TARGET_URL}.`);
      throw e;
    }
  });
});

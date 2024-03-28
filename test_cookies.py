from selenium.webdriver.common.by import By
from selene.core.logger import get_logger
from selene.core.selenium.driver import get_driver, stop_driver
from selene.core.selenium.page import PageSelene
from selene.core.selenium.scripts import script_get_scroll_height, script_expand_all_by_class_name
from selenium.webdriver.common.keys import Keys
import time


def scroll_and_show(driver, width=2560, height=1440):
    # number of scrolls needed to get to bottom
    # total height of page / height of driver
    scrolls = script_get_scroll_height(driver) // height

    # test scrolling with screenshot
    # scrolls until bottom of page
    for n in range(scrolls):
        if n == 0:
            page.screenshot_to_notebook(driver, width, height)
        else:
            page.scroll_to(driver, height * n)
            page.screenshot_to_notebook(driver, width, height)


# +
# initialise driver and logger
driver = get_driver(width=2560, height=1440, headless=False, user_agent='random', use_display=True)
logger = get_logger(level='INFO')

# url and load page
url = 'https://www.amazon.co.uk/'
page = PageSelene.from_url(driver, url, logger=logger)
accept_button = page.find(driver, By.XPATH, '//*[@id="sp-cc-accept"]')
accept_button.click(driver)
# -

scroll_and_show(driver)

# search product
element = page.find(driver, By.CSS_SELECTOR, "input[aria-label='Search Amazon.co.uk']").element
element.send_keys('dehumidifier')
element.send_keys(Keys.RETURN)
page.screenshot_to_notebook(driver, width=2560, height=1440)

# click on any product (find first)
product = page.find(driver, By.CSS_SELECTOR, "a[class='a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal']").element
product.click()
page.screenshot_to_notebook(driver, width=2560, height=1440)

# back to title page
# we should see the "related to items you've viewed" section now
element = page.find(driver, By.CSS_SELECTOR, "div[id='nav-logo']").element
element.click()
scroll_and_show(driver, 1440)



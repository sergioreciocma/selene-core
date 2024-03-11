# %%
from selenium.webdriver.common.by import By
from selene.core.logger import get_logger
from selene.core.selenium.driver import get_driver, stop_driver
from selene.core.selenium.page import PageSelene
from selene.core.selenium.scripts import script_get_scroll_height, script_expand_all_by_class_name

import random
import time

from math import ceil

# %%
# initialise driver and logger
driver = get_driver(width=2560, height=1440)
logger = get_logger(level='INFO')

# url and load page
url = 'https://www.amazon.co.uk/s?k=dehumidifier'
page = PageSelene.from_url(driver, url, logger=logger)

# %%
# accept cookies
accept_button = page.find(driver, By.XPATH, '//*[@id="sp-cc-accept"]')
accept_button.click(driver)

# %%
# expand dropdown
script_expand_all_by_class_name(driver, "a-dropdown-container", "aria-pressed", "true", "a-native-dropdown a-declarative")
page.screenshot_to_notebook(driver)

# %%
# click dropdown button to sort by average rating
sort_button = page.find(driver, By.XPATH, '//*[@id="s-result-sort-select_3"]')
sort_button.click(driver)
page.screenshot_to_notebook(driver)

# %%
# number of scrolls needed to get to bottom
# total height of page / height of driver
scrolls = script_get_scroll_height(driver) // 1440

# %%
# test scrolling with screenshot
# scrolls until bottom of page
for n in range(scrolls):
    if n == 0:
        page.screenshot_to_notebook(driver)
    else:
        page.scroll_to(driver, 1440 * n)
        page.screenshot_to_notebook(driver)

# %%
# test text scraping (all elements in page, no scrolling needed)
driver = get_driver(width=2560, height=1440)
url = 'https://www.amazon.co.uk/s?k=dehumidifier'
page = PageSelene.from_url(driver, url, logger=logger)

# expand dropdown
script_expand_all_by_class_name(driver, "a-dropdown-container", "aria-pressed", "true", "a-native-dropdown a-declarative")
# click dropdown button
sort_button = page.find(driver, By.XPATH, '//*[@id="s-result-sort-select_3"]')
sort_button.click(driver)

results = []
for element in page.find_all(driver, By.CSS_SELECTOR, '[data-component-type="s-search-result"]'):
    results.append(element.text)


# %%
# print results of first page of results
for result in results:
    print(result)
    print('\n')

# %%
url = 'https://www.amazon.co.uk/Dehumidifiers-Dehumidifier-Humidity-Basement-Drainage/product-reviews/B0C8JT1SZ8/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews&pageNumber=2'
page = PageSelene.from_url(driver, url, logger=logger)

page.screenshot_to_notebook(driver)


# %%
def get_ratings_page(page):
    selectors = [
        ('class', 'a-icon a-icon-star a-star-5 review-rating'),
        ('data-hook', 'review-date'),
        ('data-hook', 'review-body')
    ]
    
    results = []
    for selector in selectors:
        s = []
        for element in page.find_all(driver, By.CSS_SELECTOR, f'[{selector[0]}="{selector[1]}"]'):
            if selector[1] == 'a-icon a-icon-star a-star-5 review-rating':
                s.append(element.get_attribute('innerHTML'))
            else:
                s.append(element.text)
        results.append(s)
    return list(zip(*results))
                

get_ratings_page(page)

# %%
n = 0
all_results = []
while True:
    # new driver each iteration does prevent blocking
    driver = get_driver(width=1000, height=2000)
    n += 1
    page_suffix = f'&pageNumber={n}'
    url_pagination = url + page_suffix
    print(url_pagination)
    
    page = PageSelene.from_url(driver, url_pagination, logger=logger)
    
    # some time outs
    time.sleep(random.randint(1, 6))
    
    try:
        page_results = get_ratings_page(page)
        print(page_results)
        print(len(page_results))
        all_results.append(page_results)
    except:
        break


# %%
for n in all_results:
    print(len(n))

# %%
get_ratings_page(page)

# %%
for element in page.find_all(driver, By.CSS_SELECTOR, '[class="a-icon a-icon-star a-star-5 review-rating"]'):
    print(element.get_attribute('innerHTML'))
    print('\n')

# %%
for element in page.find_all(driver, By.CSS_SELECTOR, '[data-hook="review-body"]'):
    print(element.text)
    print('\n')

# %%


# import dependencies
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# path to chrome driver
chrome_path = "/home/vvats/Downloads/chromedriver"
driver = webdriver.Chrome(chrome_path)

# open amazon site
driver.get("https://www.amazon.in/")

# search for Dell 24 inch monitor
search_query = driver.find_element_by_id("twotabsearchtextbox")
search_query.send_keys("Dell Monitor 24 Inch Full HD")
search_query.send_keys(Keys.RETURN)

# get all the monitor title and prices
#data = driver.find_elements_by_css_selector("a.a-link-normal.s-access-detail-page.s-color-twister-title-link.a-text-normal")
data = driver.find_elements_by_xpath("//div[@class='a-fixed-left-grid-col a-col-right']")

monitors = driver.find_elements_by_xpath("//*[@class='a-link-normal s-access-detail-page  s-color-twister-title-link a-text-normal']")
prices = driver.find_elements_by_xpath("//*[@class='a-size-base a-color-price s-price a-text-bold' or @class='a-size-base a-color-price a-text-bold']")

for monitor in monitors:
    print(monitor.text)

for price in prices:
    print(price.text)

# print the monitor names
if len(data) < 0:
    print(len(data))
    for monitor in data:
        # todo fetch monitor title and price
        monitor_title = monitor.find_element_by_xpath("//*[@class='a-link-normal s-access-detail-page  s-color-twister-title-link a-text-normal']").text
        #monitor_price = monitor.find_element_by_class_name("a-size-base.a-color-price.s-price.a-text-bold").text
        print(monitor_title)

import time
from selenium import webdriver
import pandas as pd
from selenium.webdriver.common.keys import Keys

class bcolors:
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    RED = '\033[91m'
    ENDC = '\033[0m'

# Getting the booking Amsterdam hotels url
url = 'https://www.hotels.com/search.do?destination-id=934558&q-check-in=2021-10-25&q-check-out=2021-10-26&q-rooms=1&q-room-0-adults=2&q-room-0-children=0&sort-order=BEST_SELLER&pos=HCOM_US&locale=en_US'

# Deleting errors in the chrome connection
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome('../drivers/chromedriver.exe', options=options)

# Opening the browser
driver.get(url)

print('STARTING THE SCRAPE...')

body = driver.find_element_by_css_selector('body')

for i in range(25):
    body.send_keys(Keys.PAGE_DOWN)
    time.sleep(1)


hotels = driver.find_elements_by_class_name('_61P-R0')

urls = []
for hotel in hotels:
    urls.append(hotel.get_attribute('href'))

data = []
i = 0
print(len(hotels))
for hotel in hotels:
    j = 1
    hotel_url = urls[i]
    i += 1
    driver.get(hotel_url)
    hotel_name = driver.find_element_by_xpath('//*[@id="main"]/div[2]/div/div/section[2]/div[1]/div[1]/h1').text
    time.sleep(2)
    try:
        driver.find_element_by_class_name('_1HtKl_').click()
        reviews = driver.find_elements_by_class_name('_1BIjNY')
        time.sleep(2)
        for review in reviews:
            text_review = driver.find_element_by_xpath(f'//*[@id="modal-panel-property-reviews-0"]/section/div/div[3]/ul/li[{j}]/p[1]').text
            mark = driver.find_element_by_xpath(f'//*[@id="modal-panel-property-reviews-0"]/section/div/div[3]/ul/li[1]/div/span[1]').text
            print(f'{bcolors.BLUE}{i}.HOTEL NAME:{bcolors.ENDC} {hotel_name}')
            print(text_review + ' ' + mark)
            item = {
                'Hotel_name': hotel_name,
                'Review': text_review,
                'mark': float(mark.replace('\n.', ''))
            }
            data.append(item)
            j += 1
    except:
        pass

df = pd.DataFrame(data)
df.to_csv('../csvs/scrapped_reviews_hotelscom.csv', sep=',', encoding='utf-8', index=False)
import time
from selenium import webdriver
import pandas as pd

class bcolors:
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    RED = '\033[91m'
    ENDC = '\033[0m'

# Getting the booking Amsterdam hotels url
url = 'https://www.booking.com/searchresults.html?aid=376371&label=es-JCB2UqznXtCO_RDP_nj5CAS410545262609%3Apl%3Ata%3Ap1%3Ap22.563.000%3Aac%3Aap%3Aneg%3Afi%3Atikwd-65526620%3Alp9065109%3Ali%3Adec%3Adm%3Appccp%3DUmFuZG9tSVYkc2RlIyh9Ye8F2ouj63ytkBtrYs5TAfs&sid=393393781953526acfba298d71f6a0a0&tmpl=searchresults&ac_click_type=b&ac_position=0&class_interval=1&dest_id=-2140479&dest_type=city&dtdisc=0&from_sf=1&group_adults=2&group_children=0&iata=AMS&inac=0&index_postcard=0&label_click=undef&lang=en-us&no_rooms=1&offset=0&postcard=0&raw_dest_type=city&room1=A%2CA&sb_price_type=total&search_selected=1&shw_aparth=1&slp_r_match=0&soz=1&src=index&src_elem=sb&srpvid=07667067fffa00be&ss=%C3%81msterdam%2C%20Holanda%20Septentrional%2C%20Pa%C3%ADses%20Bajos&ss_all=0&ss_raw=A&ssb=empty&sshis=0&top_ufis=1&lang_click=other;cdl=es;lang_changed=1'

# Deleting errors in the chrome connection
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome('../drivers/chromedriver.exe', options=options)

# Opening the browser
driver.get(url)

print('STARTING THE SCRAPE...')

# Accept the cookies
time.sleep(5)
driver.find_element_by_css_selector('#onetrust-accept-btn-handler').click()

# Get a list of all the hotels in main page
hotels = driver.find_elements_by_class_name('fb01724e5b')

urls = []
for hotel in hotels:
    urls.append(hotel.get_attribute('href'))

data = []
i = 0
j = 1
for hotel in hotels:
    j = 1
    hotel_url = urls[i]
    i += 1
    driver.get(hotel_url)
    time.sleep(5)
    hotel_name = driver.find_element_by_xpath('//*[@id="hp_hotel_name"]').text
    driver.find_element_by_css_selector('#guest-featured_reviews__horizontal-block > div > div.hp-featured_reviews-bottom > button > span').click()
    time.sleep(3)
    reviews = driver.find_elements_by_class_name('c-review-block')
    for review in reviews:
        try:
            review_text_good = driver.find_element_by_xpath(f'.//*[@id="review_list_page_container"]/ul/li[{j}]/div/div[2]/div[2]/div[2]/div/div[1]/p/span[3]').text
        except:
            review_text_good = ''
        try:
            review_text_bad = driver.find_element_by_xpath(f'.//*[@id="review_list_page_container"]/ul/li[{j}]/div/div[2]/div[2]/div[2]/div/div[2]/p/span[3]').text
        except:
            review_text_bad = ''
        print(f'{bcolors.BLUE}{i}.HOTEL NAME:{bcolors.ENDC} {hotel_name}')
        print(f'{bcolors.GREEN}GOOD REVIEW {j}:{bcolors.ENDC} {review_text_good}')
        print(f'{bcolors.RED}BAD REVIEW {j}:{bcolors.ENDC} {review_text_bad}')
        j += 1

        item = {
            'Hotel_Name': hotel_name,
            'Negative_Review': review_text_bad,
            'Positive_Review': review_text_good
        }
        data.append(item)

df = pd.DataFrame(data)
df.to_csv('../csvs/scrapped_reviews_booking2.csv', sep=',', encoding='utf-8', index=False)
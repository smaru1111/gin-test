# from selenium import webdriver
# import time

# options = webdriver.ChromeOptions()
# driver = webdriver.Remote(
#              command_executor = 'http://selenium:4444/wd/hub',
#              options = options
#              )

# driver.implicitly_wait(10)

# url = 'https://datascience-beginer.com/' # テストでアクセスするURLを指定
# driver.get(url)

# time.sleep(3)
# driver.save_screenshot('test.png') # アクセスした先でスクリーンショットを取得
# driver.quit()


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as soup
from time import sleep
from selenium.common.exceptions import NoSuchElementException
import pandas as pd

movie_names = []
movie_descriptions = []
movie_ratings = []

def open_site():
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-notifiactions")
    # driver = webdriver.Chrome(executable_path='PATH/TO/YOUR/CHROME/DRIVER',options=options)
    driver = webdriver.Remote(
             command_executor = 'http://selenium:4444/wd/hub',
             options = options
             )
    # driver.get(r'https://www.amazon.co.jp/ap/signin?accountStatusPolicy=P1&clientContext=261-1149697-3210253&language=en_US&openid.assoc_handle=amzn_prime_video_desktop_us&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.mode=checkid_setup&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&openid.ns.pape=http%3A%2F%2Fspecs.openid.net%2Fextensions%2Fpape%2F1.0&openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.primevideo.com%2Fauth%2Freturn%2Fref%3Dav_auth_ap%3F_encoding%3DUTF8%26location%3D%252Fref%253Ddv_auth_ret')
    driver.get(r'https://www.amazon.co.jp/gp/video/detail/B0CNS3VD1J/ref=atv_me_inc_c_rILTFZ_HSb8e228_1_1?jic=16|CgNhbGwSBHN2b2Q=&language=ja_JP&currency=JPY')
    sleep(5)
    search(driver)

def search(driver):
    driver.find_element_by_id('pv-search-nav').send_keys('Comedy Movies',Keys.ENTER)

    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("scrollTo(0, document.body.scrollHeight);")
        sleep(5)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    html = driver.page_source
    Soup = soup(html,'lxml')
    tiles = Soup.find_all('div',attrs={"class" : "av-hover-wrapper"})
    
    for tile in tiles:
        movie_name = tile.find('h1',attrs={"class" : "_1l3nhs tst-hover-title"})
        movie_description = tile.find('p',attrs={"class" : "_36qUej _1TesgD tst-hover-synopsis"})
        movie_rating = tile.find('span',attrs={"class" : "dv-grid-beard-info"})
        rating = (movie_rating.span.text)
        try:
            if float(rating[-3:]) > 8.0 and float(rating[-3:]) < 10.0:
                movie_descriptions.append(movie_description.text)
                movie_ratings.append(movie_rating.span.text)
                movie_names.append(movie_name.text)
                print(movie_name.text, rating)
        except ValueError:
            pass
    dataFrame()


def dataFrame():
    details = {
        'Movie Name' : movie_names,
        'Description' : movie_descriptions,
        'Rating' : movie_ratings
    }
    data = pd.DataFrame.from_dict(details,orient='index')
    data = data.transpose()
    data.to_csv('Comedy.csv')

open_site()
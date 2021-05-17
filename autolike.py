from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium import webdriver

# user & password for login, can give an empty string if do not want to login for scraping
# scraping with login will get more images for each user
IG_USERNAME = ''
IG_PASSWORD = ''

# account to like all the photos
# use account username not name
IG_ACCOUNT = ''

IG_URL = 'https://www.instagram.com'


def wait_for_searchbar(wd):
    WebDriverWait(wd, 10).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, '[placeholder="Search"]')
        )
    )


def login(wd):
    wd.get(IG_URL)
    username = WebDriverWait(wd, 10).until(
        EC.presence_of_element_located((By.NAME, 'username'))
    )
    username.send_keys(IG_USERNAME)
    password = WebDriverWait(wd, 10).until(
        EC.presence_of_element_located((By.NAME, 'password'))
    )
    password.send_keys(IG_PASSWORD)
    loginbtn = WebDriverWait(wd, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '[type="submit"]'))
    )
    loginbtn.click()
    
    wait_for_searchbar(wd)


def goto_account(wd):
    wd.get('{}/{}'.format(IG_URL, IG_ACCOUNT))


def get_posts(wd):
    info = WebDriverWait(wd, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '.k9GMp'))
    )

    return info.text.split()[0]


def wait_for_images(wd):
    return WebDriverWait(wd, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '.v1Nh3.kIKUG._bz0w'))
    )


def next_img(wd):
    wd.find_element_by_css_selector('._65Bje.coreSpriteRightPaginationArrow').click()


def logout(wd):
    wd.find_element_by_css_selector('[aria-label="Close"]').click()
    wd.find_element_by_css_selector('._2dbep.qNELH').click()
    wd.find_element_by_css_selector('._7UhW9.xLCgt.MMzan.KV-D4.fDxYl').click()


def wait_for_img(wd):
    WebDriverWait(wd, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '.ltpMr.Slqrh'))
    )


def element_exists(wd, css):
    try:
        wd.find_element_by_css_selector(css)
    except NoSuchElementException:
        return False
    return True


if __name__ == '__main__':
    print('starting ...')

    wd = webdriver.Firefox()
    
    login(wd)
    goto_account(wd)
    
    posts = get_posts(wd)
    
    images = wait_for_images(wd)
    images.click()

    print('liking ...')

    for i in range(int(posts)-1):
        wait_for_img(wd)

        if element_exists(wd, '[aria-label="Like"]'):
            wd.find_element_by_css_selector('[aria-label="Like"]').click()

        next_img(wd)

    logout(wd)

    print('ending ...')

    wait_for_searchbar(wd)

    wd.close()
    wd.quit()
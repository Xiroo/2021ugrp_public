"""Simple Unsplash Images Crawler

Installation
Please install google chrome, download chrome driver at
'https://chromedriver.chromium.org/downloads' then put it here.

Usage:

python main.py -k "animal" --max-scroll 10 --max-image 100
"""
import os
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from sys import argv
import argparse
from urllib.parse import urlparse, urlencode, urlunparse, parse_qs


num_imgs = 0
path = ""
max_images = 100
BASE_URL = 'https://unsplash.com/s/photos/'
PHOTO_URL = 'https://images.unsplash.com/photo'
DRIVER_PATH = './chromedriver'


def download_image(url, filename):
    """Download single image from given url"""
    global num_imgs
    download_dir = path
    try:
        img_path = os.path.join(download_dir, filename)
        if not os.path.isfile(img_path):
            with requests.get(url) as response, open(img_path, 'wb') as f:
                f.write(response.content)
            num_imgs += 1
        print(f'Downloaded {img_path} Total: {num_imgs}')
        if num_imgs >= max_images:
            exit()
    except Exception as e:
        import traceback
        traceback.print_exc()


def download_images_on_one_screen(driver):
    """Download all images on one screen"""
    imgs = driver.find_elements_by_tag_name('img')
    for img in imgs:
        srcset = img.get_attribute('srcset')
        if srcset is not None:
            img_url = srcset.split(',')[0]
            if img_url.startswith(PHOTO_URL):
                uu = list(urlparse(img_url))
                qs = parse_qs(uu[4], keep_blank_values=True)
                if 'ixid' in qs:
                    new_qs = {'ixid': qs['ixid']}
                    uu[4] = urlencode(new_qs, doseq=True)
                    new_url = urlunparse(uu)
                    filename = '%s.png' % qs['ixid'][0]
                    download_image(new_url, filename)


def main():
    parser = argparse.ArgumentParser(description='Simple Unsplash Images Crawler')
    parser.add_argument('-k', '--keyword', type=str,
                        help='Search keyword')
    parser.add_argument('--max-scroll', type=int, default=None,
                        help='Maximum number of scrolling')
    parser.add_argument('--max-images', type=int, default=100,
                        help='Maxium number of images would be downloaded')
    parser.add_argument('--download-dir', type=str, default='downloads',
                        help='Download directory')
    parser.add_argument('--scroll-step', type=int, default=500,
                        help='Scrolling step')
    parser.add_argument('--headless', action='store_true', default=False,
                        help='Not show window')
    args = parser.parse_args()
    print(args)

    keyword = args.keyword
    max_scroll = args.max_scroll
    scroll_step = args.scroll_step
    global max_images
    max_images = args.max_images
    download_dir = "images/"+keyword
    global path
    path = download_dir
    if not os.path.isdir(download_dir):
        os.makedirs(download_dir)
    
    if args.headless:
        options = Options()
        options.headless = True
        driver = webdriver.Chrome(executable_path=DRIVER_PATH, chrome_options=options)
    else:
        driver = webdriver.Chrome(executable_path=DRIVER_PATH)
    driver.get(BASE_URL + keyword)  # first request

    scroll_height = 500
    try:
        driver.find_element_by_xpath('/html/body/div/div/div[2]/div[3]/div[6]/div[1]/button').click()
    except:
        pass
    
    for i in range(max_scroll):
        download_images_on_one_screen(driver)
        print(f'Scrolling #{i}')

        # Scroll down
        driver.execute_script("window.scrollTo(0, {});".format(scroll_height))
        scroll_height += scroll_step
        time.sleep(3)


if __name__ == '__main__':
    main()

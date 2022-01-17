
# Unsplash Images Crawler
A tool helps to crawl enumerous number of images from [Unsplash](https://unsplash.com/).
## Installation
The tool requires Selenium so you must download [chrome driver](https://chromedriver.chromium.org/downloads) and put it in project directory (make sure the driver version is compatible with your current Chrome app). After that, just install all dependencies in `requirements.txt` .
```
pip install -r requirements.txt
```
Done!
## Usage
It's very easy to use. You just need to run the following command.
```
python crawler.py -k "animal" --max-images 200 --download-dir images/
```
Use `python crawler.py` for more details.
```
python crawler.py -h
usage: crawler.py [-h] [-k KEYWORD] [--max-scroll MAX_SCROLL] [--max-images MAX_IMAGES] [--download-dir DOWNLOAD_DIR] [--scroll-step SCROLL_STEP]

Simple Unsplash Images Crawler

optional arguments:
  -h, --help            show this help message and exit
  -k KEYWORD, --keyword KEYWORD
                        Search keyword
  --max-scroll MAX_SCROLL
                        Maximum number of scrolling
  --max-images MAX_IMAGES
                        Maxium number of images would be downloaded
  --download-dir DOWNLOAD_DIR
                        Download directory
  --scroll-step SCROLL_STEP
                        Scrolling step
```
## Contribution
Feel free to leave any issues or pull requests. Every contribution is welcome.

source: https://github.com/tamnguyenvan/unsplash-images-crawler

command: python crawler.py --max-scroll 1000 --max-images 100 --scroll-step 3000 -k ""
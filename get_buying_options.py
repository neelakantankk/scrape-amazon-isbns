import requests
from requests.exceptions import ChunkedEncodingError, Timeout as TimeOutError
import pathlib
import logging
import lxml.html as lhtml
import time
from exceptions import PageNotRetrievedError
from extract_from_amazon_page import extract_from_amazon_page, contains_class
from urllib.parse import urljoin
from parse_amazon_url import parse_amazon_url

def get_buying_options(url_to_page):
   
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    
    file_dump_folder = pathlib.Path.cwd().joinpath('file-dump')

    session = requests.Session()

    session.headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0'
            }

    logger.debug(f"Fetching page {url_to_page}")

    try:
        amazon_page = session.get(url_to_page, timeout=30)
    except ChunkedEncodingError as e:
        logger.error(f"Could not call {url_to_page}. Got {e}")
        logger.info(f"Trying to call {url_to_page} again")
        amazon_page = session.get(url_to_page,timeout=60)
    except TimeOutError:
        logger.error(f"Call to {url_to_page} timed out")
        raise TimeOutError("Call to {url_to_page} timed out")

    DELAY = 15
    if amazon_page.status_code == 503: 
            logger.debug(f"{url_to_page} returned {amazon_page.status_code}")
            logger.debug(f"Pausing operations for {DELAY} seconds...")
            time.sleep(DELAY)
            logger.debug(f"Resuming operations")
            amazon_page = session.get(url_to_page, timeout = 60)
            if amazon_page.status_code != 200:
                raise PageNotRetrievedError(f"Could not call {url_to_page}. Status code: {amazon_page.status_code}")
    elif amazon_page.status_code != 200:
        logger.error(f"Fetching {url_to_page} did not work")
        raise PageNotRetrievedError(f"Could not call {url_to_page}. Status code: {amazon_page.status_code}") 
    else:
        logger.info(f"Fetched page {url_to_page}")

    try:
        isbn, page_number = parse_amazon_url(url_to_page)
    except AssertionError:
        logger.error("Could not get valid ISBN")
        logger.debug("Setting data to date and time")
        isbn = time.strftime("%Y%m%d")
        page_number = time.strftime("%H%M%S")


    amazon_html = lhtml.fromstring(amazon_page.content)

    next_button = amazon_html.xpath(
            f".//ul[@class='a-pagination']/li[{contains_class('a-last')}]")
    options = extract_from_amazon_page(amazon_html)

    if next_button and "a-disabled" not in next_button[0].get("class"):
        logger.debug(f"{amazon_page.url} has more search results")
        next_page_url = urljoin("https://amazon.com",
                next_button[0].find("./a").get("href"))
        logger.debug(f"Next Page URL is: {next_page_url}")
        logger.debug(f"Getting next page of results")
        options.extend(
                get_buying_options(
                    next_page_url)
                )
        return options
    elif next_button and "a-disabled" in next_button[0].get("class"):
        logger.debug("No more pages to get")
        return options 
    else:
        logger.debug(f"{amazon_page.url} has only one page of results")
        return options

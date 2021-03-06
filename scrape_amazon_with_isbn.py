# -*- coding: utf-8 -*-
"""
Created on Thu Aug 22 12:07:59 2019

@author: k999neel
"""

import requests
import lxml.html as lhtml
import pathlib
import logging
import logging.config
import json
from random import choice
from sys import exit as sysExit
from amazon_item import Amazon_item

#---------------------Required Amazon URLs-----------------------------------#
amazon_urls = {
        'search':r'https://amazon.com/s',
        'buying_options':r'https://amazon.com/gp/offer-listing/',
        }

# When looking at product details, always use keyword ref=mt_paperback
# Search for id productDetailsTable

trial_list_of_ISBNs = [
        '9781292040622',
        '9781292039817',
        '9781292058825',
        '9781292024967',
        '9781292153261',
        '9781292024042',
        '9781292041872',
        '9781292026763',
        '9781292255460',
        '9781292274522',
        '9781292265193',
        '9781292058825',
        '9781292020587',
        '9781292214146',
        '9781292247137']


#-------------------------------__main__-------------------------------------#
def main():

    #-----------------------------Set up logging-------------------------#
    if not pathlib.Path.cwd().joinpath('logs').exists():
        pathlib.Path.cwd().joinpath('logs').mkdir()
    if not pathlib.Path.cwd().joinpath('file-dump').exists():
        pathlib.Path.cwd().joinpath('file-dump').mkdir()

    with open('logging_config.json','r',encoding='utf-8') as fObject:
        log_config = json.load(fObject)
    logging.config.dictConfig(log_config)

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

#    -----------------------------Set up session--------------------------#
    session = requests.Session()
    session.headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0'
            }

    search_params = {'k':f'{choice(trial_list_of_ISBNs)}'}

    logger.debug(f'Calling {amazon_urls["search"]} with params {search_params}')

    search_results = session.get(amazon_urls['search'],
                                 params=search_params)

    if search_results.status_code != 200:
        logger.error(f'Search returned search_results.status_code')
        sysExit(1)
    else:
        logger.debug('Amazon returned page')
        with pathlib.Path.cwd().joinpath('file-dump/search_page.html').open('wb') as fObject:
            fObject.write(search_results.content)

    amazon_page = lhtml.fromstring(search_results.content)

    if not amazon_page.findall('.//div[@data-asin]'):
        logger.debug("No search results")

    amazon_items = []
    for div in amazon_page.findall('.//div[@data-asin]'):
        logger.debug(f'ASIN = {div.get("data-asin")}')
        logger.debug(f'Product name : {"".join(div.xpath(".//h2/a//text()")).strip()}')
        logger.debug(f'Link to product page: {div.find(".//h2/a").get("href")}')
        amazon_items.append(Amazon_item(div.get("data-asin"),
            div.find(".//h2/a").get("href")))

    for item in amazon_items:
        logger.debug(f"Product page for ASIN {item.asin} is {item.product_page}")
        loger.debug(f"Calling Product Page")

        product_page = item.get_page()






if __name__ == '__main__':
    main()

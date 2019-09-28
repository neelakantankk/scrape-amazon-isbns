# -*- coding: utf-8 -*-
"""
Created on Thu Aug 22 12:07:59 2019

@author: Neelakantan 
"""

import pathlib
import logging
import logging.config
import json
from get_buying_options import get_buying_options
from exceptions import PageNotRetrievedError
from isbn_converter import isbn_converter
from requests.exceptions import Timeout as TimeOutError

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
def scrape_amazon_for_isbn_options(list_of_ISBNs):

    #---------------------Required Amazon URLs-----------------------#
    amazon_urls = {
            'search':r'https://amazon.com/s',
            'buying_options':r'https://amazon.com/gp/offer-listing/',
            }
   
    file_dump_folder = pathlib.Path.cwd().joinpath('file-dump')

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    #-------------------------------------Calling ISBNs------------#
    item_results = dict()
    isbns_to_process = len(list_of_ISBNs) 
    for count, isbn in enumerate(list_of_ISBNs,start=1):

        logger.debug(f"Processing {count} of {isbns_to_process}")

        logger.debug(f"ISBN to fetch: {isbn}")
        url_to_page = f'{amazon_urls["buying_options"]}{isbn_converter(isbn)}'

        try:
            logger.debug(f"Getting buying options for {isbn}")
            item_results[isbn] = get_buying_options(url_to_page)
            logger.debug(f"Buying options retrieved")
        except PageNotRetrievedError as e:
            logger.error(f"{e}")
        except TimeOutError as e:
            logger.error(f"{e}")


    return item_results

if __name__ == '__main__':
    scrape_amazon_for_isbn_options(trial_list_of_ISBNs)

    

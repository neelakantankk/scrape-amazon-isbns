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
def scrape_amazon_for_isbn_options(list_of_isbns):

    #---------------------Required Amazon URLs-----------------------#
    amazon_urls = {
            'search':r'https://amazon.com/s',
            'buying_options':r'https://amazon.com/gp/offer-listing/',
            }


    #-----------------------------Set up logging-------------------------#
    if not pathlib.Path.cwd().joinpath('logs').exists():
        pathlib.Path.cwd().joinpath('logs').mkdir()
    if not pathlib.Path.cwd().joinpath('file-dump').exists():
        pathlib.Path.cwd().joinpath('file-dump').mkdir()
    
    file_dump_folder = pathlib.Path.cwd().joinpath('file-dump')

    with open('logging_config.json','r',encoding='utf-8') as fObject:
        log_config = json.load(fObject)
    logging.config.dictConfig(log_config)

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    #-------------------------------------Calling ISBNs------------#
    item_results = dict()
    
    for isbn in list_of_ISBNs:

        logger.debug(f"ISBN to fetch: {isbn}")
        url_to_page = f'{amazon_urls["buying_options"]}{isbn_converter(isbn)}'

        try:
            logger.debug(f"Getting buying options for {isbn}")
            item_results[isbn] = get_buying_options(url_to_page)
            logger.debug(f"Buying options retrieved")
        except PageNotRetrievedError as e:
            logger.error(f"{e}")


    with file_dump_folder.joinpath(
            "ISBN_and_Buying_Options.txt").open(
                    "w",encoding='utf-8') as fObject:
        for isbn in item_results.keys():
            fObject.write("{:#^80}\n".format(' '))
            fObject.write(f"ISBN: {isbn}")
            fObject.write(f" \u2013 Number of sellers found: {len(item_results[isbn])}\n")
            for olpOffer in item_results[isbn]:
                fObject.write("{:-^80}\n".format(''))
                fObject.write(f"\tSeller: {olpOffer.olpSeller}\n")
                fObject.write(f"\tLink to Seller: {olpOffer.olpSellerLink}\n")
                fObject.write(f"\tCondition: {olpOffer.olpCondition}\n")
                fObject.write(f"\tShips from: {olpOffer.olpDelivery}\n")
                fObject.write(f"\tPrice (including shipping): {olpOffer.olpPrice}\n")
            fObject.write("{:#^80}\n".format(' '))

if __name__ == '__main__':
    scrape_amazon_for_isbn_options(trial_list_of_ISBNs)

    

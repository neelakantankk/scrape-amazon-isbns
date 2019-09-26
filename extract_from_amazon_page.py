# -*- coding: utf-8 -*-
"""
Created on Mon Sep 23 19:09:12 2019

@author: Neelakantan
"""

import lxml.html as lhtml
import logging
from collections import namedtuple
import re
from urllib.parse import urljoin


def contains_class(class_name):
    return f"contains(concat(' ',normalize-space(@class),' '),' {class_name} ')"


def extract_from_amazon_page(amazon_html):
    
    OlpListing = namedtuple(
            "OlpListing",
            ["olpPrice","olpCondition","olpDelivery","olpSeller","olpSellerLink"])

    logger = logging.getLogger(__name__) 
    logger.setLevel(logging.INFO)

    olpOffers = list()

    for node in amazon_html.xpath(
            f".//div[@id='olpOfferList']//div[{contains_class('olpOffer')}]"):
       
        seller = re.sub(r"\s{2,}",
                 ' ',
                 ''.join(
                    node.xpath(
                   f".//div[{contains_class('olpSellerColumn')}]/h3//text()"))
               )

        logger.debug(f"Seller is {seller}")

        seller_link = node.xpath(
                f".//div[{contains_class('olpSellerColumn')}]/h3//a")[0].get("href")
        seller_link = urljoin(r"https://amazon.com",seller_link)

        logger.debug(f"Link to seller is {seller_link}")
        
        price = re.sub(r"\s{2,}",
                ' ',
                ''.join(
                    node.xpath(f".//div[{contains_class('olpPriceColumn')}]//text()"))
                ).replace("\nDetails",'')
        logger.debug(f"Price is {price}")

        condition = re.sub(r"\s{2,}",
                    ' ',
                    ''.join(
                        node.xpath(
                        f".//div[{contains_class('olpConditionColumn')}]//span[{contains_class('olpCondition')}]/text()"))
                    )

        logger.debug(f"Condition is {condition}") 

        try:
            delivery = re.search(r"(Ships from .*?\.)",
                     ''.join(
                     node.xpath(
                         f".//div[{contains_class('olpDeliveryColumn')}]//span[@class='a-list-item']//text()"))).group(1)
        except AttributeError:
            logger.error(f'Could not find delivery in "' + re.sub(r"\s{2,}",
                ' ',
                ''.join(
                node.xpath(
                    f".//div[{contains_class('olpDeliveryColumn')}]//span[@class='a-list-item']//text()")).replace("\t",'')) + '"')
            delivery = "Information not given"

        logger.debug(f"Delivery is {delivery}")
        olpOffers.append(
                OlpListing(price,condition,delivery,seller,seller_link)
                )
    
    return olpOffers



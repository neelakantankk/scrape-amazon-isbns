import lxml.html as lhtml
import logging
from collections import namedtuple
import re

def extract_from_amazon_page(amazon_page):
    
    def contains_class(class_name):
        return f"contains(concat(' ',normalize-space(@class),' '),' {class_name} ')"

    OlpListing = namedtuple(
            "OlpListing",
            ["olpPrice","olpCondition","olpDelivery","olpSeller"])

    logger = logging.getLogger(__name__) 
    logger.setLevel(logging.DEBUG)

    amazon_html = lhtml.fromstring(amazon_page.content)

    olpOffers = []

    for node in amazon_html.xpath(
            f".//div[@id='olpOfferList']//div[{contains_class('olpOffer')}]"):
       
        seller = re.sub(r"\s{2,}",
                 ' ',
                 ''.join(
                    node.xpath(
                   f".//div[{contains_class('olpSellerColumn')}]/h3//text()"))
               )

        logger.debug(f"Seller is {seller}")
        
        price = re.sub(r"\s{2,}",
                ' ',
                ''.join(
                    node.xpath(f".//div[{contains_class('olpPriceColumn')}]//text()"))
                )
        logger.debug(f"Price is {price}")

        condition = re.sub(r"\s{2,}",
                    ' ',
                    ''.join(
                        node.xpath(
                        f".//div[{contains_class('olpConditionColumn')}]//span[{contains_class('olpCondition')}]/text()"))
                    )

        logger.debug(f"Condition is {condition}")

                            

        




import pathlib
import openpyxl
import logging
import json
import logging.config
from scrape_amazon_for_isbn_options import scrape_amazon_for_isbn_options

def main():
    #-----------------------------Set up logging-------------------------#
    if not pathlib.Path.cwd().joinpath('logs').exists():
        pathlib.Path.cwd().joinpath('logs').mkdir()
    if not pathlib.Path.cwd().joinpath('file-dump').exists():
        pathlib.Path.cwd().joinpath('file-dump').mkdir()
 
    with open('logging_config.json','r',encoding='utf-8') as fObject:
        log_config = json.load(fObject)
    logging.config.dictConfig(log_config)

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    isbn_book = openpyxl.load_workbook("Live_ISBNs_201908.xlsx",read_only=True,data_only=True)
    isbn_sheet = isbn_book.active

    isbns = [row[1].value for row in isbn_sheet.iter_rows(min_row=2)]

    logger.debug(f"Number of isbns: {len(isbns)}")
    
    item_results = scrape_amazon_for_isbn_options(isbns)

    output_book = openpyxl.Workbook()
    output_sheet = output_book.active
    output_sheet.title = "ISBNs_and_Seller_Data"

    output_sheet.append(["ISBN13",
                         "Seller Name", 
                         "Link to seller's amazon page",
                         "Condition of product (New/Used)",
                         "Shipped from",
                         "Price"])

    logger.debug("Writing to Book ISBNs_and_Seller_Data.xlsx")
    for isbn,results in item_results.items():
        for olpOffer in results:
            output_sheet.append([isbn,
                                 olpOffer.olpSeller,
                                 olpOffer.olpSellerLink,
                                 olpOffer.olpCondition,
                                 olpOffer.olpDelivery,
                                 olpOffer.olpPrice])

    try:
        output_book.save("file-dump/ISBNs_and_Seller_Data.xlsx")
        logger.debug("File ISBNS_and_Seller_Data.xlsx written successfully")
    except Exception as e:
        logger.error("Could not save file ISBNS_and_Seller_Data.xlsx")


if __name__ == '__main__':
    main()







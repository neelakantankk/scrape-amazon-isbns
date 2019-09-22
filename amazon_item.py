import urllib.parse as urlparse
import requests

class Amazon_item:
    def __init__(self, asin, product_page):
        self.asin = asin
        self.product_page = urlparse.urljoin("https://amazon.com",product_page)

    def get_page(self):
        return requests.get(self.product_page)
    

        

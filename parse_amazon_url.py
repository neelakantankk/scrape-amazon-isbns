import urllib.parse
import re

def parse_amazon_url(url):
    parsed_url = urllib.parse.urlparse(url)
    
    isbn = parsed_url.path.split("/")[3]
    assert re.match(r"^\d{9}[0-9X]{1}$",isbn) is not None
    if parsed_url.query:
        startIndex = urllib.parse.parse_qs(parsed_url.query)["startIndex"][0]
        page_number = int(startIndex)//10 + 1
    else:
        page_number = 1

    return (isbn,page_number)

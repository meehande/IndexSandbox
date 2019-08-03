import requests
import os
from bs4 import BeautifulSoup
from src.utils.file_handling import write_file
from src.utils.url_handling import join_url_paths, get_parent_url

start_date = '2010-01-01'
end_date = '2016-12-31'

# User pandas_reader.data.DataReader to load the desired data. As simple as that.


def fetch_index_underlying_data(index_url, output_path):
    page = requests.get(index_url)
    soup = BeautifulSoup(page.text, 'html.parser')
    all_links = soup.find_all('a')
    link_text = 'Download Data into CSV'
    download_links = [l for l in all_links if l.text==link_text]
    if len(download_links) != 1:
        raise AssertionError("Expected exactly one download to be available! Actual number of downloads: {}".format(len(download_links)))
    link_to_download = download_links[0].attrs['href']
    #data = requests.get(base_url + link_to_download)
    data = requests.get(join_url_paths(get_parent_url(index_url), link_to_download))

    write_file(data.content, output_path)

sample_bloomberg_url = 'https://www.bloomberg.com/quote/ATA:CN'

bloomberg_quote_base_url = 'https://www.bloomberg.com/quote/'


def try_get_stock_price(search_url, bloomberg_code, listing_code):
    formatted_bloomberg_with_listing = ':'.join([bloomberg_code.replace('.', '/'), listing_code])
    url = join_url_paths(search_url, formatted_bloomberg_with_listing)
    stock_page = requests.get(url)
    soup = BeautifulSoup(stock_page.text, 'html.parser')


"""
<section class="dataBox previousclosingpriceonetradingdayago numeric"><header class="title__49417cb9"><span>Prev Close</span></header><div class="value__b93f12ea">44.57</div></section>

"""

if __name__ == '__main__':
    base_url = r'https://web.tmxmoney.com/'
    url = r'https://web.tmxmoney.com/indices.php?section=tsx&index=^TSX#indexInfo'
    output_file = os.path.join(os.getcwd(), 'data', 'index_constituents.csv')

    fetch_index_underlying_data(url, output_file)

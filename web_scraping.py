import requests
import os
from bs4 import BeautifulSoup
from yahoo_fin import stock_info as si
from pandas_datareader import data
import pandas as pd


start_date = '2010-01-01'
end_date = '2016-12-31'

# User pandas_reader.data.DataReader to load the desired data. As simple as that.
panel_data = data.DataReader('INPX', 'google', start_date, end_date)


base_url = r'https://web.tmxmoney.com/'
url = r'https://web.tmxmoney.com/indices.php?section=tsx&index=^TSX#indexInfo'
output_file = os.path.join(os.getcwd(), 'data', 'index_constituents.csv')


def safely_create_output_dir(output_path):
    output_dir = os.path.dirname(output_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)


def write_file(data, output_path):
    safely_create_output_dir(output_path)
    with open(output_path, 'w') as f:
        f.write(data)


def fetch_data():
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    all_links = soup.find_all('a')
    link_text = 'Download Data into CSV'
    download_links = [l for l in all_links if l.text==link_text]
    if len(download_links) != 1:
        raise AssertionError("Expected exactly one download to be available! Actual number of downloads: {}".format(len(download_links)))
    link_to_download = download_links[0].attrs.values()[0]
    data = requests.get(base_url + link_to_download)

    write_file(data.content, output_file)

sample_bloomberg_url = 'https://www.bloomberg.com/quote/ATA:CN'

bloomberg_quote_base_url = 'https://www.bloomberg.com/quote/'


def join_url_paths(base_path, *sub_paths):
    base_path = base_path.strip('/')
    sub_paths = [p.strip('/') for p in sub_paths]
    return '/'.join([base_path] + sub_paths)


def try_get_stock_price(search_url, bloomberg_code, listing_code):
    formatted_bloomberg_with_listing = ':'.join([bloomberg_code.replace('.', '/'), listing_code])
    url = join_url_paths(search_url, formatted_bloomberg_with_listing)
    stock_page = requests.get(url)
    soup = BeautifulSoup(stock_page.text, 'html.parser')


"""
<section class="dataBox previousclosingpriceonetradingdayago numeric"><header class="title__49417cb9"><span>Prev Close</span></header><div class="value__b93f12ea">44.57</div></section>

"""

if __name__ == '__main__':
    fetch_data()

"""This module contains functions that scrape product data from Amazon's product listing pages"""

import requests
from bs4 import BeautifulSoup
from utility_funcs import format_rating
import utility_funcs

HEADER_FOR_GET_REQUEST = (
    {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:107.0) Gecko/20100101 Firefox/107.0',
     'Accept-language': 'en-US, en;q=0.5'}
)

def get_target_url(page: int, keywords: str):
    """This function gets the number of pages from incoming """
    base_url = 'https://www.amazon.com/s?k='
    search_keywords_formatted = keywords.replace(' ', '+')
    # specify the results >> results in page1
    page_parameter = '&page='+ str(page)
    search_url = f'{base_url}{search_keywords_formatted}{page_parameter}'
    return search_url


def get_soup_format_obj(target_url):
    """This function returns searching results in a soup format objects from incoming url"""
    response_obj = requests.get(target_url, headers=HEADER_FOR_GET_REQUEST)
    soup_format = BeautifulSoup(response_obj.content, 'html.parser')
    return soup_format

def get_one_page(search_url):
    """This function returns gathers only the search results we are looking for: <div> tags, inside <div> tags look for 's-result-item', 's-search-result'"""
    soup_format = get_soup_format_obj(search_url)
    search_results = soup_format.find_all('div', {'class': 's-result-item', 'data-component-type': 's-search-result'})
    return search_results

def get_last_page(key_words):
    """This function returns the number of pages of results from incoming keyword."""
    target_url = get_target_url(1, key_words)
    soup_format = get_soup_format_obj(target_url)
    try:
        last_page = soup_format.find('span', attrs ={'class': 's-pagination-item s-pagination-disabled'}).text
    except AttributeError:
        print('fail finding last page')
    if(utility_funcs.string_is_integer(last_page)) is True:
        return int(last_page)
    #there are less than 4 results pages
    return 3

def get_product_title(item):
    """This functions returns product title of incoming item in a string type"""
    first_product_title = item.h2.text
    return first_product_title

def get_product_ratings(item):
    """This functions returns product rating of incoming item in a string type.
    returns None if the product has no ratings"""
    try:
        # get the rating of first product
        first_product_rating = item.find('i', {'class': 'a-icon'})
        first_product_rating = format_rating(first_product_rating.text)
        return first_product_rating
    except AttributeError:
        return None
    except IndexError:
        return None

def get_num_of_rating(item):
    """This functions returns the number of product rating of incoming item in a string type.
    returns None if the product has no ratings"""
    try:
        # if aria label has value
        rating_blocks = item.find_all('span', {'aria-label': True})
        # remove unnecessary characters(comma, round brackets)
        num_ratings = rating_blocks[1].text.replace(",","").replace("(", "").replace(")", "")
        return num_ratings
    except AttributeError:
        return None
    except IndexError:
        return None

def get_product_price(item):
    try:
        # extract price
        integer_price = item.find('span', {'class': 'a-price-whole'})
        decimal_price = item.find('span', {'class': 'a-price-fraction'})
        whole_price = integer_price.text + decimal_price.text
        whole_price = whole_price.replace(",","")
        return whole_price
    except AttributeError:
        return None

def get_url_string(item):
    try:
        # get the link of the product
        product_link = item.h2.a['href']
        return 'https://amazon.com' + product_link
    except AttributeError:
        return None

def get_data_from_results(search_results):
    """This functions prints results of scrapping. (Just for testing) """
    for item in search_results:
        print(get_product_title(item))
        print(get_url_string(item))
        print(get_product_ratings(item))
        print(get_num_of_rating(item))
        print(get_product_price(item))

import requests
from bs4 import BeautifulSoup
from utility_funcs import format_rating
import utility_funcs

HEADER_FOR_GET_REAUEST = (
    {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:107.0) Gecko/20100101 Firefox/107.0',
     'Accept-language': 'en-US, en;q=0.5'}
)


def get_target_url(page: int, keywords: str):
    base_url = 'https://www.amazon.com/s?k='
    search_keywords_formatted = keywords.replace(' ', '+')
    # specify the results >> results in page1
    page_parameter = '&page='+ str(page)
    search_url = f'{base_url}{search_keywords_formatted}{page_parameter}'
    return search_url


def get_soup_format_obj(target_url):
    response_obj = requests.get(target_url, headers=HEADER_FOR_GET_REAUEST)
    soup_format = BeautifulSoup(response_obj.content, 'html.parser')
    return soup_format


def get_one_page(search_url):
    soup_format = get_soup_format_obj(search_url)
    search_results = soup_format.find_all('div', {'class': 's-result-item', 'data-component-type' : 's-search-result'})
    return search_results


def get_last_page(key_words):
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
    first_product_title = item.h2.text
    print(first_product_title)


def get_product_ratings(item):
    try:
        # get the rating of first product
        first_product_rating = item.find('i', {'class': 'a-icon'})
        first_product_rating = format_rating(first_product_rating.text)
        print(first_product_rating)
    except AttributeError:
        print('No ratings')
    except IndexError:
        print('No ratings')


def get_num_of_rating(item):
    try:
        # aria label has value
        rating_blocks = item.find_all('span', {'aria-label': True})
        # rating_blocks[1] returns delivery date sometimes >> check if its returning None or not int/double value
        num_ratings = rating_blocks[1].text.replace(",","").replace("(", "").replace(")", "")
        print(num_ratings)
    except AttributeError:
        print('No ratings')
    except IndexError:
        print('No ratings')


def get_product_price(item):
    try:
        # extract price
        integer_price = item.find('span', {'class': 'a-price-whole'})
        decimal_price = item.find('span', {'class': 'a-price-fraction'})
        whole_price = integer_price.text + decimal_price.text
        whole_price = whole_price.replace(",","")
        print(whole_price)
    except AttributeError:
        print('product has no price listed')


def get_url_string(item):
    try:
        # get the link of the product
        product_link = item.h2.a['href']
        print('https://amazon.com' + product_link)
    except AttributeError:
        print('no link')


def get_data_from_results(search_results):
    for item in search_results:
        get_product_title(item)
        get_url_string(item)
        get_product_ratings(item)
        get_num_of_rating(item)
        get_product_price(item)

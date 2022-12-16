import requests
from bs4 import BeautifulSoup
from utility_funcs import format_rating

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


def get_one_page(search_url):
    response_obj = requests.get(search_url, headers=HEADER_FOR_GET_REAUEST)
    soup_format = BeautifulSoup(response_obj.content, 'html.parser')
    search_results = soup_format.find_all('div', {'class' : 's-result-item', 'data-component-type' : 's-search-result'})
    return search_results


def get_product_title(item):
    first_product_title = item.h2.text
    print(first_product_title)


def get_product_ratings(item):
    try:
        # get the rating of first product
        first_product_rating = item.find('i', {'class': 'a-icon'})
        first_product_rating = format_rating(first_product_rating.text)
        print(first_product_rating)
        #aria label has value
        rating_blocks = item.find_all('span', {'aria-label': True})
        num_ratings = rating_blocks[1].text.replace(",","").replace("(", "").replace(")", "")
        print(num_ratings)
    except AttributeError:
        print('No ratings')


def get_product_price(item):
    try:
        # extract price
        integer_price = item.find('span', {'class': 'a-price-whole'})
        decimal_price = item.find('span', {'class': 'a-price-fraction'})
        print(integer_price.text + decimal_price.text)
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
        get_product_ratings(item)
        get_product_price(item)
        get_url_string(item)
        next_line='\n'
        print(next_line)




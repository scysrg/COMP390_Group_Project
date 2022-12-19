"""
ui_funcs handles terminal printing, user input, and all things interface.
"""
import utility_funcs as util

keyword_prompt = "Choose an electronic you wish to search for\n" \
                 "\t1. Over Ear Headphones\n" \
                 "\t2. USB Microphones\n" \
                 "\t3. 1080p Webcams\n" \
                 "\t4. Capture Cards\n" \
                 "\t5. 8-channel Audio Mixers\n" \
                 "\t6. Gaming Laptops"

keyword_dict = {'1': 'over_ear_headphones',
                '2': 'usb_microphones',
                '3': 'webcams_1080p',
                '4': 'capture_cards',
                '5': 'audio_mixers_8channel',
                '6': 'gaming_laptops'}

relations_list = ['<', '>', '<=', '>=', '==']


def print_query_results(data: list, **query):
    """
    Takes the search results and prints them to terminal and writes it to a new file
    :param data: list of data fetched from user query
    :param query: product, rating, num_ratings, and price: tuples gathered from user input
    """
    search_query_str = f"Found {len(data)} {query['product']} with rating {query['rating']}; " \
                       f"number of ratings {query['num_ratings']}; and price {query['price']}\n"
    search_query_str = util.clean(search_query_str)
    print(search_query_str)
    util.clear(query['product'])
    util.write(search_query_str, query['product'])
    for entry in data:
        entry = process_entry(entry)
        print(entry)
        util.write(entry, query['product'])


def get_user_query():
    """
    Handles prompting the user for the search query
    :return product_query, rating_query, num_ratings_query, price_query: returns all the user input asked
    """
    print(keyword_prompt)
    product_query = prompt_product()
    print(f'Searching for {product_query}...')
    rating_query = prompt_query('star rating', 0.0, 5.0)
    num_ratings_query = prompt_query('number of ratings', 0.0, 0xffffffff)
    price_query = prompt_query('price', 0.0, 0xffffffff)
    return product_query, rating_query, num_ratings_query, price_query


def prompt_query(prompt_type: str, min_range, max_range):
    """
    Prompts user for individual values, accepting only float inputs valid by ranges
    :param prompt_type: type of prompt to be asked
    :param min_range: minimum bound for input
    :param max_range: maximum bound for input
    :return target_prompt_relation, target_prompt_value: A tuple consisting of the inequality operator and value queried
    """
    print(f'Target {prompt_type}? Hit Enter/Return for all', end='')
    while 1:  # Prompts user for the target value
        target_prompt_value = input(': ')
        if target_prompt_value == '':  # Case: User wants all in prompt_type
            return '>=', 0.0
        if not check_input(target_prompt_value, min_range, max_range):
            print(f'Please enter a valid value between {min_range}, {max_range}', end=''); continue
        break
    print(f'Choose relation operator for target from {relations_list}', end='')
    while 1:  # Prompts user for the (in)equality statement
        target_prompt_relation = input(': ')
        if target_prompt_relation not in relations_list:
            print('Please enter a valid relation from the list', end=''); continue
        return target_prompt_relation, target_prompt_value


def prompt_product():
    """
    Prompts the user for the product to search for
    :return product_query: valid user input for searching
    """
    while 1:
        keyword_input = input('>>')
        try:  # Error Case: unacceptable input
            product_query = keyword_dict[keyword_input]
        except KeyError:
            print("Please enter a valid query as a number between 1 and 6", end='')
            continue  # Call prompt again
        return product_query


def process_entry(entry: list):
    """
    Converts a db entry into a readable string format
    :param entry: list in the form fetched from the database
    :return: a str easily readable by the user
    """
    return f'{entry[0]}\n' \
           f'Avg. Rating: {entry[1]}*, Num. Ratings: {entry[2]}. ' \
           f'${entry[3]}\n' \
           f'{entry[4]}\n'


def check_input(user_input, min_range, max_range):
    """
    Checks the validity of numerical user input against ranges
    :param user_input: numerical input from user
    :param min_range: minimum bound for user_input
    :param max_range: maximum bound for user_input
    :return bool: True if user_input is float and between range values, False otherwise
    """
    if util.string_is_float(user_input):
        user_input = float(user_input)
        return min_range <= user_input <= max_range
    return False


def cont():
    """
    cont, short for continue, asks the user if they would like to continue searching for products
    :return bool: True if they would like to continue, False otherwise
    """
    print('Would you like to search again? y/n', end='')
    while 1:
        cont_input = input(': ')
        if cont_input.startswith('y'):
            return True
        if cont_input.startswith('n'):
            return False
        print('y or n, please! y for yes, n for no', end='')


load_index = 0
load_arr = ['|', '/', '-', '\\']


def loading():
    """
    Prints a silly little loading icon so the user doesn't worry that something is broken
    """
    global load_index
    print(f'\x08{load_arr[load_index]}', end='')
    load_index += 1
    load_index = load_index % 4

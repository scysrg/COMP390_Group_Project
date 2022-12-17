"""
ui_funcs handles terminal printing, user input, and all things interface.
"""
import database_funcs as db
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

relations_list = ['<', '>', '<=', '>=', '=']


def do_everything():
    """
    Don't mind this, I promise it won't be this long or do_everything forever. This is the main track for the UI
    functionality
    """
    print(keyword_prompt)
    while 1:
        keyword_input = input('>>')
        try:  # Error Case: unacceptable input
            product_query = keyword_dict[keyword_input]
        except KeyError:
            print("Please enter a valid query as a number between 1 and 6", end='')
            continue  # Call prompt again
        break
    print(f'Searching for {product_query}...')
    rating_query = prompt('star rating', 0.0, 5.0)
    num_ratings_query = prompt('number of ratings', 0.0, 0xffffffff)
    price_query = prompt('price', 0.0, 0xffffffff)

    data: list = db.fetch_data(product_query, rating_query, num_ratings_query, price_query)
    search_query_str = f"Found {len(data)} {product_query}'s with {rating_query}, {num_ratings_query}, {price_query}\n"
    print(search_query_str)
    util.clear(product_query)
    util.write(search_query_str, product_query)
    for entry in data:
        entry = process_entry(entry)
        print(entry)
        util.write(entry, product_query)


def prompt(prompt_type: str, min_range, max_range):
    print(f'Target {prompt_type}? Hit Enter/Return for all', end='')
    while 1:  # Prompts user for the target value
        target_prompt_type = input(': ')
        if target_prompt_type == '':  # Case: User wants all in prompt_type
            return 0.0, '>='
        try:  # Error Case: unacceptable input
            target_prompt_type = float(target_prompt_type)
            check_range(target_prompt_type, min_range, max_range)
        except (TypeError, ValueError):
            print(f'Please enter a valid value between {min_range}, {max_range}', end='')
            continue
        break

    print(f'Choose relation operator for target from {relations_list}', end='')
    while 1:  # Prompts user for the (in)equality statement
        target_prompt_relation = input(': ')
        if target_prompt_relation in relations_list:
            return target_prompt_type, target_prompt_relation
        print('Please enter a valid relation from the list', end='')


def check_range(val, min_range, max_range):
    if val < min_range:
        raise ValueError
    elif val > max_range:
        raise ValueError


def process_entry(entry: list):
    return f'{entry[0]}\n' \
           f'Avg. Rating: {entry[1]}*, Num. Ratings: {entry[2]}.' \
           f'${entry[3]}' \
           f'{entry[4]}'


if __name__ == '__main__':
    do_everything()

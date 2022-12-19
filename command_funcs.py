import database_funcs as db
import scrapping_funcs
import ui_funcs as ui

key_words_list= ['Over Ear Headphones', 'USB Microphones', '1080p Webcams', 'Capture Cards', '8-channel Audio Mixers', 'Gaming Laptops']
db_name = 'amazon_listings.db'
database_key_array = ['over_ear_headphones', 'usb_microphones', 'webcams_1080p', 'capture_cards', 'audio_mixers_8channel', 'gaming_laptops']

def _scrape_data(key_words, pg_num, table_listing, listing_counter, total_listings):
    search_url = scrapping_funcs.get_target_url(pg_num, key_words)
    search_results = scrapping_funcs.get_one_page(search_url)
    for item in search_results:
        listing_counter += 1
        if listing_counter > total_listings:
            break
        db_data_entry = [None, None, None, None, None]
        # FIll array with data
        db_data_entry[0] = scrapping_funcs.get_product_title(item)
        db_data_entry[1] = scrapping_funcs.get_product_ratings(item)
        db_data_entry[2] = scrapping_funcs.get_num_of_rating(item)
        db_data_entry[3] = scrapping_funcs.get_product_price(item)
        db_data_entry[4] = scrapping_funcs.get_url_string(item)
        db.populate_row(table_listing, db_data_entry[0], db_data_entry[1], db_data_entry[2], db_data_entry[3], db_data_entry[4])
    return listing_counter
def enter_database_data():
    """Creates and then populates the database with LIMIT of 300 listings each"""
    db.create_amazon_database()
    print('Database created')
    listing_counter = 0
    listing_limit = 300
    page_number = 1
    key_tracker = 0
    # gather and add data into DB with a LIMIT of 300 listings
    for key_words in key_words_list:
        # while TOTAL listings in UNDER 300
        print(f'Scraping {key_words}...')
        while listing_counter < listing_limit:
            print(f'Found {listing_counter} listings')
            listing_counter = int(_scrape_data(key_words, page_number, database_key_array[key_tracker], listing_counter, listing_limit))
            page_number += 1
        key_tracker += 1
        # reset the number of listings for the next search result
        listing_counter = 0
        page_number = 0


def handle_query():
    """
    handles the track for collecting user query and sending it to user in a readable format
    :return bool: True if the user wishes to continue, otherwise False
    """
    query = ui.get_user_query()
    data = db.fetch_data(product=query[0], rating=query[1], num_ratings=query[2], price=query[3])
    ui.print_query_results(data, product=query[0], rating=query[1], num_ratings=query[2], price=query[3])
    return ui.cont()

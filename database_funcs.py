'''Database class with functions that create and populate the database'''
import sqlite3

# Database Name
db_name = 'amazon_listings.db'
# Array of the names for each table in the database, used as keys
listings_array = ['over_ear_headphones', 'usb_microphones', 'webcams_1080p', 'capture_cards', 'audio_mixers_8channel', 'gaming_laptops']

def _convert_to_int(data_string):
    '''Converts a given string into an integer for the database, if error returns null'''
    try:
        return int(data_string)
    except:
        return None
def _convert_to_float(data_string):
    '''Converts a given string into a float for the database, if error returns null'''
    try:
        return float(data_string)
    except:
        return None

def populate_row(table_key, product_name, rating, num_ratings, price, product_url):
    '''Inserts the date into the correct database'''
    try:
        db_connection = sqlite3.connect(db_name)
        db_cursor = db_connection.cursor()
        db_cursor.execute(f'''INSERT INTO {table_key} VALUES(?, ?, ?, ?, ?)''', (product_name, _convert_to_float(rating), _convert_to_int(num_ratings), _convert_to_float(price), product_url))
        db_connection.commit()
    except sqlite3.Error as db_error:
            print(f' (populate_database) A database error has occurred: {db_error}')
    finally:
            # if a conenction exists, close the connection
            if db_connection:
                db_connection.close()

def _create_tables(db_cursor):
    '''Adds the tables to the database'''
    for key in listings_array:
                db_cursor.execute(f'''CREATE TABLE IF NOT EXISTS {key}(
                                    product_name TEXT,
                                    rating REAL,
                                    num_ratings INTEGER,
                                    price REAL,
                                    product_url TEXT);''')
                db_cursor.execute(f'''DELETE FROM {key}''')

def create_amazon_database():
    '''Creates the database'''
    try:
        db_connection = sqlite3.connect(db_name)
        db_cursor = db_connection.cursor()
        _create_tables(db_cursor)
        db_connection.commit()
    except sqlite3.Error as db_error:
        print(f'(create_amazon_database) A database error has occurred: {db_error}')
    finally:
        if db_connection:
            db_connection.close()


def fetch_data(**query):
    """
    Fetches all the data queried by the user
    :param query: product, rating (tuple), num_ratings (tuple), price (tuple): user input query
        Tuples should be in the form (relation, value).
    :return data: list fetched from database matching the query
    :raises db_error: catch for potential database errors
    """
    try:
        db_connection = sqlite3.connect(db_name)
        db_cursor = db_connection.cursor()
        db_cursor.execute(f'''SELECT * FROM {query['product']} WHERE 
                            rating {query['rating'][0]} {query['rating'][1]} AND
                            num_ratings {query['num_ratings'][0]} {query['num_ratings'][1]} AND
                            price {query['price'][0]} {query['price'][1]}''')
        return db_cursor.fetchall()
    except sqlite3.Error as db_error:
        print(f'(fetch_data) A database error has occurred: {db_error}')
    finally:
        if db_connection:
            db_connection.close()

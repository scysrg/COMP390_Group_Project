'''Database class with functions that create and populate the database'''
import sqlite3

# Database Name
db_name = 'amazon_listings.db'
# Array of the names for each table in the database, used as keys
listings_array = ['over_ear_headphones', 'usb_microphones', 'webcams_1080p', 'capture_cards', 'audio_mixers_8channel', 'gaming_laptops']


def _check_value_type(rating, price):
    '''Checks if ratings, number of ratings and the price are numbers'''
    try:
        float(rating)
        float(price)
        return True
    except TypeError as type_error:
        print(f' (_check_value_type) A type error has occurred: {type_error}')
        return False
    except ValueError as val_error:
        print(f' (_check_value_type) A value error has occurred: {val_error}')
        return False

def populate_row(table_key, product_name, rating, num_ratings, price, product_url):
    '''Inserts the date into the correct database'''
    try:
        db_connection = sqlite3.connect(db_name)
        db_cursor = db_connection.cursor()
        if _check_value_type(rating, price,) == True:
            db_cursor.execute(f'''INSERT INTO {table_key} VALUES(?, ?, ?, ?, ?)''', (product_name, rating, num_ratings, price, product_url))
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


def fetch_data(product_table, rating_query: tuple, num_ratings_query: tuple, price_query: tuple):
    """
    Fetches all the data queried by the user
    :param product_table: the product keyword, title of the table, type of product
    :param rating_query: tuple containing (float rating, string relation), ex. (4.3, '<=')
    :param num_ratings_query: tuple containing (float num_ratings, string relation)
    :param price_query: tuple containing (float price, string relation)
    :return: data: list fetched from database matching the query
    :raises: db_error: catch for potential database errors
    """
    try:
        db_connection = sqlite3.connect(db_name)
        db_cursor = db_connection.cursor()
        db_cursor.execute(f'''SELECT * FROM {product_table} WHERE 
                            rating {rating_query[1]} {rating_query[0]} AND
                            num_ratings {num_ratings_query[1]} {num_ratings_query[0]} AND
                            price {price_query[1]} {price_query[0]}''')
        return db_cursor.fetchall()
    except sqlite3.Error as db_error:
        print(f'(fetch_data) A database error has occurred: {db_error}')
    finally:
        if db_connection:
            db_connection.close()

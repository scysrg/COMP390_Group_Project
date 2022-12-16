'''Database class with functions that create and populate the database'''
import sqlite3

# Database Name
db_name = 'amazon_listings.db'
# Array of the names for each table in the database, used as keys
listings_array = ['over_ear_headhpones', 'usb_microphones', 'webcams_1080p', 'capture_cards', 'audio_mixers_8channel', 'gaming_laptops']

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
        pass
    finally:
        # if a conenction exists, close the connection
        if db_connection:
            db_connection.close()
        print('Database closed')

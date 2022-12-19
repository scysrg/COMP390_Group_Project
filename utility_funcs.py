def format_rating(rating_str: str):
    """This function removes 'out of 5 stars' from incoming string. """
    rating_str = rating_str.replace(" out of 5 stars", "")
    return rating_str


def string_is_float(in_string):
    """This function returns True if the incoming parameter is a float, returns False otherwise """
    try:
        float(in_string)
        return True
    except TypeError:
        return False
    except ValueError:
        return False


def string_is_integer(in_string):
    """This function returns True if the incoming parameter is a float, returns False otherwise """
    try:
        int(in_string)
        return True
    except TypeError:
        return False
    except ValueError:
        return False


def write(line: str, product: str):
    file = open(f'{product}_results.txt', 'a')
    file.write(line)
    file.close()


def clear(product: str):
    file = open(f'{product}_results.txt', 'w')
    file.close()

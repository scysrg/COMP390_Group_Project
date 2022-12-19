def format_rating(rating_str: str):
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
    """
    Writes a line to the search file for the product
    :param line: the line to be written
    :param product: the product under which the line is searched for
    """
    file = open(f'{product}_results.txt', 'a', encoding='UTF=8')
    file.write(line)
    file.write('\n')
    file.close()


def clear(product: str):
    """
    Simply clears the search file for product
    :param product: the product of which the file is for
    """
    file = open(f'{product}_results.txt', 'w')
    file.close()


def clean(string: str):
    """
    'Cleans' up the string entered, removing '(', ')', '\', ',' for formatting reasons
    :param string: The string to be cleaned
    :return: The cleaned string
    """
    string = string.replace('(', '')
    string = string.replace(')', '')
    string = string.replace('\'', '')
    string = string.replace(',', '')
    return string

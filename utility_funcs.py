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
    file = open(f'{product}_results.txt', 'a', encoding='UTF=8')
    file.write(line)
    file.write('\n')
    file.close()


def clear(product: str):
    file = open(f'{product}_results.txt', 'w')
    file.close()


def clean(string: str):
    string = string.replace('(', '')
    string = string.replace(')', '')
    string = string.replace('\'', '')
    return string
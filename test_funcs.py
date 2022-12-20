"""This tests the functions of all core classes"""
import pytest

import command_funcs as commands
import scraping_funcs
from database_funcs import *
from ui_funcs import *
from io import StringIO


def test_populate_row(capfd):

    # Will add the data to the correct table over_ear_headphones
    commands.enter_database_data()
    assert populate_row('over_ear_headphones', 'Generic overpriced headphones', 4.9, 1, 122.99, 'URL to awful headphones') == None

    # Number of ratings given exceeds integer limit
    with pytest.raises(OverflowError) as exception_info:
        populate_row('over_ear_headphones', 'Generic overpriced headphones', 4.9, 999999999999999999999, 129.99, 'URL to awful headphones')
    assert exception_info.type is OverflowError

    # Given the wrong table key, caught by try/except and prints error
    populate_row('usb microphones', None, None, None, None, None)
    out, err = capfd.readouterr()
    assert out == '(populate_database) A database error has occurred: near "microphones": syntax error\n'

def test_check_input():
    assert check_input('32', 0, 50)
    assert not check_input('32', 0, 25)
    assert not check_input('Fred', 0, 5)


def test_prompt_query(capfd, monkeypatch):
    # Determine what inputs could potentially crash the UI
    test_str = '\n'
    sim_input = StringIO(test_str)
    monkeypatch.setattr('sys.stdin', sim_input)
    assert prompt_query('star rating', 0.0, 5.0) == ('>=', 0.0)
    out, err = capfd.readouterr()
    assert out == 'Target star rating? Hit Enter/Return for all: '

    with pytest.raises(EOFError) as error:
        test_str = 'Apple'
        sim_input = StringIO(test_str)
        monkeypatch.setattr('sys.stdin', sim_input)
        prompt_query('star rating', 0, 99)
        out, err = capfd.readouterr()
        assert out == 'Target star rating? Hit Enter/Return for all: ' \
                      'Please enter a valid value between 0, 99: '
    assert error.type is EOFError

    with pytest.raises(EOFError) as error:
        test_str = '-1'
        sim_input = StringIO(test_str)
        monkeypatch.setattr('sys.stdin', sim_input)
        prompt_query('star rating', 0, 5)
        out, err = capfd.readouterr()
        assert out == 'Target star rating? Hit Enter/Return for all: ' \
                      'Please enter a valid value between 0, 99: '
    assert error.type is EOFError

    with pytest.raises(EOFError) as error:
        test_str = '3.5\n><'
        sim_input = StringIO(test_str)
        monkeypatch.setattr('sys.stdin', sim_input)
        prompt_query('star rating', 0, 5)
        out, err = capfd.readouterr()
        assert out == 'Target star rating? Hit Enter/Return for all: ' \
                      "Choose relation operator for target from relations_list = ['<', '>', '<=', '>=', '==']: " \
                      'Please enter a valid relation from the list: '
    assert error.type is EOFError

    test_str = '3.5\n>='
    sim_input = StringIO(test_str)
    monkeypatch.setattr('sys.stdin', sim_input)
    assert prompt_query('star rating', 0, 5) == ('>=', '3.5')


def test_prompt_product(capfd, monkeypatch):
    with pytest.raises(EOFError) as error:
        test_str = 'Apple'
        sim_input = StringIO(test_str)
        monkeypatch.setattr('sys.stdin', sim_input)
        prompt_product()
        out, err = capfd.readouterr()
        assert out == ">>Please enter a valid query as a number between 1 and 6>>"
    assert error.type is EOFError

    with pytest.raises(EOFError) as error:
        test_str = '7'
        sim_input = StringIO(test_str)
        monkeypatch.setattr('sys.stdin', sim_input)
        prompt_product()
        out, err = capfd.readouterr()
        assert out == ">>Please enter a valid query as a number between 1 and 6>>"
    assert error.type is EOFError

    with pytest.raises(EOFError) as error:
        test_str = '\n'
        sim_input = StringIO(test_str)
        monkeypatch.setattr('sys.stdin', sim_input)
        prompt_product()
        out, err = capfd.readouterr()
        assert out == ">>Please enter a valid query as a number between 1 and 6>>"
    assert error.type is EOFError

    test_str = '1'
    sim_input = StringIO(test_str)
    monkeypatch.setattr('sys.stdin', sim_input)
    assert prompt_product() == 'over_ear_headphones'

def test_get_target_url():
    assert scraping_funcs.get_target_url(3,'test function') == 'https://www.amazon.com/s?k=test+function&page=3'
    assert scraping_funcs.get_target_url(2,'') == 'https://www.amazon.com'
    # this link will rediret you to amazon main page
    assert scraping_funcs.get_target_url(2,' ') == 'https://www.amazon.com/s?k=+&page=2'

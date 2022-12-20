"""This tests the functions of all core classes"""
import pytest
import database_funcs as db
import ui_funcs as ui
from io import StringIO

def test_populate_row(capfd):

    # Number of ratings given exceeds integer limit
    with pytest.raises(OverflowError) as exception_info:
        db.populate_row('over_ear_headphones', 'Generic overpriced headphones', 4.9, 999999999999999999999, 129.99, 'URL to awful headphones')
    assert exception_info.type is OverflowError

    # Given the wrong table key, caught by try/except and prints error
    db.populate_row('usb microphones', None, None, None, None, None)
    out, err = capfd.readouterr()
    assert out == '(populate_database) A database error has occurred: near "microphones": syntax error\n'

def test_prompt_query(capfd, monkeypatch):
    # Determine what inputs could potentially crash the UI
    test_str = ''
    sim_input = StringIO(test_str)
    monkeypatch.setattr('sys.stdin', sim_input)
    assert ui.prompt_query('star rating', 0.0, 5.0) == '>=', 0.0

    # test_str = 'dfshsgh'
    # sim_input = StringIO(test_str)
    # monkeypatch.setattr('sys.stdin', sim_input)
    # assert ui.prompt_query('random', 0.0, 5.0) == 'Please enter a valid relation from the list'

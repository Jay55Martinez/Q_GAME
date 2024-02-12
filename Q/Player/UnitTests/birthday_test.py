#!/usr/bin/env python3
# tests the birthday class
import pytest
import sys
sys.path.insert(0, '../../Common')
from public_game_state import *
sys.path.insert(0, '../')
from player import Birthday

def init_birthday():
    l_birthdays = []
    feb212003 = Birthday(2, 21, 2003)
    may212004 = Birthday(4, 21, 2004)
    nov202002 = Birthday(11, 20, 2002)
    l_birthdays.append(feb212003)
    l_birthdays.append(may212004)
    l_birthdays.append(nov202002)
    return l_birthdays

def test_equal():
    l_birthdays = init_birthday()
    feb212003 = l_birthdays[0]
    may212004 = l_birthdays[1]
    feb212011 = Birthday(2, 21, 2011)
    v2_feb212003 = Birthday(2, 21, 2003)
    
    assert not feb212003 == feb212011
    assert feb212003 == v2_feb212003
    assert not feb212003 == may212004

# when the script runs it runs using pytest
if __name__ == "__main__":
    pytest.main(["-v", "birthday_test.py"])
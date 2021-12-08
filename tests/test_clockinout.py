import pytest
from pytest import approx
import sys
import os

sys.path.append("../modules")

from sqlite_handler import (
    Database
)

db_name = "test.db"
db = Database(db_name)

def test_create_table():
    res = db.create_table("users", {"id": "INTEGER PRIMARY KEY", "first_name": "TEXT", "last_name": "TEXT", "eid": "TEXT", "password": "TEXT", "is_admin": "INT", "clock_in_time": "TEXT", "clock_out_time": "TEXT"})
    assert res == (1,)

def test_create_child_table():
    res = db.create_child_table("timestamp", {"id": "INTEGER PRIMARY KEY", "date": "TEXT", "clock_in": "STRING", "clock_out": "STRING", "late": "INT", "too_early": "INT", "exception    ": "INT", "exception_description": "TEXT", "user": "INT"}, "user", "users", "id") 
    assert res == (1,)

def test_create_user():
    res = db.create_user(["Wilson", "Romero", "EID123456", "Wilson4291", "10:50AM", "19:00PM", 1])   
    assert res == (1, 'Wilson', 'Romero', 'EID123456', 'cb64a867e9b1f44a5f67223289806c33ee388f7a1e34d4b0a890475d72702a26', 1, '10:50AM', '19:00PM')

def test_create_timestamp():
    res = db.create_timestamp(["", "", 0, 0, 0, "", 1])
    assert res == (1, '12/05/2021', '', '', 0, 0, 0, '', 1)

def test_update_user():
    res = db.update_user(1,{"is_admin": 0})
    assert res == (1, 'Wilson', 'Romero', 'EID123456', 'cb64a867e9b1f44a5f67223289806c33ee388f7a1e34d4b0a890475d72702a26', 0, '10:50AM', '19:00PM')
    res = db.update_user(1,{"is_admin": 1})
    assert res == (1, 'Wilson', 'Romero', 'EID123456', 'cb64a867e9b1f44a5f67223289806c33ee388f7a1e34d4b0a890475d72702a26', 1, '10:50AM', '19:00PM')

def test_update_timestamp():
    res = db.update_timestamp(1, {"clock_in": "10:50AM"})
    assert res == (1, '12/05/2021', '10:50AM', '', 0, 0, 0, '', 1)

if __name__ == '__main__':
    pytest.main(["-v", "--tb=line", "-rN", __file__])
    os.remove(db_name)

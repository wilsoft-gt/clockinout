from datetime import datetime, date
from dataclasses import dataclass
from time import time
import re

@dataclass
class User_data:
    data = {}

    def get_data(self) -> dict:
        return self.data

    def set_data(self, data):
        self.data = data

class dotdict(dict):
    """Dot notation to dictionary attributes"""
    __getattr__ = dict.get

def is_time_format(value):
    result = re.match(r"^(2[0-3]|[01]?[0-9]):([0-5]?[0-9])[A-z][A-z]$",value)
    if result:
        return True

    return False

@dataclass
class DateTimeHelper:
    def get_str_time(self) -> datetime:
        return datetime.now().strftime("%H:%M%p")
    
    def get_str_date(self) -> datetime:
        return datetime.now().strftime("%m/%d/%Y")
    
    def get_obj_time(self, time) -> datetime:
        return datetime.now().strptime(time, "%H:%M%p")

    def get_obj_date(self, date) -> datetime:
        return datetime.now().strptime(date, "%m/%d/%Y")

    def substract_str_time(self, start, end) -> int:
        start = self.get_obj_time(start)
        end = self.get_obj_time(end)
        result = datetime.combine(date.today(), start.time()) - datetime.combine(date.today(), end.time())
        return int(result.total_seconds() / 60)

USER_INDEXES = dotdict({
    "ID": 0,
    "FIRST_NAME": 1,
    "LAST_NAME": 2,
    "EID": 3,
    "PASSWORD": 4,
    "IS_ADMIN": 5,
    "CLOCK_IN_TIME": 6,
    "CLOCK_OUT_TIME": 7
})

TIMESTAMP_INDEXES = dotdict({
    "ID": 0,
    "DATE": 1,
    "CLOCK_IN": 2,
    "CLOCK_OUT": 3,
    "LATE": 4,
    "TOO_EARLY": 5,
    "EXCEPTION": 6,
    "EXCEPTION_DESCRIPTION": 7,
    "USER": 8
})

PRIMARY = "#878DFA"
PRMARY_DARK = "#666AAD"
BACKGROUND = "#FAE488"
BACKGROUND_DARK = "#AD9A4C"

if __name__ == "__main__":
    print("this is just a helper module and should not be used as standard executable")

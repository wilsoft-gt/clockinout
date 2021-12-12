from datetime import datetime, date

class User_data:
    def __init__(self):
        self.data = {}

    def get_data(self):
        return self.data

    def set_data(self, data):
        self.data = data

class dotdict(dict):
    """Dot notation to dictionary attributes"""
    __getattr__ = dict.get

class DateTimeHelper:
    def get_str_time(self):
        return datetime.now().strftime("%H:%M%p")
    
    def get_str_date(self):
        return datetime.now().strftime("%m/%d/%Y")
    
    def get_obj_time(self, time):
        return datetime.now().strptime(time, "%H:%M%p")

    def get_obj_date(self, date):
        return datetime.now().strptime(date, "%m/%d/%Y")

    def substract_str_time(self, start, end):
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

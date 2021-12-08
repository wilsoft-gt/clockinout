class dotdict(dict):
    """Dot notation to dictionary attributes"""
    __getattr__ = dict.get


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

from modules.sqlite_handler import Database
from modules.user_interface import ClockInOutGui

def main():
    ClockInOutGui().run()

if __name__ == '__main__':
    Database().initial_setup()
    main()

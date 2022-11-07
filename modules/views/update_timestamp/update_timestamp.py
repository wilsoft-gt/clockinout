from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout

from modules.helpers import USER_INDEXES, TIMESTAMP_INDEXES
from modules.sqlite_handler import Database

class UserAdminUpdateTimestampLayout(GridLayout):
    def __init__(self, **kwargs):
        super(UserAdminUpdateTimestampLayout, self).__init__(**kwargs)
        self.db = Database()
        self.timestamp_data = []
        self.updated_timestamp = {}
        self.user_data = []

    #get timestamp data and then update the fields with the retrieved data
    def get_timestamp_data(self, instance, user_id, date_field, user_input, inputs):
        self.user_data = self.db.get_user(user_id.text)
        user_id = self.user_data[USER_INDEXES.ID]
        user_name = f"{self.user_data[USER_INDEXES.FIRST_NAME]} {self.user_data[USER_INDEXES.LAST_NAME]}"
        user_input.text = user_name

        if date_field.text != "":
            self.timestamp_data = self.db.get_timestamp(user_id, date_field.text)
        else:
            self.timestamp_data = self.db.get_timestamp(user_id)

        #TODO: Move this to a new function
        #input is an array with all the widgets, the index is -2 because clock_in is in position 2
        inputs[TIMESTAMP_INDEXES.CLOCK_IN-2].text = self.timestamp_data[TIMESTAMP_INDEXES.CLOCK_IN]
        inputs[TIMESTAMP_INDEXES.CLOCK_OUT-2].text = self.timestamp_data[TIMESTAMP_INDEXES.CLOCK_OUT]
        inputs[TIMESTAMP_INDEXES.LATE-2].text = str(self.timestamp_data[TIMESTAMP_INDEXES.LATE])
        inputs[TIMESTAMP_INDEXES.TOO_EARLY-2].text = str(self.timestamp_data[TIMESTAMP_INDEXES.TOO_EARLY])
        inputs[TIMESTAMP_INDEXES.EXCEPTION-2].text = str(self.timestamp_data[TIMESTAMP_INDEXES.EXCEPTION])
        inputs[TIMESTAMP_INDEXES.EXCEPTION_DESCRIPTION-2].text = self.timestamp_data[TIMESTAMP_INDEXES.EXCEPTION_DESCRIPTION]
    

    def update_new_data(self, instance, value):
        #the .name property is a custom property to hold the widget id
        if value == "":
            del self.updated_timestamp[instance.name]
        else:
            if instance.name == "late" or instance.name == "too_early" or instance.name == "exception":
                self.updated_timestamp[instance.name] = int(value)
            else:
                self.updated_timestamp[instance.name] = value
 
    
    def save_new_data(self, date_field, message):
        #date_field is the widget that holds the date to search
        user_id = self.user_data[USER_INDEXES.ID]
        timestamp_id = self.timestamp_data[TIMESTAMP_INDEXES.ID]
        if date_field.text == "":
            self.db.update_timestamp(user_id, self.updated_timestamp)
        else:
            self.db.update_timestamp(user_id, self.updated_timestamp, timestamp_id)

        message.text = "Data has been modified!"
        

    def go_back(self):
        app = App.get_running_app()
        app.root.current = "main_menu"

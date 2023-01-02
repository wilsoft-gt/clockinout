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


    def set_data_fields(self, inputs):
        '''
            INFO:
            -----
                Populates the inputs with the retrieved data.
                Nees to be -2 since the clock_in index is 2 because 
                of ID has an index = 0 and date has index = 1 (check helpers module)
            INPUT:
            ------
                inputs: A list of the inputs to change the text value
        '''
        inputs[TIMESTAMP_INDEXES.CLOCK_IN-2].text = self.timestamp_data[TIMESTAMP_INDEXES.CLOCK_IN]
        inputs[TIMESTAMP_INDEXES.CLOCK_OUT-2].text = self.timestamp_data[TIMESTAMP_INDEXES.CLOCK_OUT]
        inputs[TIMESTAMP_INDEXES.LATE-2].text = str(self.timestamp_data[TIMESTAMP_INDEXES.LATE])
        inputs[TIMESTAMP_INDEXES.TOO_EARLY-2].text = str(self.timestamp_data[TIMESTAMP_INDEXES.TOO_EARLY])
        inputs[TIMESTAMP_INDEXES.EXCEPTION-2].text = str(self.timestamp_data[TIMESTAMP_INDEXES.EXCEPTION])
        inputs[TIMESTAMP_INDEXES.EXCEPTION_DESCRIPTION-2].text = self.timestamp_data[TIMESTAMP_INDEXES.EXCEPTION_DESCRIPTION]

    def clear_inputs(self, inputs, search_input):
        for input in inputs+search_input:
            if hasattr(input, 'cursor'):
                input.text = ''

        search_input.text = ''

    def get_timestamp_data(self, instance, user_id, date_field, user_input, inputs, message):
        '''
            INFO:
            -----
                Retrieve the user data and timestamp from database.
            Input:
            ------
                user_id: This is the user ID whose timestamp wants to be changed.
                date_field: The date of the timestamp we want to change
                user_info: The field that will hold the user name
                inputs: A list of the inputs that maps to the timestamp data
                message: The message label that will display the result
        '''
        try:
            self.user_data = self.db.get_user(user_id.text)
            user_name = f"{self.user_data[USER_INDEXES.FIRST_NAME]} {self.user_data[USER_INDEXES.LAST_NAME]}"
            user_input.text = user_name
            user_db_id = self.user_data[USER_INDEXES.ID]

            if date_field.text != "":
                self.timestamp_data = self.db.get_timestamp(user_db_id, date_field.text)
            else:
                self.timestamp_data = self.db.get_timestamp(user_db_id)

            #populate data
            self.set_data_fields(inputs)
        except Exception as e:
            message.color = "red"
            message.text = f"{e}"
    

    def update_new_data(self, instance, value):
        '''
            INFO:
            -----
                Update the dictionary that will hold the updated value

            INPUT:
            ------
                instance: the text input instance that is being changed
                value: the new value
        '''
        if value == "":
            del self.updated_timestamp[instance.name]
        else:
            if instance.name == "late" or instance.name == "too_early" or instance.name == "exception":
                self.updated_timestamp[instance.name] = int(value)
            else:
                self.updated_timestamp[instance.name] = value
 
    
    def save_new_data(self, date_field, message):
        '''
            INFO:
            -----
                Save the new data to the database
            INPUT:
            ------
                date_field: The field that holds the date to be updated
        '''
        try:
            user_id = self.user_data[USER_INDEXES.ID]
            timestamp_id = self.timestamp_data[TIMESTAMP_INDEXES.ID]
            if date_field.text == "":
                self.db.update_timestamp(user_id, self.updated_timestamp)
            else:
                self.db.update_timestamp(user_id, self.updated_timestamp, timestamp_id)

            message.text = "Data has been modified!"
        except Exception as e:
            message.color = "red"
            message.text = f"{e}"

    def go_back(self):
        '''Returns to the main menu'''
        app = App.get_running_app()
        app.root.current = "main_menu"
        self.clear_inputs(self.children[1].children, self.children[2].children)

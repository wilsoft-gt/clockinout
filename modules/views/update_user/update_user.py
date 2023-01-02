from modules.sqlite_handler import Database
from modules.helpers import USER_INDEXES, is_time_format

from kivy.app import App
from kivy.uix.gridlayout import GridLayout

class UserAdminUpdateUserLayout(GridLayout):
    def __init__(self, **kwargs):
        super(UserAdminUpdateUserLayout, self).__init__(**kwargs)
        self.db = Database()
        self.new_user_data = {}
        self.user_data = [] 

    def set_inputs_info(self, inputs):
        '''
            INFO:
            =====
                Update each text field with the data retrieved from DB

            Inputs:
            -------
                inputs: The list of text inputs
        '''
        inputs[USER_INDEXES.FIRST_NAME-1].text = self.user_data[USER_INDEXES.FIRST_NAME]
        inputs[USER_INDEXES.LAST_NAME-1].text = self.user_data[USER_INDEXES.LAST_NAME]
        inputs[USER_INDEXES.EID-1].text = self.user_data[USER_INDEXES.EID]
        inputs[USER_INDEXES.IS_ADMIN-2].text = str(self.user_data[USER_INDEXES.IS_ADMIN])
        inputs[USER_INDEXES.CLOCK_IN_TIME-2].text = self.user_data[USER_INDEXES.CLOCK_IN_TIME]
        inputs[USER_INDEXES.CLOCK_OUT_TIME-2].text = self.user_data[USER_INDEXES.CLOCK_OUT_TIME]

    def clear_inputs(self, inputs, search_eid):
        for input in inputs:
            if hasattr(input, "cursor"):
                input.text = ""
        search_eid.text = ""

    def get_user_data(self, search_eid, inputs, message):
        '''
            INFO:
            =====
                Get the user data from database
                
            Inputs:
            -------
                search_eid: The input containing the user EID
                inputs: The list of inputs we will update with the new data
                message: The message label to show any error / success message
        '''
        try:
            message.text = ""
            self.user_data = self.db.get_user(search_eid.text)
            self.set_inputs_info(inputs)
        except Exception as e:
            self.clear_inputs(inputs, search_eid)
            message.text = f"User not found"
            message.color = "red"

    def update_new_data(self, input):
        '''
            INFO:
            =====
                Update the field info in the temporary dictionary
                
            Inputs:
            -------
                input: The input that is being changed
        '''
        if input.text == "":
            del self.new_user_data[input.name]
        else:
            self.new_user_data[input.name] = input.text
 
    def save_new_data(self, message):
        '''
            INFO:
            =====
                Save the new user data to the database
                
            Inputs:
            -------
                message: The message label to show any error / success message
        '''
        try:
            for key, value in self.new_user_data.items():
                if value == "":
                    raise ValueError(f"{key} can't be empty.")
                if key in ["clock_in_time", "clock_out_time"] and not is_time_format(value):
                    raise ValueError(f"Time not matching format")
                if key == "is_admin" and value not in ["1","0"]:
                    raise ValueError("Admin value must be 1 or 0 ")

            self.db.update_user(self.user_data[USER_INDEXES.ID],self.new_user_data)
            message.text = "User updated"
            message.color = "green"

        except Exception as e:
            message.text = f"{e}"
            message.color = "red"
            
    def go_back(self):

        app = App.get_running_app()
        app.root.current = "main_menu"
        self.clear_inputs(self.children[1].children, self.children[2].children[1])

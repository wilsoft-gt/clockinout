from modules.sqlite_handler import Database
from modules.helpers import USER_INDEXES

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
            self.user_data = self.db.get_user(search_eid.text)
            self.set_inputs_info(inputs)
        except Exception as e:
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
            self.db.update_user(self.user_data[USER_INDEXES.ID],self.new_user_data)
            
        except Exception as e:
            message.text = f"{e}"
            
    def go_back(self):
        app = App.get_running_app()
        app.root.current = "main_menu"

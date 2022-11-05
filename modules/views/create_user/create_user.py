
import sqlite3
from modules.sqlite_handler import Database
from modules.helpers import is_time_format

from kivy.app import App
from kivy.uix.gridlayout import GridLayout

class UserAdminCreateUserLayout(GridLayout):
    def __init__(self, **kwargs):
        super(UserAdminCreateUserLayout, self).__init__(**kwargs)
        self.db = Database()

    def save_new_data(self, instance, message_label):
        try:
            for item in instance:
                if item.text == "":
                    raise ValueError(f"{item.name} can't be empty")

            if not is_time_format(instance[4].text) or not is_time_format(instance[5].text):
                raise ValueError(f"Time not matching format")

            if instance[-1].text not in ["1", "0"]:
                raise ValueError("Is admin must be number 1 or 0")

            self.db.create_user([ item.text for item in instance ])
            for item in instance:
                item.text = ""
            message_label.text = "User was created successfully!"
            message_label.color = "green"
        
        except  sqlite3.DatabaseError as e:
            message_label.text = str(e)
            message_label.color = "red"

        except Exception as e:
            message_label.text = str(e)
            message_label.color = "red"

    def go_back(self, instance):
        app = App.get_running_app()
        app.root.current = "main_menu"

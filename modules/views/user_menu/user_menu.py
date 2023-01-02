from platform import release
from modules.helpers import USER_INDEXES, DateTimeHelper, TIMESTAMP_INDEXES
from modules.sqlite_handler import Database

from kivy.uix.gridlayout import GridLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.app import App
from kivy.properties import ObjectProperty


class ImageButton(ButtonBehavior, Image):
    pressed = ObjectProperty(None)
    released = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(ImageButton, self).__init__(**kwargs)
        self.bind(pressed=self.setter("pressed"))
        self.bind(released=self.setter("released"))

    def on_press(self):
        self.source = self.pressed

    def on_release(self):
        self.source = self.released
    
class UserMenuGridLayout(GridLayout):
    def __init__(self, **kwargs):
        super(UserMenuGridLayout, self).__init__(**kwargs)
        self.db = Database()
        self.user_data = {}

    def clock_in(self, message_label):
        """Check if there is already a timestamp and
        create punches for lates, early, etc."""
        try:
        
            res = self.db.get_timestamp(self.user_data[USER_INDEXES.ID])
            if res == None:
                late = 0
                early = 0
                time = DateTimeHelper().get_str_time() 
                difference = DateTimeHelper().substract_str_time(self.user_data[USER_INDEXES.CLOCK_IN_TIME], time)
                if difference < -5:
                    late=1
                self.db.create_timestamp([time, "", late, early, 0, "", self.user_data[USER_INDEXES.ID]])
                message_label.text = f"Successfully clocked in at {time}"
            else:
                message_label.text = "You already clocked in."
        except Exception as e:
            er = f"ERROR: {e}"
            message_label.text = er

    def clock_out(self, message_label):
        """Add the clock out time to the user timestamp"""
        try:
            timestamp = self.db.get_timestamp(self.user_data[USER_INDEXES.ID])
            user_id = self.user_data[USER_INDEXES.ID]
            early = 0
            time = DateTimeHelper().get_str_time() 
            difference = DateTimeHelper().substract_str_time(self.user_data[USER_INDEXES.CLOCK_OUT_TIME], time)
            if difference > 5:
                early = 1
            if timestamp[TIMESTAMP_INDEXES.CLOCK_OUT] == "":
                self.db.update_timestamp(user_id, {"clock_out": time, "too_early":early})
                message_label.text = f"Successfully clocked out at {time}"
            else:
                message_label.text = "You already clocked out."
        except Exception as e:
            er = f"ERROR: {e}"
            message_label.text = er

    def go_back(self, instance):
        app = App.get_running_app()

        if self.user_data[USER_INDEXES.IS_ADMIN] == 1:
            app.root.current = "main_menu"
        else:
            app.root.current = "login"

    def set_user_data(self, data):
        self.user_data = data
        self.children[2].text = f"Welcome {self.user_data[USER_INDEXES.FIRST_NAME]}" 

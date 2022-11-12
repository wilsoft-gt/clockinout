import csv
from .sqlite_handler import Database
from .helpers import USER_INDEXES

from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.screenmanager import ScreenManager, Screen, RiseInTransition

from .views.login.login import LoginGridLayout
Builder.load_file('modules/views/login/loginApp.kv')

from .views.user_menu.user_menu import UserMenuGridLayout
Builder.load_file('modules/views/user_menu/user_menu.kv')

from .views.main_layout.main_layout import AdminMainLayout
Builder.load_file('modules/views/main_layout/main_layout.kv')

from .views.create_user.create_user import UserAdminCreateUserLayout
Builder.load_file('modules/views/create_user/create_user.kv')

class ImageButton(ButtonBehavior, Image):
    def __init__(self, released, pressed, callback, **kwargs):
        super(ImageButton, self).__init__(**kwargs)
        self.pressed = pressed
        self.released = released
        self.callback = callback
        self.source = self.released

    def on_press(self):
        self.source = self.pressed

    def on_release(self):
        self.source = self.released
        self.callback()

from .views.update_timestamp.update_timestamp import UserAdminUpdateTimestampLayout
Builder.load_file("modules/views/update_timestamp/update_timestamp.kv")

from .views.update_user.update_user import UserAdminUpdateUserLayout
Builder.load_file("modules/views/update_user/update_user.kv")

class SaveReportLayout(GridLayout):
    def __init__(self, **kwargs):
        super(SaveReportLayout, self).__init__(**kwargs)
        self.app = App.get_running_app()
        self.db = Database()
        self.file_path = ""
        self.cols = 1
        self.padding=20
        self.minimum_height= 10
        self.height = (10, 10)

        self.filename_layout= GridLayout(cols=2, spacing=10, size_hint_y=0.2, row_default_height=40, row_force_default=True, pos_hint={"center_x": 0.5, "center_y": 0.5})
        self.filename_label = Label(text="File name", bold=True, color="#878DFA", size_hint_x=None, width=100, text_size=self.size, valign="center", halign="left")
        self.filename_input = TextInput()
        self.filename_layout.add_widget(self.filename_label)
        self.filename_layout.add_widget(self.filename_input)
        self.add_widget(self.filename_layout)

        self.file_path = FileChooserIconView(dirselect=True)
        self.file_path.children[0].color = "#878dfa"
        self.file_path.bind(selection=self.selection)
        self.add_widget(self.file_path)

        self.button_grid = GridLayout(cols=2, spacing=10, size_hint_y=0.1, row_default_height=40, row_force_default=True, pos_hint={"center_x": 0.5, "center_y": 0.5})
        self.cancel_button = Button(text="Cancel", on_press=self.go_back ,background_color = "#878DFA")
        self.save_button = Button(text="Save", on_press=self.save_file, background_color = "#878DFA")
        self.button_grid.add_widget(self.cancel_button)
        self.button_grid.add_widget(self.save_button)
        self.add_widget(self.button_grid)

    def selection(self, instance, touch):
        self.file_path = touch[0]
        
    def go_back(self, instance):
        self.app.root.current = "main_menu"

    def save_file(self, instance):
        filepath = f"{self.file_path}/{self.filename_input.text}.csv"
        users = self.db.get_all_users()
        data = []
        for user in users:
            timestamps = self.db.get_all_timestamps_form_user(user[USER_INDEXES.ID])               
            for timestamp in timestamps:
                comb = user + timestamp
                print(comb)
                data.append(comb)
       
        with open(f"{filepath}", "a") as file:
            headers = ["user_id", "first_name", "last_name", "employee_id", "clock_in_time", "clock_out_time", "is_admin", "timestamp_id", "date", "clock_in", "clock_out", "late", "too_early", "exception", "exeption_description", "user_id"]
            csv_out = csv.writer(file)
            csv_out.writerow(headers)
            for user in users:
                print(user)
                timestamps = self.db.get_all_timestamps_form_user(user[USER_INDEXES.ID])               
                for timestamp in timestamps:
                    comb = user + timestamp
                    csv_out.writerow(comb)
                   
        print("completado")            
            

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.add_widget(LoginGridLayout())

class AdminMainMenuScreen(Screen):
    def __init__(self, **kwargs):
        super(AdminMainMenuScreen, self).__init__(**kwargs)
        self.adminmainmenulayout = AdminMainLayout()
        self.add_widget(self.adminmainmenulayout)

class WelcomeScreen(Screen):
    def __init__(self, **kwargs):
        super(WelcomeScreen, self).__init__(**kwargs)
        self.usermenugridlayout = UserMenuGridLayout()
        self.add_widget(self.usermenugridlayout)

class AdminMenuCreateUserScreen(Screen):
    def __init__(self, **kwargs):
        super(AdminMenuCreateUserScreen, self).__init__(**kwargs)
        self.useradmincreateuserlayout = UserAdminCreateUserLayout()
        self.add_widget(self.useradmincreateuserlayout) 

class AdminMenuUpdateUserScreen(Screen):
    def __init__(self, **kwargs):
        super(AdminMenuUpdateUserScreen, self).__init__(**kwargs)
        self.useradminupdateuserlayout = UserAdminUpdateUserLayout()
        self.add_widget(self.useradminupdateuserlayout)

class AdminMenuUpdateTimestampScreen(Screen):
    def __init__(self, **kwargs):
        super(AdminMenuUpdateTimestampScreen, self).__init__(**kwargs)
        self.useradminupdatetimestamplayout = UserAdminUpdateTimestampLayout()
        self.add_widget(self.useradminupdatetimestamplayout)

class SaveReportScreen(Screen):
    def __init__(self, **kwargs):
        super(SaveReportScreen, self).__init__(**kwargs)
        self.savereportslayout = SaveReportLayout()
        self.add_widget(self.savereportslayout)

class ClockInOutGui(App):
    def build(self):
        Window.clearcolor=(0.9,0.9,0.9,1)
        tr = RiseInTransition()
        sm = ScreenManager(transition=tr)
        sm.add_widget(LoginScreen(name="login"))
        sm.add_widget(WelcomeScreen(name="user"))
        sm.add_widget(AdminMenuUpdateUserScreen(name="update_user_menu"))
        sm.add_widget(AdminMenuCreateUserScreen(name="create_user_menu"))
        sm.add_widget(AdminMenuUpdateTimestampScreen(name="update_timestamp_menu"))
        sm.add_widget(SaveReportScreen(name="save_report"))
        sm.add_widget(AdminMainMenuScreen(name="main_menu"))
        sm.current = "login"
        return sm


if __name__ == '__main__':
    ClockInOutGui().run()

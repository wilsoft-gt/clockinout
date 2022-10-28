from .sqlite_handler import Database
from .helpers import USER_INDEXES, TIMESTAMP_INDEXES, DateTimeHelper, User_data
from datetime import datetime
import csv
from kivy.lang import Builder

from .views.login.login import LoginGridLayout
Builder.load_file('modules/views/login/loginApp.kv')

from .views.main_layout.main_layout import AdminMainLayout
Builder.load_file('modules/views/main_layout/main_layout.kv')

from .views.user_menu.user_menu import UserMenuGridLayout
Builder.load_file('modules/views/user_menu/user_menu.kv')


from kivy.app import App
from kivy.metrics import dp
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen, RiseInTransition
from kivy.uix.behaviors import ButtonBehavior



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

class UserAdminCreateUserLayout(GridLayout):
    def __init__(self, **kwargs):
        super(UserAdminCreateUserLayout, self).__init__(**kwargs)
        self.db = Database()
        self.user_data = []
        self.cols = 1
        self.padding=(20,10)
        self.spacing = 40 
        self.minimum_height= 10
        self.height = (10, 10)

        self.title = Label(text="Create user", font_size=40, bold=True, color="#666AAD")
        self.add_widget(self.title)

        #input menu grid
        self.form_grid = GridLayout(cols=2, spacing=10, size_hint_y=5, row_default_height=40, row_force_default=True, pos_hint={"center_x": 0.5, "center_y": 0.5})

        self.form_grid.add_widget(Label(text="First Name", color="#878DFA", size_hint_x=None, width=100, text_size=self.size, valign="center", halign="left"))
        self.first_name_input = TextInput(multiline=False, write_tab=False)
        self.form_grid.add_widget(self.first_name_input)

        self.form_grid.add_widget(Label(text="Last Name", color="#878DFA", size_hint_x=None, width=100, text_size=self.size, valign="center", halign="left"))
        self.last_name_inupt = TextInput(multiline=False, write_tab=False)
        self.form_grid.add_widget(self.last_name_inupt)

        self.form_grid.add_widget(Label(text="EID", color="#878DFA", size_hint_x=None, width=100, text_size=self.size, valign="center", halign="left"))
        self.eid_input = TextInput(multiline=False, write_tab=False)
        self.form_grid.add_widget(self.eid_input)

        self.form_grid.add_widget(Label(text="Is admin", color="#878DFA", size_hint_x=None, width=100, text_size=self.size, valign="center", halign="left"))
        self.is_admin_input = TextInput(multiline=False, write_tab=False)
        self.form_grid.add_widget(self.is_admin_input)

        self.form_grid.add_widget(Label(text="Clock in time", color="#878dfa", size_hint_x=None, width=100, text_size=self.size, valign="center", halign="left"))
        self.clock_in_time_input = TextInput(multiline=False, write_tab=False)
        self.form_grid.add_widget(self.clock_in_time_input)

        self.form_grid.add_widget(Label(text="Clock out time", color="#878DFA", size_hint_x=None, width=100, text_size=self.size, valign="center", halign="left"))
        self.clock_out_time_input = TextInput(multiline=False, write_tab=False)
        self.form_grid.add_widget(self.clock_out_time_input)

        self.form_grid.add_widget(Label(text="Password", color="#878DFA", size_hint_x=None, width=100, text_size=self.size, valign="center", halign="left"))
        self.password_input = TextInput(multiline=False, write_tab=False)
        self.form_grid.add_widget(self.password_input)

        self.add_widget(self.form_grid)

        #bottom buttons
        self.bottom_grid = GridLayout(cols=3, spacing=10, row_default_height=30, row_force_default=True, pos_hint=(0.5,0.5))
        
        self.cancel_button = Button(text="Cancel", on_press=self.go_back,background_color = "#878DFA")
        self.save_button = Button(text="Save", on_press=self.save_new_data,background_color = "#878DFA")
        self.bottom_grid.add_widget(self.cancel_button)
        self.bottom_grid.add_widget(Label())
        self.bottom_grid.add_widget(self.save_button)

        self.add_widget(self.bottom_grid)

    def save_new_data(self, instance):
        self.user_data.append(self.first_name_input.text)
        self.user_data.append(self.last_name_inupt.text)
        self.user_data.append(self.eid_input.text)
        self.user_data.append(self.password_input.text)
        self.user_data.append(self.clock_in_time_input.text)
        self.user_data.append(self.clock_out_time_input.text)
        self.user_data.append(int(self.is_admin_input.text))
        self.db.create_user(self.user_data)

    def go_back(self, instance):
        app = App.get_running_app()
        app.root.current = "main_menu"

class UserAdminUpdateTimestampLayout(GridLayout):
    def __init__(self, **kwargs):
        super(UserAdminUpdateTimestampLayout, self).__init__(**kwargs)
        self.db = Database()
        self.timestamp_data = []
        self.updated_timestamp = {}
        self.user_data = []
        self.cols = 1
        self.padding=(20,10)
        self.spacing = 40 
        self.minimum_height= 10
        self.height = (10, 10)

        self.title = Label(text="Update Timestamp", font_size=40, size_hint_y=0.5, bold=True, color="#666AAD")
        self.add_widget(self.title)

        #search option at the top
        self.search_grid = GridLayout(cols=3, spacing=10, size_hint_y=None, row_default_height=30, row_force_default=True, pos_hint={"center_x": 0.5, "center_y": 0.5})
        self.search_grid.add_widget(Label(text="User EID", color="#878dfa", size_hint_x=None, width=100, text_size=self.size, valign="center", halign="left"))
        self.search_grid.add_widget(Label(text="Date", color="#878dfa", size_hint_x=None, width=100, text_size=self.size, valign="center", halign="left"))
        self.search_grid.add_widget(Label())

        self.search_eid = TextInput()
        self.search_date = TextInput()
        self.do_search = Button(text="Search", on_press=self.get_timestamp_data,background_color = "#878DFA")
        self.search_grid.add_widget(self.search_eid)
        self.search_grid.add_widget(self.search_date)
        self.search_grid.add_widget(self.do_search)

        self.add_widget(self.search_grid)

        #input menu grid
        self.form_grid = GridLayout(cols=2, spacing=10, size_hint_y=3, row_default_height=30, row_force_default=True,pos_hint={"center_x": 0.5, "center_y": 0.5})
        
        self.form_grid.add_widget(Label(text="User", color="#878dfa", size_hint_x=None, width=100, text_size=self.size, valign="center", halign="left"))
        self.user_name = TextInput(disabled=True)
        self.form_grid.add_widget(self.user_name)

        self.form_grid.add_widget(Label(text="Clock in", color="#878DFA", size_hint_x=None, width=100, text_size=self.size, valign="center", halign="left"))
        self.clock_in_input = TextInput()
        self.clock_in_input.id = "clock_in"
        self.clock_in_input.bind(text=self.update_new_data)
        self.form_grid.add_widget(self.clock_in_input)

        self.form_grid.add_widget(Label(text="Clock out", color="#878DFA", size_hint_x=None, width=100, text_size=self.size, valign="center", halign="left"))
        self.clock_out_input = TextInput()
        self.clock_out_input.id = "clock_out"
        self.clock_out_input.bind(text=self.update_new_data)
        self.form_grid.add_widget(self.clock_out_input)

        self.form_grid.add_widget(Label(text="Late", color="#878DFA", size_hint_x=None, width=100, text_size=self.size, valign="center", halign="left"))
        self.late_input = TextInput()
        self.late_input.id = "late"
        self.late_input.bind(text=self.update_new_data)
        self.form_grid.add_widget(self.late_input)

        self.form_grid.add_widget(Label(text="Too early", color="#878DFA", size_hint_x=None, width=100, text_size=self.size, valign="center", halign="left"))
        self.too_early_input = TextInput()
        self.too_early_input.id = "too_early"
        self.too_early_input.bind(text=self.update_new_data)
        self.form_grid.add_widget(self.too_early_input)

        self.form_grid.add_widget(Label(text="Exception", color="#878dfa", size_hint_x=None, width=100, text_size=self.size, valign="center", halign="left"))
        self.exception_input = TextInput()
        self.exception_input.id = "exception"
        self.exception_input.bind(text=self.update_new_data)
        self.form_grid.add_widget(self.exception_input)

        self.form_grid.add_widget(Label(text="Exception Description", color="#878DFA", size_hint_x=None, width=100, text_size=self.size, valign="center", halign="left"))
        self.exception_description_input = TextInput()
        self.exception_description_input.id = "exception_description"
        self.exception_description_input.bind(text=self.update_new_data)
        self.form_grid.add_widget(self.exception_description_input)

        self.add_widget(self.form_grid)

        #bottom buttons
        self.bottom_grid = GridLayout(cols=3, spacing=10, row_default_height=30, row_force_default=True, pos_hint=(0.5,0.5))
        
        self.cancel_button = Button(text="Cancel", on_press=self.go_back,background_color = "#878DFA")
        self.save_button = Button(text="Save", on_press=self.save_new_data,background_color = "#878DFA")
        self.bottom_grid.add_widget(self.cancel_button)
        self.bottom_grid.add_widget(Label())
        self.bottom_grid.add_widget(self.save_button)

        self.add_widget(self.bottom_grid)

    def get_timestamp_data(self, instance):
        self.user_data = self.db.get_user(self.search_eid.text)
        user_id = self.user_data[USER_INDEXES.ID]
        user_name = f"{self.user_data[USER_INDEXES.FIRST_NAME]} {self.user_data[USER_INDEXES.LAST_NAME]}"
        self.user_name.text = user_name
        if self.search_date.text != "":
            self.timestamp_data = self.db.get_timestamp(user_id, self.search_date.text)
        else:
            self.timestamp_data = self.db.get_timestamp(user_id)
        self.clock_in_input.text = self.timestamp_data[TIMESTAMP_INDEXES.CLOCK_IN]
        self.clock_out_input.text = self.timestamp_data[TIMESTAMP_INDEXES.CLOCK_OUT]
        self.late_input.text = str(self.timestamp_data[TIMESTAMP_INDEXES.LATE])
        self.too_early_input.text = str(self.timestamp_data[TIMESTAMP_INDEXES.TOO_EARLY])
        self.exception_input.text = str(self.timestamp_data[TIMESTAMP_INDEXES.EXCEPTION])
        self.exception_description_input.text = self.timestamp_data[TIMESTAMP_INDEXES.EXCEPTION_DESCRIPTION]
    
    def update_new_data(self, instance, value):
        if value == "":
            del self.updated_timestamp[instance.id]
        else:
            if instance.id == "late" or instance.id == "too_early" or instance.id == "exception":
                self.updated_timestamp[instance.id] = int(value)
            else:
                self.updated_timestamp[instance.id] = value
 
    def save_new_data(self, instance):
        user_id = self.user_data[USER_INDEXES.ID]
        date = self.timestamp_data[TIMESTAMP_INDEXES.DATE]
        if self.search_date == "":
            self.db.update_timestamp(user_id, self.updated_timestamp)
        else:
            self.db.update_timestamp(user_id, self.updated_timestamp, date)

    def go_back(self, instance):
        app = App.get_running_app()
        app.root.current = "main_menu"

class UserAdminUpdateUserLayout(GridLayout):
    def __init__(self, **kwargs):
        super(UserAdminUpdateUserLayout, self).__init__(**kwargs)
        self.db = Database()
        self.new_user_data = {}
        self.user_data = [] 
        self.cols = 1
        self.padding=(20,10)
        self.spacing = 40 
        self.minimum_height= 10
        self.height = (10, 10)

        self.title = Label(text="Update Timestamp", font_size=40, size_hint_y=0.5, bold=True, color="#666AAD")
        self.add_widget(self.title)

        #search option at the top
        self.search_grid = GridLayout(cols=2, spacing=10, size_hint_y=None, row_default_height=30, row_force_default=True, pos_hint={"center_x": 0.5, "center_y": 0.5})
        self.search_grid.add_widget(Label(text="User EID", color="#878dfa", size_hint_x=None, width=100, text_size=self.size, valign="center", halign="left"))
        #self.search_grid.add_widget(Label(text="Date", color="#878dfa", size_hint_x=None, width=100, text_size=self.size, valign="center", halign="left"))
        self.search_grid.add_widget(Label())

        self.search_eid = TextInput()
        self.search_date = TextInput()
        self.do_search = Button(text="Search", on_press=self.get_user_data,background_color = "#878DFA")
        self.search_grid.add_widget(self.search_eid)
        self.search_grid.add_widget(self.do_search)

        self.add_widget(self.search_grid)

        #input menu grid
        self.form_grid = GridLayout(cols=2, spacing=10, size_hint_y=3, row_default_height=30, row_force_default=True,pos_hint={"center_x": 0.5, "center_y": 0.5})

        self.form_grid.add_widget(Label(text="First Name", color="#878DFA", size_hint_x=None, width=100, text_size=self.size, valign="center", halign="left"))
        self.first_name_input = TextInput()
        self.first_name_input.id = "first_name"
        self.first_name_input.bind(text=self.update_new_data)
        self.form_grid.add_widget(self.first_name_input)

        self.form_grid.add_widget(Label(text="Last Name", color="#878DFA", size_hint_x=None, width=100, text_size=self.size, valign="center", halign="left"))
        self.last_name_inupt = TextInput()
        self.last_name_inupt.id = "last_name"
        self.last_name_inupt.bind(text=self.update_new_data)
        self.form_grid.add_widget(self.last_name_inupt)

        self.form_grid.add_widget(Label(text="EID", color="#878DFA", size_hint_x=None, width=100, text_size=self.size, valign="center", halign="left"))
        self.eid_input = TextInput()
        self.eid_input.id = "eid"
        self.eid_input.bind(text=self.update_new_data)
        self.form_grid.add_widget(self.eid_input)

        self.form_grid.add_widget(Label(text="Is admin", color="#878DFA", size_hint_x=None, width=100, text_size=self.size, valign="center", halign="left"))
        self.is_admin_input = TextInput()
        self.is_admin_input.id = "is_admin"
        self.is_admin_input.bind(text=self.update_new_data)
        self.form_grid.add_widget(self.is_admin_input)

        self.form_grid.add_widget(Label(text="Clock in time", color="#878dfa", size_hint_x=None, width=100, text_size=self.size, valign="center", halign="left"))
        self.clock_in_time_input = TextInput()
        self.clock_in_time_input.id = "clock_in_time"
        self.clock_in_time_input.bind(text=self.update_new_data)
        self.form_grid.add_widget(self.clock_in_time_input)

        self.form_grid.add_widget(Label(text="Clock out time", color="#878DFA", size_hint_x=None, width=100, text_size=self.size, valign="center", halign="left"))
        self.clock_out_time_input = TextInput()
        self.clock_out_time_input.id = "clock_out_time"
        self.clock_out_time_input.bind(text=self.update_new_data)
        self.form_grid.add_widget(self.clock_out_time_input)

        self.add_widget(self.form_grid)

        #bottom buttons
        self.bottom_grid = GridLayout(cols=3, spacing=10, row_default_height=30, row_force_default=True, pos_hint=(0.5,0.5))
        
        self.cancel_button = Button(text="Cancel", on_press=self.go_back,background_color = "#878DFA")
        self.save_button = Button(text="Save", on_press=self.save_new_data,background_color = "#878DFA")
        self.bottom_grid.add_widget(self.cancel_button)
        self.bottom_grid.add_widget(Label())
        self.bottom_grid.add_widget(self.save_button)

        self.add_widget(self.bottom_grid)

    def get_user_data(self, instance):
        self.user_data = self.db.get_user(self.search_eid.text)
        self.first_name_input.text = self.user_data[USER_INDEXES.FIRST_NAME]
        self.last_name_inupt.text = self.user_data[USER_INDEXES.LAST_NAME]
        self.eid_input.text = self.user_data[USER_INDEXES.EID]
        self.is_admin_input.text = str(self.user_data[USER_INDEXES.IS_ADMIN])
        self.clock_in_time_input.text = self.user_data[USER_INDEXES.CLOCK_IN_TIME]
        self.clock_out_time_input.text = self.user_data[USER_INDEXES.CLOCK_OUT_TIME]

    def update_new_data(self, instance, value):
        if value == "":
            del self.new_user_data[instance.id]
        else:
            self.new_user_data[instance.id] = value
 
    def save_new_data(self, instance):
        self.db.update_user(self.user_data[USER_INDEXES.ID],self.new_user_data)

    def go_back(self, instance):
        app = App.get_running_app()
        app.root.current = "main_menu"

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

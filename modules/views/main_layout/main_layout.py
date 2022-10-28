from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.app import App

class AdminMainLayout(GridLayout):
    def __init__(self, **kwargs):
        super(AdminMainLayout, self).__init__(**kwargs)
        self.user_data = []
        self.app = App.get_running_app()

    def go_create_user(self, instance):
        self.app.root.current = "create_user_menu"

    def go_update_user(self, instance):
        self.app.root.current = "update_user_menu"

    def go_update_timestamp(self, instance):
        self.app.root.current = "update_timestamp_menu"

    def go_self_timestamp(self, instance):
        self.app.root.get_screen("user").usermenugridlayout.set_user_data(self.user_data)
        self.app.root.current = "user"
        
    def go_save_report(self, instance):
        self.app.root.current = "save_report"

    def set_user_data(self, data):
        self.user_data = data

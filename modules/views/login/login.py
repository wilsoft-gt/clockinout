from modules.sqlite_handler import Database

from kivy.app import App

from modules.helpers import USER_INDEXES
from kivy.uix.gridlayout import GridLayout

class LoginGridLayout(GridLayout):
    def __init__(self, **kwargs):
        super(LoginGridLayout, self).__init__(**kwargs)
        self.db = Database()

    def login_db(self, value):
        cred = {
            "eid": self.children[2].children[2].text,
            "password": self.children[2].children[0].text
        }
        result = self.db.login(cred)

        if type(result) is dict and result["is_loged"] == True:
            is_admin=result["response"][USER_INDEXES.IS_ADMIN]
            print(result)
            app = App.get_running_app()
            if is_admin == 1:
                app.root.get_screen("main_menu").adminmainmenulayout.set_user_data(result["response"])
                app.root.current="main_menu"
            else:
                app.root.get_screen("user").usermenugridlayout.set_user_data(result["response"])
                app.root.current="user"
        
        else:
            self.children[2].children[0].text = ""
            self.children[2].children[2].text = ""
            self.children[3].text=str(result)

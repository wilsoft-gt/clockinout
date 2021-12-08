from .sqlite_handler import Database
import kivy
from kivy.app import App
from kivy.metrics import dp
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen, RiseInTransition

class MainGridLayout(GridLayout):
    def __init__(self, **kwargs):
        super(MainGridLayout, self).__init__(**kwargs)
        self.db = Database()
        #layout properties
        self.cols = 1
        self.size_hint = (0.6, 0.7)
        self.pos_hint = {"center_x": 0.5, "center_y": 0.5}
        self.spacing = 20
        #Widgets
        
        #top layout
        self.top_grid = GridLayout(
                cols=2,
                size_hint=(1,0.6),
                spacing=10
            )
        
        self.top_grid.add_widget(Label(
            text="EID:",
            font_size=18,
            size_hint_x=None,
            width=100,
            bold=True,
            color="#878DFA",
            text_size=self.size,
            halign="left",
            valign="middle"
        ))
        
        self.eid = TextInput(
                multiline=False,
                size_hint=(1,0.5)
            )
        self.top_grid.add_widget(self.eid)

        self.top_grid.add_widget(Label(
            text="Password:",
            font_size=18,
            size_hint_x=None,
            width=100,
            bold=True,
            color="#878DFA",
            text_size=self.size,
            halign="left",
            valign="middle"
        ))

        self.password = TextInput(
                multiline=False,
                password = True,
                size_hint=(1,0.5)
                )
        self.top_grid.add_widget(self.password)

        self.logo = Image(
                source="resources/logo.png",
                size_hint_y=None,
                height=200
                )
        self.add_widget(self.logo)

        self.add_widget(self.top_grid)

        self.login_button = Button(
                text="Login",
                size_hint=(1, 0.5),
                bold=True,
                background_color = "#878DFA"
        )
        self.login_button.bind(on_press=self.login_db) 
        self.add_widget(self.login_button)

        self.result = Label(
                size_hint=(1,0.3), 
                bold=True,
                color="#FF0000"
                )
        self.add_widget(self.result)

    def login_db(self, value):
        cred = {
            "eid": self.eid.text,
            "password": self.password.text
        }

        result = self.db.login(cred)
        print(type(result))

        if type(result) is dict and result["is_loged"] == True:
            self.result.text = ""
            self.eid.text = ""
            self.password.text = ""
            app = App.get_running_app()
            app.root.current="welcome"
        else:
            self.eid.text = ""
            self.password.text = ""
            self.result.text=str(result)

class WelcomeLayout(GridLayout):
    def __init__(self, **kwargs):
        super(WelcomeLayout, self).__init__(**kwargs)
        
        self.cols = 1

        self.label = Label(text="Hola", color="blue")
        self.add_widget(self.label)
        
        self.back = Button(text="Back")
        self.back.bind(on_press=self.go_back)
        self.add_widget(self.back)

    def go_back(self, value):
        app = App.get_running_app()
        app.root.current = "login"


class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.add_widget(MainGridLayout())

class WelcomeScreen(Screen):
    def __init__(self, **kwargs):
        super(WelcomeScreen, self).__init__(**kwargs)
        self.add_widget(WelcomeLayout())

class ClockInOutGui(App):
    def build(self):
        Window.clearcolor=(0.9,0.9,0.9,1)
        tr = RiseInTransition()
        sm = ScreenManager(transition=tr)
        sm.add_widget(LoginScreen(name="login"))
        sm.add_widget(WelcomeScreen(name="welcome"))
        sm.current = "login"
        return sm


if __name__ == '__main__':
    ClockInOutGui().run()

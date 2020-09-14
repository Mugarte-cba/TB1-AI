import kivy
kivy.require('1.0.7')

import csv
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen,ScreenManager
from kivy.properties import ObjectProperty
from database import DataBase
from kivy.uix.popup import Popup
from kivy.uix.label import Label

def invalidLogin():
    pop = Popup(title='Invalid Login',
                  content=Label(text='Invalid username or password.'),
                  size_hint=(None, None), size=(400, 400))
    pop.open()

class Home(GridLayout):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.Presentation=Presentation()
        self.Login=Login()

        self.add_widget(self.Presentation)
        self.add_widget(self.Login)

class Presentation(BoxLayout):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)

class Login(GridLayout):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)

    email = ObjectProperty(None)
    password = ObjectProperty(None)

    def loginBtn(self):
        if self.db.validate(self.email.text, self.password.text):
            myapp.current = self.email.text
            self.reset()
            myapp.screen_manager.current = "Distance"
        else:
            invalidLogin()

    db = DataBase("users.txt")

    def reset(self):
        self.email.text = ""
        self.password.text = ""

class Distance(GridLayout):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
    def logOut(self):
        myapp.screen_manager.current='Home'



class HillclimApp(App):
    title = 'Algoritmo Hill Climbing'
    def build(self):
        self.screen_manager=ScreenManager()

        self.home=Home()
        screenHome=Screen(name='Home')
        screenHome.add_widget(self.home)
        self.screen_manager.add_widget(screenHome)

        self.distance=Distance()
        screenDistance=Screen(name='Distance')
        screenDistance.add_widget(self.distance)
        self.screen_manager.add_widget(screenDistance)

        return self.screen_manager

if __name__=='__main__':
    myapp=HillclimApp()
    myapp.run()
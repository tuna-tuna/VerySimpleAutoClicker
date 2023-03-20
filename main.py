import pyautogui
from pynput import mouse

HotKey = mouse.Button.x2
isRunning = False
cps = 0.1
interval = 10.0

import kivy
from kivy.config import Config
Config.set('graphics', 'resizable', '0')
Config.set('graphics', 'width', '200')
Config.set('graphics', 'height', '300')

from kivy.app import App
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder

Builder.load_file('mainwindow.kv')
Builder.load_file('settings.kv')

class MainWindow(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.createListener()

    def onPress(self, x, y, button, pressed):
        if isRunning == True and button == HotKey:
            if pressed == True:
                pyautogui.PAUSE = interval
                Clock.schedule_interval(self.clickMouse, 0.0001)
            else:
                self.onRelease()

    def onRelease(self):
        Clock.unschedule(self.clickMouse)

    def createListener(self):
        listener = mouse.Listener(on_click=self.onPress)
        listener.start()

    def clickMouse(self, *args):
        pyautogui.click()

    def setRunning(self, toggle: bool):
        global isRunning
        isRunning = toggle

class Settings(Screen):
    def set_cps(self):
        global cps, interval
        try:
            cps = float(self.ids.cps.text)
        except ValueError:
            pass
        interval = 1.0 / cps
        print(f'cps set to {cps}, interval set to {interval}')

class MainApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainWindow(name='main'))
        sm.add_widget(Settings(name='settings'))
        return sm

if __name__ == '__main__':
    MainApp().run()


from kivy.config import Config

# Config.set('modules', 'touchring', '')
# Config.getint('kivy', 'show_fps')
# Config.set('graphics', 'maxfps', '30')
# Config.write()

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.graphics import Color, Ellipse, Triangle
from kivy.properties import ObjectProperty
from kivy.clock import Clock
import algorithms
import polygon
import random

COLORS  = [(0.925, 0, 0.543, 0.682),
           (0, 0.276, 0.769, 0.133),
           (0, 0.632, 0.792, 0.113),
           (0, 0.035, 0.129, 0.121),
           (0.924, 0.122, 0, 0.325)
          ]

Window.clearcolor = (1, 1, 1, 1)

class Application(Screen):
    def __init__(self, **args):
        super(Application, self).__init__(**args)

        self.points = set()
        self.structure = algorithms.Delanuay([(-4320., -4320.),(4320., 0.),(0., 4320.)])
        self.polygons = []
        self.tempPoly = None
        self.polygonFlag = False
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self, 'text')
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        print(keycode)
        if keycode[1] == 'escape':

            if self.polygonFlag:
                self.polygonFlag = False
                if self.tempPoly.doneAddingPoints():
                    self.polygons.append(self.tempPoly)
                self.updateScreen()
                self.tempPoly = None
            else:
                self.manager.transition.direction = 'right'
                self.manager.current = 'Theory'
        if keycode[1] == 'a':
            self.polygonFlag = True
            self.tempPoly = polygon.Polygon(1)

        return True

    def _keyboard_closed(self):
        print('My keyboard have been closed!')
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def on_touch_down(self, touch):
        if (touch.x, touch.y) not in self.points:
            self.draw_point(touch)
            self.updateScreen()

    def on_touch_move(self, touch):
        self.draw_point(touch)
        self.updateScreen()

    def on_touch_up(self, touch):
        pass

    def draw_point(self, touch):

        if self.polygonFlag:
            self.tempPoly.addPoint((touch.x, touch.y))

        self.structure.addPoint((touch.x,touch.y))
        self.points.add((touch.x, touch.y))

    def updateScreen(self):
        self.canvas.clear()
        self.clear_widgets()
        with self.canvas:
            i = 0
            for each in self.structure.triangulation:
                points = []
                for point in each.vertices:
                    for dim in point:
                        points.append(dim)
                # print(points)
                Color(rgba = each.color)
                i = (i+1)%len(COLORS)
                Triangle(points = points)

            Color(0,0,0)
            d = 3
            for each in self.polygons:
                self.canvas.add(each.line)

            Color(0., 0., 0.)
            for touch in self.points:
                Ellipse(pos=(touch[0] - d / 2, touch[1] - d / 2), size=(d, d))


class Theory(Screen):
    pass

class MainApp(App):

    def build(self):
        self.sc = ScreenManager()
        self.sc.add_widget(Theory(name = 'Theory'))
        self.sc.add_widget(Application(name = 'Application'))
        return self.sc

if __name__ == "__main__":
    MainApp().run()


from kivy.config import Config

# Config.set('modules', 'touchring', '')
# Config.getint('kivy', 'show_fps')
# Config.set('graphics', 'maxfps', '30')
# Config.write()

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.graphics import Color, Ellipse, Triangle
from kivy.clock import Clock
import algorithms
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
        super().__init__(**args)
        self.points = set()
        self.structure = algorithms.Delanuay([(-4320., -4320.),(4320., 0.),(0., 4320.)])
        # Clock.schedule_interval(self.updateScreen, 0.2)


    def on_touch_down(self, touch):
        if (touch.x, touch.y) not in self.points:
            print(len(self.points))
            self.draw_point(touch)
            self.updateScreen()

    def on_touch_move(self, touch):
        self.draw_point(touch)
        self.updateScreen()

    def on_touch_up(self, touch):
        pass

    def draw_point(self, touch):
        self.points.add((touch.x,touch.y))
        self.structure.addPoint((touch.x,touch.y))

    def updateScreen(self):
        self.canvas.clear()
        with self.canvas:
            i = 0
            for each in self.structure.triangulation:
                points = []
                for point in each.vertices:
                    for dim in point:
                        points.append(dim)
                # print(points)
                Color(rgb = each.color)
                i = (i+1)%len(COLORS)
                Triangle(points = points)

            Color(0., 0., 0.)
            d = 3
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

MainApp().run()

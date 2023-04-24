from kivy.app import App
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.vector import Vector

class Basak(Image):
    def __init__(self, **kwargs):
        super(Basak, self).__init__(**kwargs)
        self.velocity = Vector(0, 0)
        self.key_pressed = set()
        self.size_hint = (None, None)
        self.allow_stretch = True
        self.keep_ratio = False
  
  
        self.source = 'basak.png'

    def keyboard_on_key_down(self, window, key, code, text, modifiers):
        if key == 276:
            self.velocity.x = -5
        elif key == 275:
            self.velocity.x = 5
        elif key == 273:
            self.velocity.y = 5
        elif key == 274:
            self.velocity.y = -5
    def keyboard_on_key_up(self, window, key, *args):
        if key == 276 or key == 275:
            self.velocity.x = 0
        elif key == 273 or key == 274:
            self.velocity.y = 0

    def update(self, dt):
        self.pos = Vector(*self.velocity) + self.pos

class Myapp(App):
    def build(self):
        image = MyImage()
        Clock.schedule_interval(image.update, 1.0 / 60.0)
        Window.bind(on_key_down=image.keyboard_on_key_down)
        Window.bind(on_key_up=image.keyboard_on_key_up)
        return image
if __name__ == '__main__':
    Basak().run()

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout


from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.vector import Vector
from kivy.uix.screenmanager import ScreenManager, Screen


class Character(Image):
    def __init__(self, **kwargs):
        super(Character, self).__init__(**kwargs)
        self.velocity = Vector(0, 0)
        self.key_pressed = set()
        self.size_hint = (None, None)
        self.allow_stretch = True
        self.keep_ratio = False
        self.source = 'basak.png'
        self.size = (300, 300)
        self.is_jumping = False
        self.jump_velocity = Vector(0, 0)
        self.jump_height = 100
        self.floor_height = 200
        self.screen_width = Window.width
        self.screen_height = Window.height
        self.pos= 0,200

    def keyboard_on_key_down(self, window, key, code, text, modifiers):
        if key == 276:
            self.velocity.x = -5
            
        elif key == 275:
            self.velocity.x = 5
           
        elif key == 273 and not self.is_jumping:
            self.is_jumping = True
            self.jump_velocity.y = 10

    def keyboard_on_key_up(self, window, key, *args):
        if key == 276 or key == 275:
            self.velocity.x = 0

    def update(self, dt):
        self.screen_width = Window.width
        self.screen_height = Window.height
        if self.is_jumping:
            self.jump_velocity.y -= 1
            self.pos = Vector(*self.jump_velocity) + self.pos
            if self.pos[1] <= self.floor_height:
                self.pos[1] = self.floor_height
                self.is_jumping = False
                self.jump_velocity.y = 0
        else:
            self.pos = Vector(*self.velocity) + self.pos

            # Check boundaries
            if self.pos[0] < 0:
                self.pos[0] = 0
            elif self.pos[0] + self.width > self.screen_width:
                self.pos[0] = self.screen_width - self.width
            if self.pos[1] < 0:
                self.pos[1] = 0
            elif self.pos[1] + self.height > self.screen_height:
                self.pos[1] = self.screen_height - self.height


class StartScreen(Screen):
    def __init__(self, **kwargs):
        super(StartScreen, self).__init__(**kwargs)
        
      
        # Resmi yükleyin
        self.background = Image(source=('background.jpg'))
        # Resmi ekranınıza ekleyin
        self.add_widget(self.background)
        image = Character()
        Clock.schedule_interval(image.update, 1.0 / 60.0)
        Window.bind(on_key_down=image.keyboard_on_key_down)
        Window.bind(on_key_up=image.keyboard_on_key_up)
        self.add_widget(image)

class Rewind(App):
    def build(self):

        Builder.load_file("rewind.kv")
        sm = ScreenManager()

        sm.add_widget(StartScreen(name='start'))

        return sm

if __name__ == '__main__':
    Rewind().run()

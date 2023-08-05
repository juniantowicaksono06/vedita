import os, sys
import base64
import requests
if sys.version_info[0] == 2:
    import Tkinter
    tkinter = Tkinter
else:
    import tkinter
from PIL import Image, ImageTk

def get_base_path():
    return os.path.dirname(os.path.abspath(sys.argv[0]))

def convert_b64_to_file(filename, b64_data):
    try:
        b64_data = base64.b64decode(b64_data)
        with open(filename, 'wb') as file:
            file.write(b64_data)
    except Exception as e:
        print(f"Error {e}")
        return False
    return True

def make_request(url: str, method: str, animate_motor=True, payload=None, files=None, headers=None, proxies=None, verify=False):
    req: requests = None
    if method == 'GET':
        req: requests = requests.get(url, data=payload, files=files, headers=headers, proxies=proxies, verify=verify)
    elif method == "POST":
        req: requests = requests.post(url, data=payload, files=files, headers=headers, proxies=proxies, verify=verify)
    return req

def show_image_full_screen(path):
    pilImage = Image.open(path)
    root = tkinter.Tk()
    w, h = root.winfo_screenwidth(), root.winfo_screenheight()
    root.overrideredirect(1)
    root.geometry("%dx%d+0+0" % (w, h))
    root.focus_set()    
    root.bind("<Escape>", lambda e: (e.widget.withdraw(), e.widget.quit()))
    canvas = tkinter.Canvas(root,width=w,height=h)
    canvas.pack()
    canvas.configure(background='black')
    imgWidth, imgHeight = pilImage.size
    if imgWidth > w or imgHeight > h:
        ratio = min(w/imgWidth, h/imgHeight)
        imgWidth = int(imgWidth*ratio)
        imgHeight = int(imgHeight*ratio)
        pilImage = pilImage.resize((imgWidth,imgHeight), Image.ANTIALIAS)
    image = ImageTk.PhotoImage(pilImage)
    imagesprite = canvas.create_image(w/2,h/2,image=image)
    root.mainloop()
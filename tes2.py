import sys
if sys.version_info[0] == 2:
    import Tkinter
    tkinter = Tkinter
else:
    import tkinter
from PIL import Image, ImageTk
import threading


# def showPIL(pilImage):
#     root = tkinter.Tk()
#     w, h = root.winfo_screenwidth(), root.winfo_screenheight()
#     root.overrideredirect(1)
#     root.geometry("%dx%d+0+0" % (w, h))
#     root.focus_set()    
#     root.bind("<Escape>", lambda e: (e.widget.withdraw(), e.widget.quit()))
#     canvas = tkinter.Canvas(root,width=w,height=h)
#     canvas.pack()
#     canvas.configure(background='black')
#     imgWidth, imgHeight = pilImage.size
#     if imgWidth > w or imgHeight > h:
#         ratio = min(w/imgWidth, h/imgHeight)
#         imgWidth = int(imgWidth*ratio)
#         imgHeight = int(imgHeight*ratio)
#         pilImage = pilImage.resize((imgWidth,imgHeight), Image.ANTIALIAS)
#     image = ImageTk.PhotoImage(pilImage)
#     imagesprite = canvas.create_image(w/2,h/2,image=image)
#     root.mainloop()

# pilImage = Image.open("./output_faq.jpg")
# print("WOKE")
# background_thread = threading.Thread(target=showPIL, args=(pilImage, ))
# background_thread.start()

# print("TES")

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


background_thread = threading.Thread(target=show_image_full_screen, args=("./output_faq.jpg", ))

background_thread.start()
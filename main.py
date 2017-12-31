import glob
import os
import sys
if sys.version_info[0] == 2:  # the tkinter library changed it's name from Python 2 to 3.
    import Tkinter
    tkinter = Tkinter #I decided to use a library reference to avoid potential naming conflicts with people's programs.
else:
    import tkinter
from PIL import Image, ImageTk
import time
import shutil

NEW_DIR = 'tmp/new'
ARCHIVE_DIR = 'tmp/archive'

def showPIL(pilImage):
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
        ratio = min(float(w)/imgWidth, float(h)/imgHeight)
        imgWidth = int(imgWidth*ratio)
        imgHeight = int(imgHeight*ratio)
        pilImage = pilImage.resize((imgWidth,imgHeight), Image.ANTIALIAS)
    image = ImageTk.PhotoImage(pilImage)
    imagesprite = canvas.create_image(w/2,h/2,image=image)
    root.after(5000, root.destroy)
    root.mainloop()

def main():
    # Load things
    new_queue = glob.glob(os.path.join(NEW_DIR, "*"))
    archive_queue = glob.glob(os.path.join(ARCHIVE_DIR, "*"))
    if (len(new_queue) + len(archive_queue)) == 0:
        print "Everything empty"
        return

    while True:
        new_files = glob.glob(os.path.join(NEW_DIR, "*"))
        new_queue = new_queue + new_files

        if len(new_queue) != 0:
            curr_file = new_queue[0]
            new_queue = new_queue[1:]
            new_path = os.path.join(ARCHIVE_DIR, curr_file.split('/')[-1])
            archive_queue = archive_queue + [new_path]
        else:
            curr_file = archive_queue[0]
            archive_queue = archive_queue[1:]
            archive_queue = archive_queue + [curr_file]

        image = Image.open(curr_file)
        shutil.move(curr_file, os.path.join(ARCHIVE_DIR, curr_file.split('/')[-1]))
        showPIL(image)


if __name__ == '__main__':
    main()

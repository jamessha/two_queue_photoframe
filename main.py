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

class PhotoFrame():
    def __init__(self):
        self.new_queue = glob.glob(os.path.join(NEW_DIR, "*"))
        self.archive_queue = glob.glob(os.path.join(ARCHIVE_DIR, "*"))
        if (len(self.new_queue) + len(self.archive_queue)) == 0:
            print "Everything empty"
            return

        self.root = tkinter.Tk()
        self.w, self.h = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        self.root.overrideredirect(1)
        self.root.geometry("%dx%d+0+0" % (self.w, self.h))
        self.root.focus_set()
        self.root.bind("<Escape>", lambda e: (e.widget.withdraw(), e.widget.quit()))
        self.canvas = tkinter.Canvas(self.root, width=self.w, height=self.h)
        self.canvas.pack()
        self.canvas.configure(background='black')
        pilImage = Image.new('RGB', (1400, 900))
        image = ImageTk.PhotoImage(pilImage)
        self.imagesprite = self.canvas.create_image(self.w/2, self.h/2, image=image)

        self.root.after(1000, self.loadNextImage)
        self.root.mainloop()


    def loadNextImage(self):
        new_files = glob.glob(os.path.join(NEW_DIR, "*"))
        self.new_queue = self.new_queue + new_files

        if len(self.new_queue) != 0:
            curr_file = self.new_queue[0]
            self.new_queue = self.new_queue[1:]
            new_path = os.path.join(ARCHIVE_DIR, curr_file.split('/')[-1])
            shutil.move(curr_file, new_path)
            curr_file = new_path
            self.archive_queue = self.archive_queue + [new_path]
        else:
            curr_file = self.archive_queue[0]
            self.archive_queue = self.archive_queue[1:]
            self.archive_queue = self.archive_queue + [curr_file]

        self.pilImage = Image.open(curr_file)
        self.showPIL()


    def showPIL(self):
        imgWidth, imgHeight = self.pilImage.size
        if imgWidth > self.w or imgHeight > self.h:
            ratio = min(float(self.w)/imgWidth, float(self.h)/imgHeight)
            imgWidth = int(imgWidth*ratio)
            imgHeight = int(imgHeight*ratio)
            self.pilImage = self.pilImage.resize((imgWidth, imgHeight), Image.ANTIALIAS)
        self.image = ImageTk.PhotoImage(self.pilImage)
        self.canvas.itemconfigure(self.imagesprite, image=self.image)
        self.root.update()
        time.sleep(5)
        self.loadNextImage()


def main():
    # Load things
    photoframe = PhotoFrame()


if __name__ == '__main__':
    main()

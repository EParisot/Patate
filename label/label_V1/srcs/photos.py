import os
import time
import srcs.color as c
from tkinter import *
from PIL import ImageTk, Image

class Photos(object):
    def __init__(self, photos, lab_photos, trash='trash/', auto_next=False, width=800, height=600):
        self.photos_dir = photos
        self.lab_photos_dir = lab_photos
        self.trash_dir = trash
        self.photo_act = 0
        self.fen = {
            'fen' : None,
            'lab_photo' : None,
            'photo' : None,
            'lab_info' : None
        }
        self.width = width
        self.height = height
        self.width_img = self.width
        self.height_img = self.height - 50
        self.auto_next = auto_next

    def load(self):
        self.photos = os.listdir(self.photos_dir)
        self.photos_inf = [{'del' : False, 'label' : ''} for i in range(len(self.photos))]
        self.photo_act = 0

    def init_win(self, width=0, height=0):
        self.width = width if width != 0 else self.width
        self.width_img = width if width != 0 else self.width_img
        self.height_img = height - 50 if height != 0 else self.height_img
        self.fen['fen'] = Tk()
        self.fen['fen'].title('lab_photo')
        self.print_win()
        self.init_key()
        self.fen['fen'].mainloop()

    def init_key(self):
        self.fen['fen'].bind("<Escape>", self.quit_win)
        self.fen['fen'].bind("<BackSpace>", self.del_label)
        self.fen['fen'].bind("<Control-Key-s>", self.save)
        self.fen['fen'].bind("<Right>", self.next_photo)
        self.fen['fen'].bind("<Left>", self.last_photo)
        self.fen['fen'].bind("<Up>", self.del_photo)
        self.fen['fen'].bind("<KeyPress>", self.event_win)

    def save(self, event):
        for i in range(len(self.photos)):
            if self.photos_inf[i]['del'] == True:
                print(c.RED + 'DELETE -> ' + c.EOC + self.photos[i])
                os.rename(self.photos_dir + self.photos[i], self.trash_dir + self.photos[i])
            if self.photos_inf[i]['label'] != '':
                print(c.GREEN + 'LABEL -> ' + c.EOC + self.photos_inf[i]['label'] + '_' + self.photos[i])
                os.rename(self.photos_dir + self.photos[i], self.lab_photos_dir + self.photos_inf[i]['label'] + '_' + self.photos[i])
        self.load()

    def quit_win(self, event):
        self.save(None)
        self.fen['fen'].destroy()
        self.fen['fen'].quit()

    def del_label(self, event):
        self.photos_inf[self.photo_act]['label'] = ''
        if self.auto_next == True:
            self.next_photo(None)
        else:
            self.print_win()

    def event_win(self, event):
        if event.char in ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9'):
            self.photos_inf[self.photo_act]['label'] = event.char
            if self.auto_next == True:
                self.next_photo(None)
            else:
                self.print_win()

    def del_photo(self, event):
        if self.photos_inf[self.photo_act]['del'] == True:
            self.photos_inf[self.photo_act]['del'] = False
        else:
            self.photos_inf[self.photo_act]['del'] = True
        if self.auto_next == True:
            self.next_photo(None)
        else:
            self.print_win()

    def last_photo(self, event):
        self.photo_act -= 1
        if self.photo_act < 0:
            self.photo_act = len(self.photos) - 1
        self.print_win()

    def next_photo(self, event):
        self.photo_act += 1
        if self.photo_act >= len(self.photos):
            self.photo_act = 0
        self.print_win()

    def print_win(self):
        if self.fen['lab_photo'] != None:
            self.fen['lab_photo'].destroy()
        if self.fen['lab_info'] != None:
            self.fen['lab_info'].destroy()
        image = Image.open(self.photos_dir + self.photos[self.photo_act])
        image = image.resize((self.width_img, self.height_img), Image.ANTIALIAS)
        self.fen['photo'] = ImageTk.PhotoImage(image)
        self.fen['lab_photo'] = Label(self.fen['fen'], image=self.fen['photo'])
        self.fen['lab_photo'].pack(side=TOP)
        self.fen['lab_info'] = Label(self.fen['fen'], width=32, height=2, font=("Courier", 40))
        if self.photos_inf[self.photo_act]['del'] == True:
            self.fen['lab_info'].configure(bg='red')
        else:
            self.fen['lab_info'].configure(bg='white')
        self.fen['lab_info']['text'] = self.photos_inf[self.photo_act]['label'] + '\t\t' + str(self.photo_act) + '/' + str(len(self.photos))
        self.fen['lab_info'].pack(side=BOTTOM)

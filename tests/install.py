import zipfile
from tkinter import *
import tkinter.ttk as ttk
import time, threading, pip._internal
import urllib.request

TITLE = 'Project installator'
SUBHEADER = 'For Python project "pymunk-game"\nSource code: https://github.com/100ants/pymunk-game'
URL = 'http://212.118.51.104:10105/python/file.zip'
START = 'main.py'

root = Tk()
root.title(TITLE)
root.geometry('600x400')

pb = None


pgerr = None
pmerr = None

var1 = IntVar()

def postinstall():
    subheader.config(text='Succesfully installed project')
    header.config(text='Finish!')
    pb.destroy()

    okbtn = Button(root,
                   text='Finish installation',
                   bg='#68a6de',
                   activebackground='#4479c3',
                   activeforeground='white',
                   fg='white',
                   font='arial 10',
                   bd=0,
                   padx=20,
                   pady=5,
                   width=10,
                   command=end
                   )
    okbtn.place(x=300, y=300, anchor='center')
    cancellbtn.destroy()

def unpack():
    subheader.config(text='Unpacking...')
    pb['value'] = 0
    zip = zipfile.ZipFile('./file.zip')
    zip.extractall()
    pb['value'] = 100
    postinstall()

def download():
    subheader.config(text='Downloading packages...')
    pb['value'] = 0
    urllib.request.urlretrieve(URL, './file.zip')
    pb['value'] = 100
    unpack()


def install():
    pb = ttk.Progressbar(root, length=300, mode="determinate")
    pb.place(x=300, y=120, anchor='center')
    if not pg:
        pgerr.destroy()
    if not pm:
        pmerr.destroy()
    okbtn.destroy()

    subheader.config(text='Installing')
    l = 100 / (int(not pg) + int(not pm))
    if not pg:
        pip._internal.main(["install", "--user", "pygame"])
    pb['value'] += l
    if not pm:
        pip._internal.main(["install", "--user", "pymunk"])
    pb['value'] += l
    time.sleep(.3)
    download()

def req():
    global pmerr, pgerr, okbtn, pg, pm
    pg = False
    try:
        import pygame
        del pygame
        pg = True
    except ImportError:
        pg = False

    if pg: pb['value'] += 50

    pm = False
    try:
        import pymunk
        del pymunk
        pm = True
    except ImportError:
        pm = False

    if pm: pb['value'] += 50

    print(pg, pm)

    if pg and pm:
        time.sleep(.3)
        download()
    else:
        time.sleep(.3)
        subheader.config(text='Found some missing libraries')
        pb.destroy()

        if not pg:
            pgerr = Label(root, text='Pygame not found', fg='#f76b47', font='arial 10')
            pgerr.place(x=300, y=150, anchor='center')

        if not pm:
            pmerr = Label(root, text='Pymunk not found', fg='#f76b47', font='arial 10')
            print(pm, pmerr)
            if not pg:
                pmerr.place(x=300, y=170, anchor='center')
            else:
                pmerr.place(x=300, y=150, anchor='center')

        okbtn = Button(root,
                       text='Install missing',
                       bg='#68a6de',
                       activebackground='#4479c3',
                       activeforeground='white',
                       fg='white',
                       font='arial 10',
                       bd=0,
                       padx=20,
                       pady=5,
                       width=10,
                       command=install
                       )

        okbtn.place(x=300, y=220, anchor='center')






def check_req():
    global pb
    header.config(text='In progress')
    subheader.config(text='Checking requirements...')
    okbtn.destroy()
    cancellbtn.place(x=300, y=300, anchor='center')
    pb = ttk.Progressbar(root, length=300, mode="determinate")
    pb.place(x=300, y=120, anchor='center')

    threading.Thread(target=req).start()


header = Label(root, text=TITLE, font='arial 14')
header.place(x=300, y=50, anchor='center')

subheader = Label(root, text=SUBHEADER, fg='gray', font='arial 10')
subheader.place(x=300, y=80, anchor='center')

okbtn = Button(root,
                   text='Install project',
                   bg='#68a6de',
                   activebackground='#4479c3',
                   activeforeground='white',
                   fg='white',
                   font='arial 10',
                   bd=0,
                   padx=20,
                   pady=5,
                   width=10,
                   command=check_req
)
okbtn.place(x=300, y=150, anchor='center')

cancellbtn = Button(root,
                   text='Cancell',
                   bg='lightgray',
                   activebackground='gray',
                   activeforeground='white',
                   fg='white',
                   font='arial 10',
                   bd=0,
                   padx=20,
                   pady=5,
                   width=10,
                   command=lambda: exit(-1)
)
cancellbtn.place(x=300, y=190, anchor='center')

copy = Label(root, text='Made by © Ivan_SD, 2019', fg='gray', font='arial 10')
copy.place(x=300, y=370, anchor='center')


root.mainloop()

exit()

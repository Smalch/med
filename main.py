from tkinter import *
import time
import sqlite3
import random
import tempfile
import win32api
import win32print

f = ''
flag = ''
flags = ''

login = sqlite3.connect("admin.db")
l = login.cursor()

c = sqlite3.connect("assortiment.db")
cur = c.cursor()

def add_tables():
    # Create table
    cur.execute("CREATE TABLE assortiment (id integer, name text, amount integer, price real, description text)")
    cur.execute("CREATE TABLE history (id integer, name text, amount integer, price real, date text)")

    # Save (commit) the changes
    c.commit()
    c.close()

def add_system():
    # Create table
    l.execute("CREATE TABLE logs (login text, password text)")

    # Insert a row of data
    l.execute("INSERT INTO logs VALUES ('admin','admin')")
    l.execute("INSERT INTO logs VALUES ('user','user')")
    # Save (commit) the changes
    login.commit()
    login.close()





def again():
    global un, pwd, flag, root, apt
    if flag == 'apt':
        apt.destroy()
    root = Tk()
    root.geometry('300x150')
    root.title('Management System')
    Label(root, text='Management System').grid(row=0, column=0, columnspan=5)
    Label(root, text="Artem Sklyar").grid(row=1, column=0, columnspan=5)
    Label(root, text='-------------------------------------------------------').grid(row=2, column=0, columnspan=5)
    Label(root, text='Username').grid(row=3, column=0)
    un = Entry(root, width=30)
    un.grid(row=3, column=1)
    Label(root, text='Password').grid(row=4, column=0)
    pwd = Entry(root, width=30)
    pwd.grid(row=4, column=1)
    Button(root, width=6, bg='blue', fg='white', text='Enter', command=check).grid(row=5, column=0)
    Button(root, width=6, bg='red', fg='white', text='Close', command=root.destroy).grid(row=5, column=1)
    root.mainloop()


def check():
    global un, pwd, login, l, root
    u = un.get()
    p = pwd.get()
    l.execute("select * from logs")
    for i in l:
        if i[0] == u and i[1] == p and u == 'admin':
            root.destroy()
            print("admin")
            #open_win()
        elif i[0] == u and i[1] == p:
            root.destroy()
            print("user")
            #open_cus()
    login.commit()


again()
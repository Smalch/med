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

columns = ('id', 'name', 'amount', 'price', 'description')


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


def main_window():
    global apt, flag
    flag = 'apt'
    apt = Tk()
    apt.title("Main Menu")
    Label(apt, text="STORE MANAGEMENT SYSTEM").grid(row=0, column=0, columnspan=3)
    Label(apt, text='*' * 80).grid(row=1, column=0, columnspan=3)
    Label(apt, text='-' * 80).grid(row=3, column=0, columnspan=3)

    Label(apt, text="Stock Maintenance", bg='green', fg='white').grid(row=2, column=0)
    # Button(apt, text='New V.C.', width=25, bg='green', fg='white', command=val_cus).grid(row=4, column=0)
    Button(apt, text='Add product to Stock', bg='green', fg='white', width=25, command=NewStock).grid(row=5, column=0)
    Button(apt, text='Delete product from Stock', bg='red', fg='white', width=25, command=delete_stock).grid(row=6, column=0)

    Label(apt, text="Access Database", bg='blue', fg='white').grid(row=2, column=1)
    # Button(apt, text='Modify', width=15, bg='blue', fg='white', command=modify).grid(row=4, column=1)
    # Button(apt, text='Search', width=15, bg='blue', fg='white', command=search).grid(row=5, column=1)
    # Button(apt, text='Expiry Check', bg='red', fg='white', width=15, command=exp_date).grid(row=6, column=1)

    Label(apt, text="Handle Cash Flows", bg='skyblue', fg='black').grid(row=2, column=2)
    # Button(apt, text="Check Today's Revenue", bg='skyblue', fg='black', width=20, command=show_rev).grid(row=5, column=2)
    # Button(apt, text='Billing', width=20, bg='skyblue', fg='black', command=billing).grid(row=4, column=2)
    Button(apt, text='Logout', bg='red', fg='white', width=20, command=again).grid(row=6, column=2)
    apt.mainloop()


def NewStock():
    global cur, c, columns, accept, flag, sto, apt
    apt.destroy()
    flag = 'sto'
    accept = [''] * 10
    sto = Tk()
    sto.title('ADD NEW STOCK')
    Label(sto, text='ENTER NEW PRODUCT DATA TO THE STOCK').grid(row=0, column=0, columnspan=2)
    Label(sto, text='-' * 50).grid(row=1, column=0, columnspan=2)
    for i in range(1, len(columns)):
        Label(sto, width=15, text=' ' * (14 - len(str(columns[i]))) + str(columns[i]) + ':').grid(row=i + 2, column=0)
        accept[i] = Entry(sto)
        accept[i].grid(row=i + 2, column=1)
    Button(sto, width=15, text='Submit', bg='blue', fg='white', command=submit).grid(row=12, column=1)
    Label(sto, text='-' * 165).grid(row=13, column=0, columnspan=7)
    # Button(sto, width=15, text='Reset', bg='red', fg='white', command=reset).grid(row=12, column=0)
    Button(sto, width=15, text='Refresh stock', bg='skyblue', fg='black', command=refresh).grid(row=12, column=4)
    for i in range(1, 5):
        Label(sto, text=columns[i]).grid(row=14, column=i - 1)
    Label(sto, text='Exp           Rack   Manufacturer                      ').grid(row=14, column=5)
    Button(sto, width=10, text='Main Menu', bg='green', fg='white', command=main_menu).grid(row=12, column=5)
    refresh()
    sto.mainloop()


def submit():
    global accept, c, cur, columns, sto
    y=0
    x = [''] * 5
    cur.execute("select * from assortiment")
    for i in cur:
        y = int(i[0])
    for i in range(1, 5):
        x[i] = accept[i].get()
    sql = "insert into assortiment values('%s','%s','%s','%s','%s')" % (y + 1, x[1], x[2], x[3], x[4])
    cur.execute(sql)
    cur.execute("select * from assortiment")
    c.commit()

    top = Tk()
    Label(top, width=20, text='Success!').pack()
    top.mainloop()
    main_menu()

def refresh():
    global sto, c, cur

    def onvsb(*args):
        lb1.yview(*args)
        lb2.yview(*args)
        lb3.yview(*args)
        lb4.yview(*args)
        lb5.yview(*args)
        lb6.yview(*args)

    def onmousewheel():
        lb1.ywiew = ('scroll', event.delta, 'units')
        lb2.ywiew = ('scroll', event.delta, 'units')
        lb3.ywiew = ('scroll', event.delta, 'units')
        lb4.ywiew = ('scroll', event.delta, 'units')
        lb5.ywiew = ('scroll', event.delta, 'units')
        lb6.ywiew = ('scroll', event.delta, 'units')

        return 'break'

    cx = 0
    vsb = Scrollbar(orient='vertical', command=onvsb)
    lb1 = Listbox(sto, yscrollcommand=vsb.set)
    lb2 = Listbox(sto, yscrollcommand=vsb.set)
    lb3 = Listbox(sto, yscrollcommand=vsb.set, width=10)
    lb4 = Listbox(sto, yscrollcommand=vsb.set, width=7)
    lb5 = Listbox(sto, yscrollcommand=vsb.set, width=25)
    lb6 = Listbox(sto, yscrollcommand=vsb.set, width=37)
    vsb.grid(row=15, column=6, sticky=N + S)
    lb1.grid(row=15, column=0)
    lb2.grid(row=15, column=1)
    lb3.grid(row=15, column=2)
    lb4.grid(row=15, column=3)
    lb5.grid(row=15, column=4)
    lb6.grid(row=15, column=5)
    lb1.bind('<MouseWheel>', onmousewheel)
    lb2.bind('<MouseWheel>', onmousewheel)
    lb3.bind('<MouseWheel>', onmousewheel)
    lb4.bind('<MouseWheel>', onmousewheel)
    lb5.bind('<MouseWheel>', onmousewheel)
    lb6.bind('<MouseWheel>', onmousewheel)
    cur.execute("select * from assortiment")
    for i in cur:
        cx += 1
        seq = (str(i[0]), str(i[1]))
        lb1.insert(cx, '. '.join(seq))
        lb2.insert(cx, i[2])
        lb3.insert(cx, i[3])
        lb4.insert(cx, i[4])
        lb5.insert(cx, i[5])
        lb6.insert(cx, i[6] + '    ' + i[7] + '    ' + i[8])
    c.commit()

def ren():
    global lb1, d, cur, c

    def onvsb(*args):
        lb1.yview(*args)
        lb2.yview(*args)

    def onmousewheel():
        lb1.ywiew = ('scroll', event.delta, 'units')
        lb2.ywiew = ('scroll', event.delta, 'units')
        return 'break'

    cx = 0
    vsb = Scrollbar(orient='vertical', command=onvsb)
    lb1 = Listbox(d, width=25, yscrollcommand=vsb.set)
    lb2 = Listbox(d, width=30, yscrollcommand=vsb.set)
    vsb.grid(row=3, column=2, sticky=N + S)
    lb1.grid(row=3, column=0)
    lb2.grid(row=3, column=1)
    lb1.bind('<MouseWheel>', onmousewheel)
    lb2.bind('<MouseWheel>', onmousewheel)
    cur.execute("select * from assortiment")
    for i in cur:
        cx += 1
        s1 = [str(i[0]), str(i[1])]
        s2 = [str(i[3]), str(i[4])]
        lb1.insert(cx, '. '.join(s1))
        lb2.insert(cx, '   '.join(s2))
    c.commit()
    lb1.bind('<<ListboxSelect>>', sel_del)


def sel_del(e):
    global lb1, d, cur, c, p, sl2
    p = lb1.curselection()
    print(p)
    x = 0
    sl2 = ''
    cur.execute("select * from assortiment")
    for i in cur:
        print(x, p[0])
        if x == int(p[0]):
            sl2 = i[0]
            break
        x += 1
    c.commit()
    print(sl2)
    Label(d, text=' ', bg='white', width=20).grid(row=0, column=1)
    cur.execute('Select * from assortiment')
    for i in cur:
        if i[0] == sl2:
            Label(d, text=i[0] + '. ' + i[1], bg='white').grid(row=0, column=1)
    c.commit()

def delete_stock():
    global cur, c, flag, lb1, d
    apt.destroy()
    flag = 'd'
    d = Tk()
    d.title("Delete a product from Stock")
    Label(d, text='Enter Product to delete:').grid(row=0, column=0)
    Label(d, text='', width=30, bg='white').grid(row=0, column=1)
    Label(d, text='Product').grid(row=2, column=0)
    Label(d, text='Qty.  Exp.dt.     Cost                           ').grid(row=2, column=1)
    ren()
    b = Button(d, width=20, text='Delete', bg='red', fg='white', command=delt).grid(row=0, column=3)
    b = Button(d, width=20, text='Main Menu', bg='green', fg='white', command=main_menu).grid(row=5, column=3)
    d.mainloop()

def delt():
    global p, c, cur, d
    cur.execute("delete from assortiment where id=?", (sl2,))
    c.commit()
    ren()

def main_menu():
    global sto, apt, flag, root, st, val, exp, st1, rev
    if flag == 'sto':
        sto.destroy()
    if flag == 'rev':
        rev.destroy()
    elif flag == 'st':
        st.destroy()
    elif flag == 'st1':
        st1.destroy()
    elif flag == 'val':
        val.destroy()
    elif flag == 'exp':
        exp.destroy()
    elif flag == 'd':
        d.destroy()
    main_window()


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
            main_window()
        elif i[0] == u and i[1] == p:
            root.destroy()
            print("user")
            # open_cus()
    login.commit()


again()

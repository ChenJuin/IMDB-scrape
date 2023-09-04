import tkinter as tk
from tkinter import *
from tkinter import ttk
import sqlite3

#open initial tkinter
window = tk.Tk()

window.title('IMDB Movie Data')
window.iconbitmap('imdb.ico')
window_width = 870
window_height = 500
window.resizable(False,False)

#set initial window to center
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x_cordinate = int((screen_width/2) - (window_width/2))
y_cordinate = int((screen_height/2) - (window_height/2))

window.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))

bg = PhotoImage(file = "bg.png")
bg_lbl = Label(window,image=bg)
bg_lbl.place(x=0,y=0,width=870,height=500)

#open welcome tkinter
welcome = Tk()
welcome.geometry('270x70')
welcome.title('Welcoming Messages')
welcome.iconbitmap('imdb.ico')
text = "Welcome to our website! \n You can find out the top 250 movies here! \n Enjoy~"
index = 0

lab = Label(welcome)
lab.pack()

def add(a):
    global index
    if index < len(text):
        lab.config(text=lab.cget("text") + text[index])
        index += 1
    welcome.after(100, add, welcome)

add(1)

#function for getting data from database for the top 250 movie
def movie_250():
    root = Tk()
    root.title('IMDb Top 250 Ranking Movie')
    root.iconbitmap('imdb.ico')
    root.geometry("850x500")

    def clear():
        r_entry.delete(0,END)
        n_entry.delete(0,END)
        y_entry.delete(0,END)
        rating_entry.delete(0,END)

    #add style
    style = ttk.Style()

    #theme
    style.theme_use('default')

    #configure treeview colors
    style.configure("Treeview",background="#D3D3D3",fg="black",rowheight=25,fieldbg="#D3D3D3")

    #change selected color
    style.map('Treeview',
        background=[('selected','#347083')])

    #create a treeview frame
    tree_frame = Frame(root)
    tree_frame.pack(pady=20)

    #create treeview scrollbar
    tree_scroll = Scrollbar(tree_frame)
    tree_scroll.pack(side=RIGHT,fill=Y)

    #create treeview
    tree = ttk.Treeview(tree_frame,yscrollcommand=tree_scroll.set,selectmode="extended")
    tree.pack()

    #configure scrollbar
    tree_scroll.config(command=tree.yview)

    #define column
    tree['columns'] = ("Rank","Name","Year","Cast","Rating","Link")

    #setting width of columns
    tree.column('#0',stretch=NO,width=0)
    tree.column('Rank',anchor=CENTER,width=45)
    tree.column('Name',anchor=W,width=250)
    tree.column('Year',anchor=CENTER,width=45)
    tree.column('Cast',anchor=W,width=180)
    tree.column('Rating',anchor=CENTER,width=65)
    tree.column('Link',anchor=W,width=200)

    #setting headings for columns
    tree.heading('#0',text="",anchor=W)
    tree.heading('Rank',text="Rank",anchor=CENTER)
    tree.heading('Name',text="Name",anchor=W)
    tree.heading('Year',text="Year",anchor=CENTER)
    tree.heading('Cast',text="Cast",anchor=W)
    tree.heading('Rating',text="Rating",anchor=CENTER)
    tree.heading('Link',text="Link",anchor=W)



    def query_database():
        #clear the treeview
        for record in tree.get_children():
            tree.delete(record)
        conn = sqlite3.connect('movierank.db')
        c = conn.cursor()
        c.execute("SELECT * FROM imdbmovie")
        records = c.fetchall()
        #add data to screen
        global count
        count = 0
        for record in records:
            if count % 2 == 0:
                tree.insert(parent='',index='end',iid=count,text='',values=(record[0],record[1],record[2],record[3],record[4],record[5]),tags=('evenrow',))
            else:
                tree.insert(parent='',index='end',iid=count,text='',values=(record[0],record[1],record[2],record[3],record[4],record[5]),tags=('oddrow',))
            #increment counter
            count += 1
        conn.commit()
        conn.close()

    def r_data():
        lookup_data = r_entry.get()
        #clear treeview
        for record in tree.get_children():
            tree.delete(record)
        conn = sqlite3.connect('movierank.db')
        c = conn.cursor()
        c.execute("SELECT * FROM imdbmovie WHERE Rank like ?",(lookup_data,))
        records = c.fetchall()
        #add data to screen
        global count
        count = 0
        for record in records:
            if count % 2 == 0:
                tree.insert(parent='',index='end',iid=count,text='',values=(record[0],record[1],record[2],record[3],record[4],record[5]),tags=('evenrow',))
            else:
                tree.insert(parent='',index='end',iid=count,text='',values=(record[0],record[1],record[2],record[3],record[4],record[5]),tags=('oddrow',))
            #increment counter
            count += 1
        conn.commit()
        conn.close()
        clear()

    def n_data():
        lookup_data = n_entry.get()
        #clear treeview
        for record in tree.get_children():
            tree.delete(record)
        conn = sqlite3.connect('movierank.db')
        c = conn.cursor()
        c.execute("SELECT * FROM imdbmovie WHERE Name like ?",('%'+str(lookup_data)+'%',))
        records = c.fetchall()
        #add data to screen
        global count
        count = 0
        for record in records:
            if count % 2 == 0:
                tree.insert(parent='',index='end',iid=count,text='',values=(record[0],record[1],record[2],record[3],record[4],record[5]),tags=('evenrow',))
            else:
                tree.insert(parent='',index='end',iid=count,text='',values=(record[0],record[1],record[2],record[3],record[4],record[5]),tags=('oddrow',))
            #increment counter
            count += 1
        conn.commit()
        conn.close()
        clear()

    def y_data():
        lookup_data = y_entry.get()
        #clear treeview
        for record in tree.get_children():
            tree.delete(record)
        conn = sqlite3.connect('movierank.db')
        c = conn.cursor()
        c.execute("SELECT * FROM imdbmovie WHERE Year like ?",('%'+str(lookup_data)+'%',))
        records = c.fetchall()
        #add data to screen
        global count
        count = 0
        for record in records:
            if count % 2 == 0:
                tree.insert(parent='',index='end',iid=count,text='',values=(record[0],record[1],record[2],record[3],record[4],record[5]),tags=('evenrow',))
            else:
                tree.insert(parent='',index='end',iid=count,text='',values=(record[0],record[1],record[2],record[3],record[4],record[5]),tags=('oddrow',))
            #increment counter
            count += 1
        conn.commit()
        conn.close()
        clear()

    def rating_data():
        lookup_data = rating_entry.get()
        #clear treeview
        for record in tree.get_children():
            tree.delete(record)
        conn = sqlite3.connect('movierank.db')
        c = conn.cursor()
        c.execute("SELECT * FROM imdbmovie WHERE Rating like ?",('%'+str(lookup_data)+'%',))
        records = c.fetchall()
        #add data to screen
        global count
        count = 0
        for record in records:
            if count % 2 == 0:
                tree.insert(parent='',index='end',iid=count,text='',values=(record[0],record[1],record[2],record[3],record[4],record[5]),tags=('evenrow',))
            else:
                tree.insert(parent='',index='end',iid=count,text='',values=(record[0],record[1],record[2],record[3],record[4],record[5]),tags=('oddrow',))
            #increment counter
            count += 1
        conn.commit()
        conn.close()
        clear()

    #create striped row tags
    tree.tag_configure('oddrow',background="white")
    tree.tag_configure('evenrow',background="lightblue")

    #add search box
    search_frame = LabelFrame(root,text="Search By")
    search_frame.pack(fill="x",expand="yes",padx=20)

    r_label = Label(search_frame,text="Rank:")
    r_label.grid(row=0,column=0,padx=10,pady=5)
    r_entry = Entry(search_frame,width=105)
    r_entry.grid(row=0,column=1,padx=10,pady=5)

    r_btn = Button(search_frame,text="Search",command=r_data)
    r_btn.grid(row=0,column=2,padx=10,pady=5)

    n_label = Label(search_frame,text="Name:")
    n_label.grid(row=1,column=0,padx=10,pady=5)
    n_entry = Entry(search_frame,width=105)
    n_entry.grid(row=1,column=1,padx=10,pady=5)

    n_btn = Button(search_frame,text="Search",command=n_data)
    n_btn.grid(row=1,column=2,padx=10,pady=5)

    y_label = Label(search_frame,text="Year:")
    y_label.grid(row=2,column=0,padx=10,pady=5)
    y_entry = Entry(search_frame,width=105)
    y_entry.grid(row=2,column=1,padx=10,pady=5)

    y_btn = Button(search_frame,text="Search",command=y_data)
    y_btn.grid(row=2,column=2,padx=10,pady=5)

    rating_label = Label(search_frame,text="Rating:")
    rating_label.grid(row=3,column=0,padx=10,pady=5)
    rating_entry = Entry(search_frame,width=105)
    rating_entry.grid(row=3,column=1,padx=10,pady=5)

    rating_btn = Button(search_frame,text="Search",command=rating_data)
    rating_btn.grid(row=3,column=2,padx=10,pady=5)

    reset_btn = Button(root,text="Reset",command=query_database)
    reset_btn.pack(padx=20,pady=20)

    #run to pull data from database on start
    query_database()

    root.mainloop()

#button for the third tkinter
img2 = PhotoImage(file="t.png")
l_icon = Button(image=img2,borderwidth=0,cursor="hand2",command=movie_250)
l_icon.place(x=234,y=203)

welcome.mainloop()

window.mainloop()

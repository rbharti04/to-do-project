#Python version 3.10.0
from asyncio import tasks
from queue import PriorityQueue
import tkinter
import tkinter.messagebox
from tkinter import * #imports all tkinter functions and modules
from tkinter import ttk #style widget
from tkinter.ttk import Treeview 
import sqlite3
from typing import List

app = Tk()

# Setup the database
class Database:
    def __init__(self,db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS to-do (id INTEGER PRIMARY KEY, task text, due text, priority integer)")
        self.conn.commit()
    def fetch(self, task=''):
        self.cur.execute("SELECT * FROM to-do where task LIKE ?", ('%'+task+'%'))
        rows = self.cur.fetchall()
        return rows

    def fetch2(self, priority):
        self.cur.execute(priority)
        rows = self.cur.fetchall()
        return rows
    
    def insert(self, task, due, priority):
        self.cur.execute("INSERT INTO to-do VALUES (NULL, ?, ?, ?)", (task, due, priority))
        self.conn.commit()
    
    def remove(self, id):
        self.cur.execute("DELETE FROM to-do WHERE id=?", (id,))
        self.conn.commit()
    
    def update(self, id, task, due, priority):
        self.cur.execute("UPDATE to-do SET task = ?, due = ?, priority = ?", (task, due, priority, id))
        self.conn.commit()

    def __del__(self):
        self.conn.close()

def clear_text():
    task_entry.delete(0, END)
    due_date_entry.delete(0, END)
    priority_entry.delete(0, END)

def populate_list(task=''):
    for i in task_tree_view.get_children():
        task_tree_view.delete(i)
    for row in fetch(task):
        task_tree_view.insert('', 'end', values=row)

def populate_list2(search='SELECT * FROM tasks'):
    for i in task_tree_view.get_children():
        task_tree_view.delete(i)
    for row in fetch2(tasks):
        task_tree_view.insert('', 'end', values=row)

def add_task():
    if task_text.get() == '' or due_date_text.get() == '' or priority_text.get() == '':
        tkinter.messagebox.showwarning('Required Fields', 'Please include all fields')
        return
    cur.execute(task_text.get(), due_date_text.get(), priority_text.get())
    clear_text()
    populate_list()

def delete_task():
    id = selected_item[0]
    cur.execute("DELETE FROM tasks WHERE id=?", (id,))
    clear_text()
    populate_list()
        
def select_task(event):
    try:
        global selected_item
        index = task_tree_view.selection()[0]
        selected_item = task_tree_view.item(index)['values']
        task_entry.delete(0, END)
        task_entry.insert(END, selected_item[1])
        due_date_entry.delete(0, END)
        due_date_entry.insert(END, selected_item[2])
        priority_entry.delete(0, END)
        priority_entry.insert(END, selected_item[3])
    except IndexError:
        pass

def search_task():
    search = search_task.get()
    populate_list(tasks)

def search_priority():
    priority= priority_search.get()
    populate_list2(priority)

#Create GUI
frame_search = Frame(app)
frame_search.grid(row=0, column=0) #using .grid allows you to control which part of the grid the edits will apply to

lbl_search = Label(frame_search, text='Search by task', font=('bold', 12), pady=20)
lbl_search.grid(row=0, column=0, sticky=W) #what is sticky and what does the W and E do?
task_search = StringVar()
task_search_entry = Entry(frame_search, textvariable=task_search)
task_search_entry.grid(row=0, column=1)

lbl_search = Label(frame_search, text='Search by Priority', font=('bold', 12), pady=20)
lbl_search.grid(row=1, column=0, sticky=W)
priority_search = StringVar()
priority_search.set("Select * from high priority tasks")
priority_search_entry = Entry(frame_search, textvariable=priority_search, width=40)
priority_search_entry.grid(row=1, column=1)

frame_fields = Frame(app)
frame_fields.grid(row=1, column=0)

#task
task_text = StringVar()
task_label = Label(frame_fields, text='task', font=('bold', 12))
task_label.grid(row=0, column=0, sticky=E)
task_entry = Entry(frame_fields, textvariable=task_text)
task_entry.grid(row=0, column=1, sticky=W)
#priority
priority_text = StringVar()
priority_label = Label(frame_fields, text='Priority (1 low - 10 high)', font=('bold', 12))
priority_label.grid(row=0, column=2, sticky=E)
priority_entry = Entry(frame_fields, textvariable=priority_text)
priority_entry.grid(row=1, column=1, sticky=W)
#due date
due_date_text = StringVar()
due_date_label = Label(frame_fields, text='Due Date (dd/mm/yyyy)', font=('bold', 12))
due_date_label.grid(row=1, column=0, sticky=E)
due_date_entry = Entry(frame_fields, textvariable=due_date_text)
due_date_entry.grid(row=2, column=1, sticky=W)

frame_task = Frame(app)
frame_task.grid(row=4, column=0, columnspan=4, rowspan=6, pady=20, padx=20)

columns = ['id', 'Task', 'Priority', 'Due Date'] #what is the id for?
task_tree_view = Treeview(frame_task, columns=columns, show="headings") #why do we put columns=columns?
task_tree_view.column("id", width=30)
for col in columns[1:]:
    task_tree_view.column(col, width=120)
    task_tree_view.heading(col, text=col)
task_tree_view.bind('<<TreeviewSelect>>', select_task)#why are there the double arrow (<<,>>)
task_tree_view.pack(side="left", fill="y")
scrollbar = Scrollbar(frame_task, orient= 'vertical')
scrollbar.configure(command=task_tree_view.yview)
scrollbar.pack(side="right", fill="y")
task_tree_view.config(yscrollcommand=scrollbar.set)

frame_btns = Frame(app)
frame_btns.grid(row=3, column=0)

button_add_task = tkinter.Button(frame_btns, text='Add Task', command=add_task)
button_add_task.grid(row=0, column = 0, pady=20)

button_delete_task = tkinter.Button(frame_btns, text='Delete task', command=delete_task)
button_delete_task.grid(row=0, column=1)

button_clear = Button(frame_btns, text='Clear Input', command= clear_text)
button_clear.grid(row=0, column=3)

search_btn = Button(frame_search, text='Search tasks', width=12, command=search_task)
search_btn.grid(row=0, column=2)

search_priority_btn = Button(frame_search, text='Search priority', width=12, command=search_priority)
search_priority_btn.grid(row=1, column=2)

frame_task = tkinter.Frame(app)
frame_task.grid(row=5, column=0, columnspan=4, rowspan=6, pady=20, padx=20)
columns = ['id','Priority','Due Date','Task']

app.title('To-do List')
app.geometry('700x550')

populate_list()

app.mainloop() #start program
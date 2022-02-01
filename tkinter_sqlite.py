#Python version 3.10.0
from queue import PriorityQueue
import tkinter
import tkinter.messagebox
from tkinter import * #imports all tkinter functions and modules
from tkinter import ttk #style widget
from tkinter.ttk import Treeview 
import sqlite3
from typing import List

# Setup the database
conn = sqlite3.connect('tasks.sqlite')
cur = conn.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS tasks(
   id INTEGER PRIMARY KEY AUTOINCREMENT,
   task TEXT,
   due TEXT,
   priority INT);
""") #sets up the table with task, due date, and priority using text and integers
conn.commit()

win = tkinter.Tk() #creating the main window and storing the window object in 'win'
#We create the widgets here
win.title('To-Do List') #setting the title of the window
win.geometry('600x400') #setting the size of the window

def clear_text():
    task_entry.delete(0, END)
    due_entry.delete(0, END)
    priority_entry.delete(0, END)
    
def fetch(task=''):
        cur.execute("SELECT * FROM tasks WHERE task LIKE ?", ('%'+task+'%',))#why is there a comma within the second set of parantheses on this line?
        rows = cur.fetchall()
        return rows

def populate_list(task=''):
    for i in view.get_tasks():
        view.delete(i)
    for row in fetch(task):
        view.insert('', 'end', values=row)

def add_task():
    if task_text.get() == '' or due_text.get() == '' or priority_text.get() == '':
        tkinter.messagebox.showwarning('Required Fields', 'Please include all fields')
        return
    cur.execute("INSERT INTO tasks (task, due, priority) VALUES (?, ?, ?)", (str(task_text.get()), str(due_text.get), str(priority_text.get)))
    clear_text()
    populate_list()

def delete_task():
    id = selected_item[0]
    cur.execute("DELETE FROM tasks WHERE id=?", (id,))
    conn.commit()
    clear_text()
    populate_list()
        
def select_task(event):
    try:
        global selected_item
        index = view.selection()[0]
        selected_item = view.item(index)['values']
        task_entry.delete(0, END)
        task_entry.insert(END, selected_item[1])
        due_entry.delete(0, END)
        due_entry.insert(END, selected_item[2])
        priority_entry.delete(0, END)
        priority_entry.insert(END, selected_item[3])
    except IndexError:
        pass

#Create GUI
app = Tk()
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
priority_label = Label(frame_fields, text='priority', font=('bold', 12))
priority_label.grid(row=0, column=2, sticky=E)
priority_entry = Entry(frame_fields, textvariable=priority_text)
priority_entry.grid(row=0, column=2, sticky=W)
#due date
due_date_text = StringVar()
due_date_label = Label(frame_fields, text='due date', font=('bold', 12))
due_date_label.grid(row=1, column=0, sticky=E)
due_date_entry = Entry(frame_fields, textvariable=due_date_text)
due_date_entry.grid(row=1, column=1, sticky=W)

task_text = StringVar()
task_label = tkinter.Label(win, text='Task Text', font=('bold', 12))
task_label.grid(row=0, column=0, sticky=E)
task_entry = tkinter.Entry(win, textvariable=task_text, width = 50)
task_entry.grid(row=0, column=1, sticky=W)

priority_text = StringVar()
priority_label = tkinter.Label(win, text='Priority (1 low - 10 high)', font=('bold', 12))
priority_label.grid(row=1, column=0, sticky=E)
priority_entry = tkinter.Entry(win, textvariable=priority_text, width = 50)
priority_entry.grid(row=1, column=1, sticky=W)

due_text = StringVar()
due_label = tkinter.Label(win, text='Due Date (dd/mm/yyyy)', font=('bold', 12))
due_label.grid(row=2, column=0, sticky=E)
due_entry = tkinter.Entry(win, textvariable=due_text, width = 50)
due_entry.grid(row=2, column=1, sticky=W)

frame_router = Frame(app)
frame_router.grid(row=4, column=0, columnspan=4, rowspan=6, pady=20, padx=20)

columns = ['id', 'Task', 'Priority', 'Due Date'] #what is the id for?
router_tree_view = Treeview(frame_router, columns=columns, show="headings") #why do we put columns=columns?
router_tree_view.column("id", width=30)

frame_btns = tkinter.Frame(win)
frame_btns.grid(row=3, column=0)

button_add_task = tkinter.Button(frame_btns, text="Add Task", command=add_task)
button_add_task.grid(row=4, column = 0, padx=20, pady=20)

button_delete_task = tkinter.Button(frame_btns, text="Delete task", command=delete_task)
button_delete_task.grid(row=4, column = 1)

frame_tasks = tkinter.Frame(win)
frame_tasks.grid(row=5, column=0, columnspan=4, rowspan=6, pady=20, padx=20)
columns = ['id','Priority','Due Date','Task']

view = ttk.Treeview(frame_tasks, columns=columns, show="headings")
view.column("id", width=20)
for col in columns[1:]:
    view.column(col, width = 120)
    view.heading(col, text=col)
view.bind('<<TreeviewSelect>>',select_task)
view.pack(side="left", fill="y")
scrollbar = tkinter.Scrollbar(frame_tasks, orient='vertical')
scrollbar.configure(command=view.yview)
scrollbar.pack(side="right", fill="y")
view.config(yscrollcommand=scrollbar.set)

win.mainloop() #running the loop that works as a trigger

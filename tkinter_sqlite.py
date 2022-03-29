#Python version 3.10.0
import tkinter
import tkinter.messagebox
from tkinter import * #imports all tkinter functions and modules
from tkinter import ttk #style widget
import sqlite3
from matplotlib.pyplot import text
from tkcalendar import *
from numpy import row_stack

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
win.geometry('800x400') #setting the size of the window

def clear_text():
    task_entry.delete(0, END)
    due_entry.delete(0, END)
    priority_entry.delete(0, END)

def fetch(task=''):
        cur.execute("SELECT * FROM tasks WHERE task LIKE ?", ('%'+task+'%',))
        rows = cur.fetchall()
        return rows

def sort_lowest(task=''):
        cur.execute("SELECT * FROM tasks WHERE task LIKE ? ORDER BY priority ASC", ('%'+task+'%',))
        rows = cur.fetchall()
        for i in view.get_children():
            view.delete(i)
        for row in rows:
            row = [row[0], row[3], row[2], row[1]]
            view.insert('', 'end', values=row)

def sort_highest(task=''):
        cur.execute("SELECT * FROM tasks WHERE task LIKE ? ORDER BY priority DESC", ('%'+task+'%',))
        rows = cur.fetchall()
        for i in view.get_children():
            view.delete(i)
        for row in rows:
            row = [row[0], row[3], row[2], row[1]]
            view.insert('', 'end', values=row)

def sort_recent(task=''):
        cur.execute("SELECT * FROM tasks WHERE task LIKE ? ORDER BY due ASC", ('%'+task+'%',))
        rows = cur.fetchall()
        for i in view.get_children():
            view.delete(i)
        for row in rows:
            row = [row[0], row[3], row[2], row[1]]
            view.insert('', 'end', values=row)

def populate_list(task=''):
    for i in view.get_children():
        view.delete(i)
    for row in fetch(task):
        a=[row[0], row[3], row[2], row[1]]#a is the array and then i can insert the correct order with the insert calling upon 'a' instead of the row order
        view.insert('', 'end', values=a)

def add_task():
    if task_text.get() == '' or due_text.get() == '' or priority_text.get() == '':
        tkinter.messagebox.showwarning('Required Fields', 'Please include all fields')
        return
    cur.execute("INSERT INTO tasks (task, due, priority) VALUES (?, ?, ?)", (str(task_text.get()), str(due_text.get()), str(priority_text.get())))
    clear_text()
    populate_list()
    conn.commit()

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
priority_text = StringVar()
priority_label = tkinter.Label(win, text='Priority (1 low - 10 high)', font=('bold', 12))
priority_label.grid(row=0, column=0, sticky=E) #using .grid allows you to control which part of the grid the edits will apply to, E=East
priority_entry = tkinter.Entry(win, textvariable=priority_text, width = 50)
priority_entry.grid(row=0, column=1, sticky=W)

due_text = StringVar()
due_label = tkinter.Label(win, text='Due Date (dd/mm/yyyy)', font=('bold', 12))
due_label.grid(row=1, column=0, sticky=E)
due_entry = DateEntry(win, width=20, bd=2, textvariable=due_text)
due_entry.grid(row=1, column=1, sticky=W)

task_text = StringVar()
task_label = tkinter.Label(win, text='Task Text', font=('bold', 12))
task_label.grid(row=2, column=0, sticky=E)
task_entry = tkinter.Entry(win, textvariable=task_text, width = 50)
task_entry.grid(row=2, column=1, sticky=W)

frame_btns = tkinter.Frame(win)
frame_btns.grid(row=3, column=0)

button_add_task = tkinter.Button(frame_btns, text="Add Task", command=add_task)
button_add_task.grid(row=4, column = 1, pady=20)

button_delete_task = tkinter.Button(frame_btns, text="Delete Task", command=delete_task)
button_delete_task.grid(row=4, column = 2, pady=20)

button_sort_low = tkinter.Button(frame_btns, text="Sort by Lowest Priority", command=sort_lowest)
button_sort_low.grid(row=4, column = 3, pady=20)

button_sort_high = tkinter.Button(frame_btns, text="Sort by Highest Priority", command=sort_highest)
button_sort_high.grid(row=4, column = 4, pady=20)

button_sort_recent = tkinter.Button(frame_btns, text="Sort by Recent Due Dates", command=sort_recent)
button_sort_recent.grid(row=4, column = 5, pady=20)

frame_tasks = tkinter.Frame(win)
frame_tasks.grid(row=5, column=0, columnspan=4, rowspan=6, pady=20, padx=20)
columns = ['id','Priority','Due Date','Task']

view = ttk.Treeview(frame_tasks, columns=columns, show="headings")
view.column("id", width=10)
for col in columns[1:]:
    view.column(col, width = 170)
    view.heading(col, text=col)
view.bind('<<TreeviewSelect>>',select_task)
view.pack(side="left", fill="y")
scrollbar = tkinter.Scrollbar(frame_tasks, orient='vertical')
scrollbar.configure(command=view.yview)
scrollbar.pack(side="right", fill="y")
view.config(yscrollcommand=scrollbar.set)

populate_list()
win.mainloop() #running the loop that works as a trigger
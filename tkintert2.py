#Python version 3.10.0
from msilib import Table
import tkinter
import tkinter.messagebox
import pickle
import sqlite3

conn = sqlite3.connect('AA_db.sqlite')
cur = conn.cursor()
cur.execute('CREATE TABLE experiments (task VARCHAR, due date VARCHAR, priority VARCHAR)')
conn.commit()

win = tkinter.Tk() #creating the main window and storing the window object in 'win'
#We create the widgets here
win.title('To-Do List') #setting the title of the window
win.geometry('500x400') #setting the size of the window
List = []

def add_task():
    task = entry_task.get()
    if task != "":
        List.append(task)
        update_gui()

    else:
        tkinter.messagebox.showwarning(title="Warning!", message="You must enter a task.")

def update_gui():
    listbox_tasks.delete(0,listbox_tasks.size()) #delete all of the current tasks from the gui
    for item in List:
        listbox_tasks.insert(tkinter.END, item) #add each item in our python List back to the gui
        entry_task.delete(0, tkinter.END)

def delete_task():
    try:
        task_index = listbox_tasks.curselection() [0] #cur-selection NOT curse-selection
        List.pop(task_index) #pop function to remove the task from the list
        listbox_tasks.delete(task_index)
    except:
       tkinter.messagebox.showwarning(title="Warning!", message="You must select a task.") 

def load_tasks():
    try:
        tasks = pickle.load(open("tasks.dat","rb"))
        listbox_tasks.delete(0, tkinter.END)
        for task in tasks:
            listbox_tasks.insert(tkinter.END, task)
    except:
        tkinter.messagebox.showwarning(title="Warning!", message="No tasks found.")

def save_tasks():
    tasks = listbox_tasks.get(0, listbox_tasks.size())
    
    pickle.dump(tasks, open("tasks.dat", "wb"))

#Create GUI
frame_tasks = tkinter.Frame(win)
frame_tasks.pack()

listbox_tasks = tkinter.Listbox(frame_tasks,height=15,width=50)
listbox_tasks.pack(side=tkinter.LEFT)

scrollbar_tasks = tkinter.Scrollbar(frame_tasks)
scrollbar_tasks.pack(side=tkinter.RIGHT, fill=tkinter.Y)

listbox_tasks.config(yscrollcommand=scrollbar_tasks.set)
scrollbar_tasks.config(command=listbox_tasks.yview)

entry_task=tkinter.Entry(win, width=50)
entry_task.pack()

button_add_task = tkinter.Button(win, text="Add task", width=50, command=add_task)
button_add_task.pack()

button_delete_task = tkinter.Button(win, text="Delete task", width=50, command=delete_task)
button_delete_task.pack()

button_load_tasks = tkinter.Button(win, text="Load tasks", width=50, command=load_tasks)
button_load_tasks.pack()

button_save_tasks = tkinter.Button(win, text="Save tasks", width=50, command=save_tasks)
button_save_tasks.pack()

win.mainloop() #running the loop that works as a trigger
#Python version 3.10.0
import tkinter
import tkinter.messagebox
import sqlite3

# Setup the database
conn = sqlite3.connect('tasks.sqlite')
cur = conn.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS tasks(
   task TEXT,
   due TEXT,
   priority INT);
""")
conn.commit()

win = tkinter.Tk() #creating the main window and storing the window object in 'win'
#We create the widgets here
win.title('To-Do List') #setting the title of the window
win.geometry('500x400') #setting the size of the window

def add_task():
    task = entry_task.get()
    if task != "":
        full_task = (task, "never", 1)
        cur.execute("INSERT INTO tasks VALUES(?, ?, ?);", full_task)
        conn.commit()
        update_gui()
    else:
        tkinter.messagebox.showwarning(title="Warning!", message="You must enter a task.")

def delete_task():
    try:
        task_pos = listbox_tasks.curselection()[0] #cur-selection NOT curse-selection
        task = listbox_tasks.get(task_pos)
        # WARNING: If duplicate tasks exist, this will currently delete them all!
        cur.execute("DELETE FROM tasks WHERE task=?;",(str(task[0]),))
        conn.commit()
        update_gui()
    except:
       tkinter.messagebox.showwarning(title="Warning!", message="You must select a task.") 
       
def update_gui():
    listbox_tasks.delete(0,listbox_tasks.size()) # delete all of the current tasks from the gui
    cur.execute("SELECT * FROM tasks;")
    all_results = cur.fetchall()
    for item in all_results:
        listbox_tasks.insert(tkinter.END, item) # add each item in our python List back to the gui
        entry_task.delete(0, tkinter.END)

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

update_gui()

win.mainloop() #running the loop that works as a trigger
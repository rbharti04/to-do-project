import pandas as pd
import datetime
from datetime import datetime
import os.path as path

if path.exists('to_do.csv'):
    to_do = pd.read_csv('to_do.csv', header=0)
else:
    columns = ['date_due', 'item', 'priority']
    to_do = pd.DataFrame(columns=columns)

action = ''

while action != 'Q':
  action = str(input("Enter what you want to do: 'A' for add, 'D' for delete, 'P' for print, 'S' for sort, or 'Q' for quit: ")).upper()
  if action == 'A':
    date = input('Enter date due (ex 2021, 11, 22):')
    year, month, day = map(int, date.split(','))
    due = datetime(year, month, day)
    due = str(due)
    due = due[:10]
    due_item = input("Enter the item you need to do: ")
    ranking = input("Please enter the priority of this item (ex Low, Medium, High): ")
    to_do = to_do.append({'date_due' : due, 'item' : due_item, 'priority' : ranking}, ignore_index=True)
  elif action == 'D':
    del_no = input("please enter the index number of the to_do item you would like to delete: ")
    del_no = int(del_no)
    to_do.drop([del_no], inplace=True)
  elif action == 'P': print(to_do)
  elif action == 'S':
    sorted = input("please enter how you want the list sorted: 'D' for date-due or 'P' for priority: ").upper()
    if sorted == 'D': to_do = to_do.sort_values(by='date_due')
    elif sorted == 'P': to_do = to_do.sort_values(by='priority')
  elif action == 'Q': break
to_do.to_csv ('to_do.csv', index = False)
to_do = pd.read_csv('to_do.csv')
print(to_do)
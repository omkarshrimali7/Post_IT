import tkinter as tk
import pyodbc
from datetime import datetime
from datetime import date
conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb)};DBQ=Post-It.mdb;')
cursor = conn.cursor()




def sub(dummy_event):
    data = (lb.get(lb.curselection()[0]))
    index = data.find(':')
    index2 = data.find(';')
    mini = tk.Toplevel(window)
    mini.attributes("-toolwindow", 1)
    uid = int(data[:index])
    mini.title(uid)
    textbox = tk.Text(mini,height = 30, width = 30,wrap = 'word')
    textbox.insert('1.0',data[index2+2:]+"")
    textbox.pack()
    textbox.focus_set()
    b1 = tk.Button(mini, text='Save', width=15, height=2, command=lambda: save_f(mini,textbox.get("1.0",'end-1c'),uid))
    b2 = tk.Button(mini, text='Delete', width=15, height=2, command = lambda: delete_f(mini,uid))
    b1.pack(side = tk.LEFT)
    b2.pack(side = tk.RIGHT)
    mini.mainloop()

def add_new():
    mini = tk.Toplevel(window)
    mini.title("Add New")
    textbox = tk.Text(mini,height = 30, width = 30)
    textbox.pack()
    textbox.focus_set()
    b1 = tk.Button(mini, text='Save', width=15, height=2, command=lambda: save_f(mini,textbox.get("1.0",'end-1c')))
    b1.pack()
    mini.mainloop()

def save_f(mini,data,uid = 0):
    today = date.today()
    if(uid):
        query = "UPDATE MAIN SET Data = '"+data+"',Updated = '"+str(today)+"'WHERE UID ="+str(uid)+";"
##        print(query)
        cursor.execute(query)
    else:
        query = "INSERT INTO Main ([Data],[Updated]) VALUES ('"+data+"','"+str(today)+"');"
##        print(query)
        cursor.execute(query)
    conn.commit()
    update()
    mini.destroy()

def update():
    cursor.execute('select * from MAIN')
    lb.delete(0,'end')
    for key in cursor.fetchall():
        lb.insert('end','{}: Last Updated {}; {}'.format(key[0],key[2],key[1]))

def delete_f(mini,uid):
    cursor.execute('DELETE FROM MAIN WHERE UID='+str(uid)+';')
    conn.commit()
    update()
    mini.destroy()
        
    


    
    
    
    



window = tk.Tk()
lb = tk.Listbox(window,width = 300, height = 300)
window.title('Post-It')

 
window.geometry('500x300') 
update()

b1 = tk.Button(window, text='Add New', width=15, height=2, command=add_new)
b1.pack()
lb.pack()
lb.bind("<Double-Button-1>",sub)
window.mainloop()

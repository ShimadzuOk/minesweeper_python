import random
from tkinter import *

previous_grid = 0

def  ch_button(col,row):
    btn = result_frame.grid_slaves(column=col, row=row)[0]
    btn.grid_forget()
    pass

def draw_cells():
    global previous_grid
    [i.grid_forget() for i in result_frame.grid_slaves()]
    for i in range(previous_grid):
        result_frame.columnconfigure(i, weight=0)
        result_frame.rowconfigure(i, weight=0)
    
    # Get cells number
    cells_n = int(cells_number_entry.get())
    mine_n = int(mine_number_entry.get())
    previous_grid = cells_n
    
    # Draw
    for i in range(cells_n):
        result_frame.columnconfigure(i, weight=1)
        result_frame.rowconfigure(i, weight=1)

        for j in range(cells_n):
            lbl = Label(result_frame,text="   ")
            lbl.grid(column=i, row=j, sticky=(N,S,W,E), padx=5.5, pady=5.5)

            btn = Button(result_frame, text = "   ", command=lambda col=i, row=j: ch_button(col,row))
            btn.grid(column=i, row=j, sticky=(N,S,W,E), padx=3, pady=3)
            pass
    
    
    labels = [i for i in result_frame.grid_slaves() if isinstance(i,Label)]
    mines = []

    for i in range(mine_n):
        ind = random.randint(0,len(labels)-1)
        labels[ind].config(text = "\U0001F4A3")
        mines.append(labels[ind])
        labels.remove(labels[ind])


    for m in mines:
        m:Label
        column = m.grid_info()["column"]
        row = m.grid_info()["row"]
        for l in labels:
            if l.grid_info()["column"] == column and l.grid_info()["row"] == row + 1: l.configure(text = f"{1 if l.cget("text") =="   " else int(l.cget("text"))+1}")
            if l.grid_info()["column"] == column and l.grid_info()["row"] == row - 1: l.configure(text = f"{1 if l.cget("text") =="   " else int(l.cget("text"))+1}")
            if l.grid_info()["column"] == column - 1 and l.grid_info()["row"] == row: l.configure(text = f"{1 if l.cget("text") =="   " else int(l.cget("text"))+1}")
            if l.grid_info()["column"] == column + 1 and l.grid_info()["row"] == row: l.configure(text = f"{1 if l.cget("text") =="   " else int(l.cget("text"))+1}")
            if l.grid_info()["column"] == column + 1 and l.grid_info()["row"] == row + 1: l.configure(text = f"{1 if l.cget("text") =="   " else int(l.cget("text"))+1}")
            if l.grid_info()["column"] == column - 1 and l.grid_info()["row"] == row - 1: l.configure(text = f"{1 if l.cget("text") =="   " else int(l.cget("text"))+1}")
            if l.grid_info()["column"] == column - 1 and l.grid_info()["row"] == row + 1: l.configure(text = f"{1 if l.cget("text") =="   " else int(l.cget("text"))+1}")
            if l.grid_info()["column"] == column + 1 and l.grid_info()["row"] == row - 1: l.configure(text = f"{1 if l.cget("text") =="   " else int(l.cget("text"))+1}")




main_window = Tk()

controls_frame = Frame()
result_frame = Frame()
controls_frame.pack()
result_frame.pack(expand=True, fill=BOTH,anchor="center")


# Widgets
Label(controls_frame, text="Cells number: ").grid(row=0,column=0,sticky=EW)
cells_number_entry = Entry(controls_frame)
cells_number_entry.grid(row=0,column=1,sticky=EW)
Button(controls_frame, text="Draw cells", command=draw_cells).grid(row=0,column=2,rowspan=2,sticky=NSEW)
Label(controls_frame, text="Mine number: ").grid(row=1,column=0,sticky=EW)
mine_number_entry = Entry(controls_frame)
mine_number_entry.grid(row=1,column=1,sticky=EW)


main_window.mainloop()

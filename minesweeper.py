import random
from tkinter import *


class MainFrame(Tk):
    def __init__(self):
        super().__init__()
        self.title("Minesweeper")
        self.result_frame = ResultFrame(self)
        self.controls_frame = ControlFrame(self)
        self.controls_frame.pack()
        self.result_frame.pack(expand=True, fill=BOTH,anchor="center")

class ControlFrame(Frame):
    def __init__(self, master_w:MainFrame):
        super().__init__(master = master_w)
        self.master_w = master_w

        self.lbl1 = Label(self, text="Cells number: ")
        self.lbl2 = Label(self, text="Mine number: ")
        self.action_btn = Button(self, text="Draw cells", command= self.master_w.result_frame.draw_cells)
        self.cells_number_entry = Entry(self)
        self.mine_number_entry = Entry(self)
        self.gm_over = Label(self,text="GAME OVER")

        self.mine_number_entry.grid(row=1,column=1,sticky=EW)
        self.cells_number_entry.grid(row=0,column=1,sticky=EW)
        self.lbl1.grid(row=0,column=0,sticky=EW)
        self.lbl2.grid(row=1,column=0,sticky=EW)
        self.action_btn.grid(row=0,column=2,rowspan=2,sticky=NSEW)


class ResultFrame(Frame):
    def __init__(self, master_w:MainFrame):
        super().__init__(master = master_w)
        self.master_w = master_w
        self.previous_grid = 0

    def  ch_button(self,col,row):
        btn = [i for i in self.master_w.result_frame.grid_slaves(column=col, row=row) if isinstance(i,Button)]
        btn[0].grid_forget()

        for lbl in [i for i in self.master_w.result_frame.grid_slaves() if isinstance(i,Label)]:

            if lbl.cget("text") == "\U0001F4A3" and lbl.grid_info()["column"] == col and lbl.grid_info()["row"] == row:

                self.master_w.controls_frame.gm_over.grid(row=2,column=0,columnspan=3,sticky=NSEW)
                
                for lbl in self.master_w.result_frame.grid_slaves():
                            if isinstance(lbl, Label) and lbl.cget("text") == "\U0001F4A3":
                                lbl.lift()


    def draw_cells(self):
        self.master_w.controls_frame.gm_over.grid_forget()
        [i.grid_forget() for i in self.master_w.result_frame.grid_slaves()]
        for i in range(self.previous_grid):
            self.master_w.result_frame.columnconfigure(i, weight=0)
            self.master_w.result_frame.rowconfigure(i, weight=0)
        
        # Get cells number
        cells_n = int(self.master_w.controls_frame.cells_number_entry.get())
        mine_n = int(self.master_w.controls_frame.mine_number_entry.get())
        self.previous_grid = cells_n
        
        # Draw
        for i in range(cells_n):
            self.master_w.result_frame.columnconfigure(i, weight=1)
            self.master_w.result_frame.rowconfigure(i, weight=1)

            for j in range(cells_n):
                lbl = Label(self.master_w.result_frame,text="   ")
                lbl.grid(column=i, row=j, sticky=(N,S,W,E), padx=5.5, pady=5.5)

                btn = Button(self.master_w.result_frame, text = "   ", command=lambda col=i, row=j: self.ch_button(col,row))
                btn.grid(column=i, row=j, sticky=(N,S,W,E), padx=3, pady=3)
                pass
        
        
        labels = [i for i in self.master_w.result_frame.grid_slaves() if isinstance(i,Label)]
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



main_window = MainFrame()
main_window.mainloop()





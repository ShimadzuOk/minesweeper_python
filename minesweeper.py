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
        self.win = Label(self,text="YOU WIN!")

        self.mine_number_entry.grid(row=1,column=1,sticky=EW)
        self.cells_number_entry.grid(row=0,column=1,sticky=EW)
        self.lbl1.grid(row=0,column=0,sticky=EW)
        self.lbl2.grid(row=1,column=0,sticky=EW)
        self.action_btn.grid(row=0,column=2,rowspan=2,sticky=NSEW)


class ResultFrame(Frame):
    def __init__(self, master_w:MainFrame):
        super().__init__(master = master_w)
        self.master_w = master_w
        self.mines = []
        self.btns = []
        self.previous_grid = 0


    def  ch_button(self,col,row):
        btn = [i for i in self.grid_slaves(column=col, row=row) if isinstance(i,Button)][0]
        btn.grid_forget()

        if [lbl for lbl in self.grid_slaves(row=row,column=col) if isinstance(lbl,Label) and lbl.cget("text") == "   "]: self.blank_zone(col,row)

        if [lbl for lbl in self.grid_slaves(row=row,column=col) if lbl.cget("text") == "\U0001F4A3"]:
            self.master_w.controls_frame.gm_over.grid(row=2,column=0,columnspan=3,sticky=NSEW)
            [mines.configure(bg="red") for mines in self.mines]
            [btn.grid_forget() for btn in self.btns]
    
        if len([i for i in self.grid_slaves() if isinstance(i,Button)]) == len(self.mines):
            self.master_w.controls_frame.win.grid(row=2,column=0,columnspan=3,sticky=NSEW)
            [mines.configure(bg="green") for mines in self.mines]
            [btn.grid_forget() for btn in self.btns]

    def blank_zone(self,col,row):
        area = []

        for r in range(row-1,row+2):
            for c in range(col-1,col+2):
                if c == col and r == row:continue
                try: area.append([btn for btn in self.grid_slaves(row=r,column=c) if isinstance(btn,Button)][0])
                except:pass
        
        for btn in area:
            btn:Button
            try:
                r = btn.grid_info()["row"]
                c = btn.grid_info()["column"]
                btn.grid_forget()
                if [i for i in self.grid_slaves(row=r,column=c) if isinstance(i,Label)][0].cget("text") == "   ": self.blank_zone(c,r)
            except:pass

    def draw_cells(self):
        # Reset
        self.mines =[]
        self.btns = []
        self.master_w.controls_frame.gm_over.grid_forget()
        self.master_w.controls_frame.win.grid_forget()
        [i.grid_forget() for i in self.grid_slaves()]
        for i in range(self.previous_grid):
            self.columnconfigure(i, weight=0)
            self.rowconfigure(i, weight=0)
        
        # Get cells number
        cells_n = int(self.master_w.controls_frame.cells_number_entry.get())
        mine_n = int(self.master_w.controls_frame.mine_number_entry.get())
        self.previous_grid = cells_n
        
        # Draw
        for i in range(cells_n):
            self.columnconfigure(i, weight=1)
            self.rowconfigure(i, weight=1)

            for j in range(cells_n):
                lbl = Label(self,text="   ")
                lbl.grid(column=i, row=j, sticky=(N,S,W,E), padx=5.5, pady=5.5)

                btn = Button(self, text = "   ", command=lambda col=i, row=j: self.ch_button(col,row))
                btn.grid(column=i, row=j, sticky=(N,S,W,E), padx=3, pady=3)
        
        self.btns = [i for i in self.grid_slaves() if isinstance(i,Button)]
        labels = [i for i in self.grid_slaves() if isinstance(i,Label)]

        for m in range(mine_n):
            if labels:
                ind = random.randint(0,len(labels)-1)
                labels[ind].configure(text = "\U0001F4A3")
                self.mines.append(labels[ind])
                labels.remove(labels[ind])

        for m in self.mines:
            m:Label
            col = m.grid_info()["column"]
            row = m.grid_info()["row"]

            for r in range(row-1,row+2):
                for c in range(col-1,col+2):
                    if c == col and r == row:continue
                    try:
                        lbl = [i for i in self.grid_slaves(row=r,column=c) if isinstance(i,Label)][0]
                        lbl.configure(text = f"{1 if lbl.cget("text") =="   " else int(lbl.cget("text"))+1}")
                    except:pass

main_window = MainFrame()
main_window.mainloop()
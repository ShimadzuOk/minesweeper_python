import random,time,threading
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
        self.timer_status = None
        self.current_timer_sec = 0
        self.current_timer_min = 0
        self.current_timer_hour = 0
        self.clock = StringVar(value="0:00:00")

        self.lbl1 = Label(self, text="Cells number: ")
        self.lblx = Label(self, text="x")
        self.lbl2 = Label(self, text="Mine number: ")
        self.lbl_timer = Label(self, textvariable= self.clock)
        self.action_btn = Button(self, text="Draw cells", command= self.master_w.result_frame.draw_cells)
        self.cells_width_entry = Entry(self,width=3)
        self.cells_height_entry = Entry(self,width=3)
        self.mine_number_entry = Entry(self)
        self.gm_over = Label(self,text="GAME OVER")
        self.win = Label(self,text="YOU WIN!")

        self.lbl1.grid(row=0,column=0,sticky=EW)
        self.lbl2.grid(row=1,column=0,sticky=EW)
        self.lblx.grid(row=0,column=2)
        self.lbl_timer.grid(row=2,column=0,columnspan=5)
        self.cells_width_entry.grid(row=0,column=1,sticky=EW)
        self.cells_height_entry.grid(row=0,column=3,sticky=EW)
        self.mine_number_entry.grid(row=1,column=1,columnspan=3 ,sticky=EW)
        self.action_btn.grid(row=0,column=4,rowspan=2,sticky=NSEW)

    def timer(self):
        self.current_timer_sec = -1
        self.current_timer_min = 0
        self.current_timer_hour = 0
        self.clock.set(f"{self.current_timer_hour}:{self.current_timer_min:02}:{self.current_timer_sec:02}")
        self.timer_status = None
        while self.timer_status != "STOP":
            if self.current_timer_sec == 59: 
                self.current_timer_sec = 0
                if self.current_timer_min == 59:
                    self.current_timer_min = 0
                    self.current_timer_hour += 1
                else: self.current_timer_min += 1
            else:self.current_timer_sec += 1
            self.clock.set(f"{self.current_timer_hour}:{self.current_timer_min:02}:{self.current_timer_sec:02}")
            time.sleep(1)

class MineField(Frame):
    def __init__(self,master_w,r,c):
        super().__init__(master= master_w)
        self.master = master_w
        self.lbl = Label(self,text="   ",width=3,bg="lightgray",bd=1,relief=GROOVE)
        self.btn = Button(self, text = "   ",command= self.ch_button)
        self.row = r
        self.column = c
        self.cover = True
        self.neighbors = []
        self.flagged = False
        self.mine = False

        self.rowconfigure(0,weight=1)
        self.columnconfigure(0,weight=1)
        self.lbl.grid(row=0,column=0,sticky=NSEW,padx=5.5, pady=6.5)
        self.btn.grid(row=0,column=0,sticky=NSEW, padx=3, pady=3)
        self.btn.bind("<Button-3>",lambda event: self.flag(event))

    def flag(self,event:Event):
        if self.btn.cget("text") == "   ": 
            self.flagged = True
            self.btn.config(text="⚑",state=DISABLED)
        else: 
            self.btn.config(text="   ",state=NORMAL)
            self.flagged = False

    def  ch_button(self):
        self.btn.grid_forget()
        self.cover = False

        if self.lbl.cget("text") == "   ":
            self.blank_zone(self.neighbors)

        if self.mine == True:
            self.master.loss()
            self.lbl.configure(text="\U0001F4A5",bg = "#ff6f00")

        self.master.check_win()


    def blank_zone(self,neighbors: list):
        for fl in neighbors:
            if not fl.mine and fl.cover:
                fl.btn.grid_forget()
                fl.cover = False
                if fl.lbl.cget("text") == "   ":
                    self.blank_zone(fl.neighbors)

class ResultFrame(Frame):
    def __init__(self, master_w:MainFrame):
        super().__init__(master = master_w,padx=5.5, pady=5.5)
        self.master_w = master_w
        self.fields = []
        self.mines = []
        self.previous_grid = []

    def loss(self):
        for fl in self.fields:
            if fl.cover: fl.btn.grid_forget()
            if fl.mine and fl.flagged: fl.lbl.config(bg="green")
            elif not fl.mine and fl.flagged: fl.lbl.config(bg="yellow")
            elif fl.mine and not fl.flagged: fl.lbl.config(bg="red")
        self.master_w.controls_frame.timer_status = "STOP"
        self.master_w.controls_frame.gm_over.grid(row=3,column=0,columnspan=5,sticky=NSEW)

    def check_win(self):
        mines = [fl for fl in self.fields if fl.mine]
        uncovered = [fl for fl in self.fields if not fl.cover]
        if len(self.fields) - len(uncovered) == len(mines):
            for fl in self.fields: 
                if fl.cover: fl.btn.grid_forget()
                if fl.mine: fl.lbl.config(bg="green")
            self.master_w.controls_frame.timer_status = "STOP"
            self.master_w.controls_frame.win.grid(row=3,column=0,columnspan=5,sticky=NSEW)

    def draw_cells(self):
        # Reset
        self.fields = []
        self.master_w.controls_frame.timer_status = "STOP"
        self.master_w.controls_frame.gm_over.grid_forget()
        self.master_w.controls_frame.win.grid_forget()
        [i.grid_forget() for i in self.grid_slaves()]
        if self.previous_grid:
            for i in range(self.previous_grid[0]):
                self.columnconfigure(i, weight=0)
            for j in range(self.previous_grid[1]):
                self.rowconfigure(j, weight=0)
        
        # Get cells number
        cells_w = int(self.master_w.controls_frame.cells_width_entry.get())
        cells_h = int(self.master_w.controls_frame.cells_height_entry.get())
        mine_n = int(self.master_w.controls_frame.mine_number_entry.get())
        self.previous_grid = [cells_w,cells_h]
        
        # Draw
        for c in range(cells_w):
            self.columnconfigure(c, weight=1)
            for r in range(cells_h):
                self.rowconfigure(r, weight=1)
                field = MineField(self,r,c)
                self.fields.append(field)
                field.grid(row=r,column=c,sticky=NSEW)

        #Mine
        fields = self.fields.copy()
        for m in range(mine_n):
            if fields:
                ind = random.randint(0,len(fields)-1)
                fields[ind].mine = True
                fields[ind].lbl.configure(text = "\U0001F4A3")
                fields.remove(fields[ind])

        for field in self.fields:
            for n_field in self.fields:
                if n_field.row in range(field.row - 1,field.row + 2) and n_field.column in range(field.column - 1,field.column + 2):
                    if n_field.row == field.row and n_field.column == field.column: continue
                    field.neighbors.append(n_field)
                    
            [i.lbl.configure(text = f"{1 if i.lbl.cget("text") =="   " else int(i.lbl.cget("text"))+1}") 
             if not i.lbl.cget("text") == "\U0001F4A3" else i 
             for i in field.neighbors 
             if field.mine == True]
        
        threading.Thread(target=self.master_w.controls_frame.timer,daemon=True).start()
        self.master_w.after(600)

main_window = MainFrame()
main_window.mainloop()
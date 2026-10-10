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
        time.sleep(1)
        self.current_timer_sec = 0
        self.current_timer_min = 0
        self.current_timer_hour = 0
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
        self.timer_status = None
            




class ResultFrame(Frame):
    def __init__(self, master_w:MainFrame):
        super().__init__(master = master_w)
        self.master_w = master_w
        self.mines = []
        self.btns = []
        self.previous_grid = []

    def flag(self,event:Event):
        btn = event.widget
        if btn.cget("text") == "   ": btn.config(text="⚑",state=DISABLED)
        else: btn.config(text="   ",state=NORMAL)
        

    def  ch_button(self,col,row):
        btn = [i for i in self.grid_slaves(column=col, row=row) if isinstance(i,Button)][0]
        btn.grid_forget()

        if [lbl for lbl in self.grid_slaves(row=row,column=col) if isinstance(lbl,Label) and lbl.cget("text") == "   "]: self.blank_zone(col,row)

        if [lbl for lbl in self.grid_slaves(row=row,column=col) if lbl.cget("text") == "\U0001F4A3"]:
            self.master_w.controls_frame.timer_status = "STOP"
            self.master_w.controls_frame.gm_over.grid(row=3,column=0,columnspan=5,sticky=NSEW)
            flaged_mines =[[i for i in self.grid_slaves(row= flm.grid_info()["row"],column=flm.grid_info()["column"]) if i.cget("text") == "\U0001F4A3"][0]
                            for flm in 
                            [fl for fl in self.grid_slaves() if fl.cget("text") == "⚑"]]
            [mines.configure(bg="red") if mines not in flaged_mines else mines.configure(bg="green") for mines in self.mines]
            [btn.grid_forget() for btn in self.btns]
            self.grid_slaves(column=col, row=row)[0].configure(text="\U0001F4A5",bg = "#ff6f00")
    
        if len([i for i in self.grid_slaves() if isinstance(i,Button)]) == len(self.mines):
            self.master_w.controls_frame.timer_status = "STOP"
            self.master_w.controls_frame.win.grid(row=3,column=0,columnspan=5,sticky=NSEW)
            [mines.configure(bg="green") for mines in self.mines]
            [btn.grid_forget() for btn in self.btns]

    def blank_zone(self,col,row):
        area = []

        for r in range(row-1,row+2):
            for c in range(col-1,col+2):
                if c == col and r == row:continue
                try: area.append([btn for btn in self.grid_slaves(row=r,column=c) if isinstance(btn,Button) and btn.cget("text") != "⚑"][0])
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
        for i in range(cells_w):
            self.columnconfigure(i, weight=1)

            for j in range(cells_h):
                self.rowconfigure(j, weight=1)

                lbl = Label(self,text="   ")
                lbl.grid(column=i, row=j, sticky=(N,S,W,E), padx=5.5, pady=5.5)

                btn = Button(self, text = "   ", command=lambda col=i, row=j: self.ch_button(col,row))
                btn.bind("<Button-3>",lambda event: self.flag(event))
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

        threading.Thread(target=self.master_w.controls_frame.timer,daemon=True).start()


main_window = MainFrame()
main_window.mainloop()
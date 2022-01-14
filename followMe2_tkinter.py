# -*- coding: utf-8 -*-
"""
Created on Fri Jan 14 11:54:52 2022

@author: Jungle
"""
import tkinter as tk
import tkinter.filedialog
import pysrt as srt

def window():
    global frameShow
    win = tk.Tk()
    win.geometry("860x360")
    win.title("FollowME")

    # Create Menu
    filemenu = tk.Menu(win)
    win.config(menu = filemenu)
        
    # Add Add srt menu
    add_srt_menu = tk.Menu(filemenu, tearoff=0)
    add_srt_menu.add_command(label = '打開檔案', command = add_srt)
    filemenu.add_cascade(label = "檔案", menu = add_srt_menu)
    filemenu.add_cascade(label = "說明")    
    
    # 字幕顯示區
    #labelwords = tk.Label(win, text="") #空白列
    frameTool  = tk.Frame(win, 
                         width = 860, 
                         height = 30, 
                         relief="ridge",
                         borderwidth = 1)  
    frameShow = tk.Frame(win, 
                         width = 860, 
                         height = 300)
    # Create Status Bar
    status_bar = tk.Label(win,text='', bd=1, relief="ridge", anchor="e")

    frameTool.pack()  
    frameShow.pack()
    status_bar.pack(fill="x", side="bottom", ipady=2)

    Subtitle(0)

    win.mainloop()

class Subtitle():
    global frameShow
    def __init__(self, row):
        self.row = row
        self.pagesize = 6
        self.index = []
        self.empty = []
        self.duration = []
        self.play_btn= []
        self.subEng = []
        self.subCht = []
        for row in range(self.pagesize + 1):
            if row == 0:
                # table title
                tt_idx_lbl = tk.Label(frameShow, 
                                      text = "#",
                                      width = 5,
                                      bg="silver",
                                      font = ("Calibri",12))
                tt_dra_lbl = tk.Label(frameShow, 
                                      text = "duration",
                                      width = 15,
                                      font = ("Calibri",12))
                tt_play_btn = tk.Button(frameShow,
                                       text = "|＞", 
                                       width=3,
                                       font=("新細明體",10),
                                       state=tk.DISABLED)
                tt_sub_lbl = tk.Label(frameShow, 
                                  text = "subtitle",
                                  fg = "white",
                                  bg = "silver",
                                  width = 82,
                                  font = ("Calibri",12))
                tt_idx_lbl.grid(row = row, column = 0)
                tt_dra_lbl.grid(row = row, column = 1)
                tt_play_btn.grid(row = row, column = 2)
                tt_sub_lbl.grid(row = row, column = 3)
            # elif row == 1:
            else:
                print("%d" % row)
                self.index.append(tk.Label(frameShow, 
                                           text = '%d' % row, 
                                           width = 5, 
                                           font = ("Calibri",12)))
                self.play_btn.append(tk.Button(frameShow, 
                                                text = "|＞", 
                                                width = 3, 
                                                font = ("新細明體",10),
                                                state=tk.DISABLED))
                self.subEng.append(tk.Label(frameShow, 
                                            text="", 
                                            font=("Calibri",12)))
                self.subCht.append(tk.Label(frameShow, 
                                            text="", 
                                            font=("Calibri",10)))
                
                self.index[row-1].grid(row = row*2-1, column = 0, rowspan = 2)
                self.play_btn[row-1].grid(row = row*2-1, column = 2, sticky="w")
                self.subEng[row-1].grid(row = row*2-1, column = 3, sticky="w")
                self.subCht[row-1].grid(row = row*2, column = 3, sticky="w")  
            
    
# Add Srt file Function
def add_srt():
    global subs,datasize,totpage,totfield,song
    file = tkinter.filedialog.askopenfilename(initialdir = ".", 
                                              title = "選擇檔案", 
                                              filetypes =(("Subtitle Files","*.srt"),))
    song = file.replace(".srt",".mp3") # 為了找同檔名的mp3檔
    subs = srt.open(file, encoding = "utf-8")

    
if __name__ == '__main__':
    window()

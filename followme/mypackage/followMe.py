# -*- coding: utf-8 -*-
"""
Created on Fri Jan 14 11:54:52 2022

@author: Jungle
"""
import base64
from icon import img
import os
import tkinter as tk
import tkinter.filedialog
import pysrt as srt
import math
import pygame as pyg
import threading

def window():
    global frameShow, subtitles, labelPage
    win = tk.Tk()
    win.geometry("860x380")
    #win.iconbitmap("followme.ico")
    tmp = open("tmp.ico","wb+")
    tmp.write(base64.b64decode(img))
    tmp.close()
    win.iconbitmap("tmp.ico")
    os.remove("tmp.ico")
    win.title("FollowME")

    # Initialze Pygame Mixer
    pyg.mixer.init()

    # Create Menu
    filemenu = tk.Menu(win)
    win.config(menu = filemenu)
        
    # Add Add srt menu
    add_srt_menu = tk.Menu(filemenu, tearoff=0)
    add_srt_menu.add_command(label = '打開檔案', command = add_srt)
    add_srt_menu.add_command(label = '離開程式', command = win.destroy)
    filemenu.add_cascade(label = "檔案", menu = add_srt_menu)
    filemenu.add_cascade(label = "說明")    

    
    
    # 字幕顯示區
    frameToolbar  = tk.Frame(win, 
                         #width = 860, 
                         #height = 30, 
                         relief="raised",
                         borderwidth = 2)  
    frameShow = tk.Frame(win, 
                         width = 860, 
                         height = 300)
    
    # Toolbar
    btnFirst = tk.Button(frameToolbar, text="|<", width=3)
    btnPrev = tk.Button(frameToolbar, text="<", width=3)
    btnNext = tk.Button(frameToolbar, text=">", width=3)
    btnBottom = tk.Button(frameToolbar, text=">|", width=3)
    btnFirst.grid(row=0, column=0, padx=2, pady=2)
    btnPrev.grid(row=0, column=1, padx=2, pady=2)
    btnNext.grid(row=0, column=2, padx=2, pady=2)        
    btnBottom.grid(row=0, column=3, padx=2, pady=2) 
    
    # Create Status Bar
    frameStatusbar = tk.Frame(win, 
                         height = 20, 
                         relief="raised",
                         borderwidth = 2) 

    labelPage = tk.Label(frameStatusbar, text="")

    frameToolbar.pack(side = "top", fill = "x")  
    frameShow.pack()
    frameStatusbar.pack(fill="x", side="bottom", ipady=2)
    labelPage.pack(anchor="w")

    subtitles = Subtitle(6)
    btnFirst.config(command = subtitles.First)
    btnPrev.config(command = subtitles.Prev)
    btnNext.config(command = subtitles.Next)
    btnBottom.config(command = subtitles.Bottom)
    
    win.mainloop()

class Subtitle():
    global frameShow, labelPage
    def __init__(self, pagesize):
        self.row = 0
        self.start = 0
        self.page = 0
        self.datasize = 0;  #資料筆數
        self.pagesize = 6
        self.totpage = 0
        self.totfield = 0
        self.subs = 0
        self.song = 0
        self.tt_play_btn = 0
        self.index = []
        self.empty = []
        self.duration = []
        self.play_btn= []
        self.subEng = []
        self.subCht = []
        self.subStart = []
        self.firstPlay = 0
        self.stopTimer = 0
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
                self.tt_play_btn = tk.Button(frameShow,
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
                self.tt_play_btn.grid(row = row, column = 2)
                tt_sub_lbl.grid(row = row, column = 3)
            else:
                #print("%d" % row)
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
            
    def load_srt(self, subs, song):
        self.subs = subs
        #first = self.subs[0]
        #print(first)
        self.datasize=len(subs) #資料筆數
        self.totpage=math.ceil(self.datasize/self.pagesize) #總頁數
        self.totfield=self.pagesize*self.totpage #總欄位數  
        self.__set_song(song)
        self.tt_play_btn.configure(state=tk.NORMAL, command=self.play)
        
    def refresh_page(self):
        row = 1
        start = self.page * self.pagesize
        for i in range(0, self.totfield):
            if i >= start and i < start + self.pagesize:
                #print("i=%d" % i)
                self.duration.append(tk.Label(frameShow,
                                              #text = subs[i].duration,
                                              font=("Calibri",12)))
                if i < self.datasize:
                    self.index[i%6].config(text = self.subs[i].index)
                    self.duration[i%6].config(
                        text = self.__calc_seconds(self.subs[i].duration.minutes,
                                                   self.subs[i].duration.seconds,
                                                   self.subs[i].duration.milliseconds))
                    self.subEng[i%6].config(text = self.subs[i].text)
                    sta = self.__calc_seconds(self.subs[i].start.minutes,
                                                self.subs[i].start.seconds,
                                                self.subs[i].start.milliseconds)
                    self.setAB(self.play_btn[i%6], sta, float(self.duration[i%6]['text']))
                else:
                    self.index[i%6].config(text = "")
                    self.duration[i%6].config(text = "")
                    self.subEng[i%6].config(text = "")
                    self.play_btn[i%6].configure(state=tk.DISABLED)
                    
                self.duration[i%6].grid(row = row, column = 1, rowspan = 2)
                self.subEng[i%6].grid(row = row, column = 3, sticky="w")
                row+=2
                
        labelPage.configure(text = str(self.page+1) + "/" + str(self.totpage))
        
        
    def __calc_seconds(self, min, sec, mili):
        return round(min*60+sec+mili/1000, 2)
    
    def First(self):  # 首頁
        self.page = 0
        self.refresh_page()
     
    def Prev(self):  #上一頁
        if self.page > 0:
            self.page -=1
            self.refresh_page()

    def Next(self): #下一頁
        if self.page < self.totpage-1:
            self.page += 1
            self.refresh_page()
        
    def Bottom(self): #最後頁
        self.page=self.totpage-1
        self.refresh_page()
        
    def __set_song(self, song):
        self.song = song
     
    # Play and pause selected srt's mp3
    def play(self):
        if(self.tt_play_btn['text'] == "|＞"):
            if self.firstPlay == 0:
                pyg.mixer.music.load(song)
                pyg.mixer.music.play(loops=0)
            else:
                pyg.mixer.music.unpause()
            self.tt_play_btn['text'] = ("| |")
        else:
            self.tt_play_btn['text'] = ("|＞")
            pyg.mixer.music.pause()
        self.firstPlay+=1
    
    def setAB(self, btn, start, duration):
        btn.configure(command = lambda:self.playAB(start, duration), state=tk.NORMAL)

    def playTest(self, start, duration):
        pyg.mixer.music.unload()
        pyg.mixer.music.load(self.song)
        pyg.mixer.music.play(loops=0, start = start)
        # print("helloworld %f - %f" % (start, duration))

    def playAB(self, start, duration):
        self.playTest(start, duration)
        
        if self.stopTimer:
            self.stopTimer.cancel()
        self.stopTimer = threading.Timer(duration, self.stop)
        self.stopTimer.start()
        
    def stop(self):
        pyg.mixer.music.stop()
        #print("stop")
        
# Add Srt file Function
def add_srt():
    global subtitles, song, totpagevar
    file = tkinter.filedialog.askopenfilename(initialdir = ".", 
                                              title = "選擇檔案", 
                                              filetypes =(("Subtitle Files","*.srt"),))
    song = file.replace(".srt",".mp3") # 為了找同檔名的mp3檔
    subs = srt.open(file, encoding = "utf-8")

    subtitles.load_srt(subs, song)
    subtitles.refresh_page()
    
if __name__ == '__main__':
    window()

# -*- coding: utf-8 -*-
"""
Created on Fri Jan 14 11:54:52 2022

@author: Jungle
"""
import base64
from icon import img
import os
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox
import tkinter.filedialog
import tkinter.simpledialog
import pysrt as srt
from math import ceil
import pygame as pyg
import threading
# from pytube import YouTube
# from moviepy import editor as mv
from os import remove
import asstosrt

global song

songStatus = {
    'INIT' : 0,
    'PLAYING' : 1,
    'PAUSE' : 2
}

subStatus = {
    'NONE' : 0,
    'HIDEALL' : 1,
    'SHOWALL' : 2,
    'SHOWAWORD' : 4
}

def window():
    global win, frameShow, subtitles, labelPage, toolbar
    pageSize = 6
    win = tk.Tk()
    if pageSize == 6:
        win.geometry("1000x460")
    elif pageSize == 7:
        win.geometry("1000x515")
    win.resizable(width = False, height = False)
    #win.iconbitmap("followme.ico")
    tmp = open("tmp.ico","wb+")
    tmp.write(base64.b64decode(img))
    tmp.close()
    win.iconbitmap("tmp.ico")
    remove("tmp.ico")
    win.title("Caption Player")
    win.protocol("WM_DELETE_WINDOW", close_window)

    # Initialze Pygame Mixer
    pyg.mixer.init()

    # 字幕顯示區
    frameToolbar  = tk.Frame(win, 
                         #width = 860, 
                         #height = 30, 
                         relief="raised",
                         borderwidth = 2)  
    frameShow = tk.Frame(win, 
                         width = 1000)
                         #height = 400)
    # Create Status Bar
    frameStatusbar = tk.Frame(win, 
                         height = 20, 
                         relief="raised",
                         borderwidth = 2) 
    
    # tool bar
    toolbar = Toolbar(frameToolbar)
    # main frame
    subtitles = Subtitle(pageSize)
    # status bar
    labelPage = tk.Label(frameStatusbar, text="")
    
    toolbar.setSubsCmd(subtitles)
    #toolbar.setPageBtnEn()

    frameToolbar.pack(side = "top", fill = "x")  
    frameShow.pack()
    frameStatusbar.pack(fill="x", side="bottom", ipady=2)
    labelPage.pack(anchor="w")
    
    # Create Menu
    filemenu = tk.Menu(win)
    win.config(menu = filemenu)
        
    # Add Add srt menu
    add_srt_menu = tk.Menu(filemenu, tearoff = 0)
    readme_menu = tk.Menu(filemenu, tearoff = 0)
    #add_srt_menu.add_command(label = '開啟檔案...', command = add_srt)
    add_srt_menu.add_command(label = '開啟字幕...', command = lambda:add_srt(toolbar))
    # add_srt_menu.add_command(label = '開啟連接...', command = open_yt)
    add_srt_menu.add_command(label = '離開程式', command = close_window)
    readme_menu.add_command(label = '資訊', command = readme)
    filemenu.add_cascade(label = "檔案", menu = add_srt_menu)
    filemenu.add_cascade(label = "說明", menu = readme_menu)        
    
    win.mainloop()
    
class Toolbar():
    def __init__(self, frameToolbar):
        self.btnFirst = 0
        self.btnPrev = 0
        self.btnNext = 0
        self.btnBottom = 0
        self.btnGPlay = 0
        self.pageList = []
        # Toolbar
        self.btnFirst = tk.Button(frameToolbar, text="|<", width=3, state=tk.DISABLED)
        self.btnPrev = tk.Button(frameToolbar, text="<", width=3, state=tk.DISABLED)
        self.btnNext = tk.Button(frameToolbar, text=">", width=3, state=tk.DISABLED)
        self.btnBottom = tk.Button(frameToolbar, text=">|", width=3, state=tk.DISABLED)
        self.btnGPlay = tk.Button(frameToolbar, text = "▶", 
                             width=3, 
                             font=("新細明體",12), 
                             state=tk.DISABLED)
        self.btnEng = tk.Button(frameToolbar, text="英", width=3, state=tk.DISABLED)
        self.btnCht = tk.Button(frameToolbar, text="中", width=3, state=tk.DISABLED)
        self.cbb = ttk.Combobox(frameToolbar, width = 6)
        # self.cbbRow = ttk.Combobox(frameToolbar, width = 8)
        self.lbl1 = tk.Label(frameToolbar, text=" ", width=3)
        self.btn1 = tk.Button(frameToolbar, text="讀", width=3, state=tk.DISABLED)
        self.btn2 = tk.Button(frameToolbar, text="寫", width=3, state=tk.DISABLED)
        self.btn3 = tk.Button(frameToolbar, text="憶", width=3, state=tk.DISABLED)
        self.btn4 = tk.Button(frameToolbar, text="說", width=3, state=tk.DISABLED)
        self.btn5 = tk.Button(frameToolbar, text="聽", width=3, state=tk.DISABLED)
        self.btn6 = tk.Button(frameToolbar, text="複", width=3, state=tk.DISABLED)
        self.btnC = tk.Button(frameToolbar, text="清", width=3, state=tk.DISABLED)
        self.btnFirst.grid(row=0, column=0, padx=2, pady=2)
        self.btnPrev.grid(row=0, column=1, padx=2, pady=2)
        self.btnNext.grid(row=0, column=2, padx=2, pady=2)
        self.btnBottom.grid(row=0, column=3, padx=2, pady=2) 
        self.btnGPlay.grid(row=0, column=4, padx=2, pady=2)
        self.btnEng.grid(row=0, column=5, padx=2, pady=2)
        self.btnCht.grid(row=0, column=6, padx=2, pady=2)
        self.cbb.grid(row=0, column=7, padx=2, pady=2)
        self.cbb.set("page")
        # self.cbbRow.grid(row=0, column=8, padx=2, pady=2)
        # self.cbbRow.set("一頁幾句")
        # self.cbbRow["values"] = ['6', '7', '8']
        self.lbl1.grid(row=0, column=9, padx=2, pady=2)
        self.btn1.grid(row=0, column=10, padx=2, pady=2)
        self.btn2.grid(row=0, column=11, padx=2, pady=2)
        self.btn3.grid(row=0, column=12, padx=2, pady=2)
        self.btn4.grid(row=0, column=13, padx=2, pady=2)
        self.btn5.grid(row=0, column=14, padx=2, pady=2)
        self.btn6.grid(row=0, column=15, padx=2, pady=2)
        self.btnC.grid(row=0, column=16, padx=2, pady=2)
        
    def setSubsCmd(self, subtitles):
        self.btnFirst.config(command = subtitles.First)
        self.btnPrev.config(command = subtitles.Prev)
        self.btnNext.config(command = subtitles.Next)
        self.btnBottom.config(command = subtitles.Bottom)
        
    def setSongCmd(self, song):
        self.btnGPlay.config(command = lambda:self.play(song), state=tk.NORMAL)
        
    def clrSongCmd(self):
            self.btnGPlay.config(state=tk.DISABLED)
        
    def setPageBtnEn(self):
        self.btnFirst.config(state=tk.NORMAL)
        self.btnPrev.config(state=tk.NORMAL)
        self.btnNext.config(state=tk.NORMAL)
        self.btnBottom.config(state=tk.NORMAL)

    def setPageBtnDis(self):
        self.btnFirst.config(state=tk.DISABLED)
        self.btnPrev.config(state=tk.DISABLED)
        self.btnNext.config(state=tk.DISABLED)
        self.btnBottom.config(state=tk.DISABLED)        

    def setComboBoxPage(self, subtitles):
        self.pageList.clear()
        # print(subtitles.totpage)
        for i in range(subtitles.totpage):
            self.pageList.append(str(i + 1))
        self.cbb["values"] = self.pageList
        self.cbb.bind("<<ComboboxSelected>>", subtitles.Assign)
        
    # def setComboBoxRow(self, subtitles):
        # self.cbbRow.bind("<<ComboboxSelected>>", subtitles.ChgRow)

    def changeSubsStatus(self, lesson, subs):
        if lesson == 1:
            subs.haveEng = subStatus['SHOWALL']
            subs.haveCht = subStatus['HIDEALL']
            self.btn1.config(bg = 'lightyellow') 
        elif lesson == 2:
            subs.haveEng = subStatus['HIDEALL']
            subs.haveCht = subStatus['SHOWALL']
            self.btn2.config(bg = 'lightyellow') 
        elif lesson == 3:
            subs.haveEng = subStatus['SHOWAWORD']
            subs.haveCht = subStatus['HIDEALL']
            self.btn3.config(bg = 'lightyellow')
        elif lesson == 4:
            subs.haveEng = subStatus['SHOWALL']
            subs.haveCht = subStatus['HIDEALL'] 
            self.btn4.config(bg = 'lightyellow')
        elif lesson == 5:
            subs.haveEng = subStatus['HIDEALL']
            subs.haveCht = subStatus['HIDEALL']   
            self.btn5.config(bg = 'lightyellow')
        elif lesson == 6:
            subs.haveEng = subStatus['HIDEALL']
            subs.haveCht = subStatus['SHOWALL']
            self.btn6.config(bg = 'lightyellow')             
        subs.refresh_page()            
            
    def clearLessonColor(self, subs):
        self.btn1.config(bg = 'SystemButtonFace')   
        self.btn2.config(bg = 'SystemButtonFace')  
        self.btn3.config(bg = 'SystemButtonFace')  
        self.btn4.config(bg = 'SystemButtonFace')  
        self.btn5.config(bg = 'SystemButtonFace')  
        self.btn6.config(bg = 'SystemButtonFace')  
        subs.haveEng = subStatus['HIDEALL']
        subs.haveCht = subStatus['HIDEALL'] 
        subs.refresh_page() 
            
    def setLessonFlow(self, subs):
        self.btn1.config(command = lambda:self.changeSubsStatus(1, subs), state=tk.NORMAL)
        self.btn2.config(command = lambda:self.changeSubsStatus(2, subs), state=tk.NORMAL)
        self.btn3.config(command = lambda:self.changeSubsStatus(3, subs), state=tk.NORMAL)
        self.btn4.config(command = lambda:self.changeSubsStatus(4, subs), state=tk.NORMAL)
        self.btn5.config(command = lambda:self.changeSubsStatus(5, subs), state=tk.NORMAL)
        self.btn6.config(command = lambda:self.changeSubsStatus(6, subs), state=tk.NORMAL)
        self.btnC.config(command = lambda:self.clearLessonColor(subs), state=tk.NORMAL)
        
    def setLangBtn(self, subtitles):
        #self.btnGPlay.config(command = subtitles.play, state=tk.NORMAL)
        if subtitles.haveEng == 1 or subtitles.haveEng == 2:
            self.btnEng.config(state=tk.NORMAL,
                                command = lambda:self.toggleEngBtn(subtitles))
        if subtitles.haveCht == 1 or subtitles.haveCht == 2:
            self.btnCht.config(state=tk.NORMAL, 
                               command = lambda:self.toggleChtBtn(subtitles))
    
    def toggleEngBtn(self, subs):
        if subs.haveEng == subStatus['SHOWALL']:
            subs.haveEng = subStatus['SHOWAWORD']
            self.btnEng.config(text='E1')
        elif subs.haveEng == subStatus['SHOWAWORD']:
            subs.haveEng = subStatus['HIDEALL']
            self.btnEng.config(text='英', fg = 'gray')
        elif subs.haveEng == subStatus['HIDEALL']:
            subs.haveEng = subStatus['SHOWALL']
            self.btnEng.config(text='英', fg = 'black')
        subs.refresh_page()
            
    def toggleChtBtn(self, subs):
        if subs.haveCht == subStatus['SHOWALL']:
            subs.haveCht = subStatus['HIDEALL']
            self.btnCht.config(relief='raise')
        elif subs.haveCht == subStatus['HIDEALL']:
            subs.haveCht = subStatus['SHOWALL']
            self.btnCht.config(relief='sunken')
        subs.refresh_page()
            

    def play(self, song):
        song.cancelTimer()
        if (self.btnGPlay['text'] == "▶"):
            if pyg.mixer.music.get_busy() == True:
                pyg.mixer.music.play(loops=0, start = 0)
                print("AB is playing, rewind g play")
            elif song.getSongStatus() == songStatus['INIT']:
                pyg.mixer.music.unload()
                pyg.mixer.music.load(song.getSong())
                pyg.mixer.music.play(loops=0)
                print("no song is playing, toolbar's play")    
            elif song.getSongStatus() == songStatus['PAUSE']:
                pyg.mixer.music.unpause()
                print("g play just pause, you press UNPAUSE")
            self.btnGPlay['text'] = ("| |")
            song.setSongStatus(songStatus['PLAYING'])
        else:
            if song.getSongStatus() == songStatus['INIT']:
                print("AB play is playing DONE, you press PAUSE")
                self.btnGPlay['text'] = "▶"
            #elif song.getSongStatus() == songStatus['PLAYING']:
            else:
                print("g play is now playing, you press PAUSE")
                self.btnGPlay['text'] = "▶"
                pyg.mixer.music.pause()
                song.setSongStatus(songStatus['PAUSE'])

class Subtitle():
    global frameShow, labelPage, song
    def __init__(self, pagesize):
        self.row = 0
        self.start = 0
        self.page = 0
        self.datasize = 0;  #資料筆數
        self.pagesize = pagesize
        self.totpage = 0
        self.totfield = 0
        self.subs = 0
        self.tt_play_btn = 0
        self.frameSentence = []
        self.index = []
        self.empty = []
        self.duration = []
        self.play_btn= []
        self.canvas = []
        self.subText = []
        self.subEng = [] # table
        self.subCht = []
        self.textEng = []
        self.textCht = []
        self.sep = []
        self.subStart = []
        self.haveEng = subStatus['NONE']
        self.haveCht = subStatus['NONE']
        for row in range(self.pagesize + 1):
            if row == 0:
                tt_empty = tk.Label(frameShow, text = "\t", font = ("Calibri", 1))
                self.frameSentence.append(tk.Frame(frameShow, 
                                     width = 1000, height = 40))
                # table title
                tt_idx_lbl = tk.Label(self.frameSentence[row], 
                                      text = "#",
                                      width = 5,
                                      bg="silver",
                                      font = ("Calibri",12))
                tt_dra_lbl = tk.Label(self.frameSentence[row], 
                                      text = "duration",
                                      width = 10,
                                      font = ("Calibri",12))
                self.tt_play_btn = tk.Button(self.frameSentence[row], 
                                        text = "►", 
                                        width=3,
                                        font = ("Calibri", 10),
                                        state=tk.DISABLED)
                tt_sub_lbl = tk.Label(self.frameSentence[row], 
                                  text = "subtitle",
                                  fg = "white",
                                  bg = "silver",
                                  width = 103,
                                  font = ("Calibri",12))
                tt_idx_lbl.grid(row = row, column = 0)
                tt_dra_lbl.grid(row = row, column = 1)
                self.tt_play_btn.grid(row = row, column = 2)
                tt_sub_lbl.grid(row = row, column = 3)
            else:
                self.frameSentence.append(tk.Frame(frameShow, 
                                     width = 1000, 
                                     height = 50, relief = 'ridge', borderwidth = 1))

                self.index.append(tk.Label(self.frameSentence[row], 
                                            text = '%d' % row, 
                                            width = 5, 
                                            font = ("Calibri",12)))
                self.duration.append(tk.Label(self.frameSentence[row],
                                              #text = subs[i].duration,
                                              width = 10,
                                              font=("Calibri",12)))
                self.play_btn.append(tk.Button(self.frameSentence[row], 
                                                text = "▷", 
                                                width = 3, 
                                                font = ("Calibri",10),
                                                state=tk.DISABLED))
                self.canvas.append(tk.Canvas(self.frameSentence[row], width = 840, height = 51))
                                             #relief = 'ridge', borderwidth = 1))
                
                self.subEng.append(self.canvas[row-1].create_text(3, 13, text = '\t\t\t\t\t', 
                                                                  font=("Calibri",14), 
                                                                  activefill = 'blue', 
                                                                  anchor = 'w'))
                self.subCht.append(self.canvas[row-1].create_text(3, 40, text='', 
                                                                  font=("Calibri",12),
                                                                  anchor = 'w'))
                self.sep.append(ttk.Separator(frameShow, orient = 'horizontal'))      
                
                self.index[row-1].grid(row = 0, column = 0, rowspan = 2)
                self.duration[row-1].grid(row = 0, column = 1, rowspan = 2)
                self.play_btn[row-1].grid(row = 0, column = 2, sticky="wn")
                self.canvas[row-1].grid(row = 0, column = 3, sticky="w", rowspan = 2)

            tt_empty.pack()
            self.frameSentence[row].pack()

    def is_contains_chinese(self, strs):
        for _char in strs:
            if '\u4e00' <= _char <= '\u9fa5':
                return True
            else: 
                continue
        return False
            
    def load_srt(self, subs, song):
        self.subs = subs
        self.textEng.clear()
        self.textCht.clear()
        for sub in subs:
            # print(sub.index)
            if "\n" in sub.text:
                subText = sub.text.split("\n")
                # print(subText[0])
                # print(subText[1])
                self.haveCht = subStatus['HIDEALL']
                if (self.is_contains_chinese(subText[0])):
                    self.textCht.append(subText[0])
                    self.textEng.append(subText[1])
                else:
                    self.textEng.append(subText[0])
                    self.textCht.append(subText[1])
            else:
                # print(sub.text)
                if self.is_contains_chinese(sub.text):
                    self.textCht.append(sub.text)
                    self.textEng.append("")
                else:
                    self.textEng.append(sub.text)
                    self.textCht.append("")
        self.haveEng = subStatus['SHOWALL']
        
        #first = self.subs[0]
        #print(first)
        self.datasize=len(subs) #資料筆數
        self.totpage=ceil(self.datasize/self.pagesize) #總頁數
        self.totfield=self.pagesize*self.totpage #總欄位數  
        #self.tt_play_btn.configure(state=tk.NORMAL, command=self.play)
        
    #def __eng_wipe_in(self, event, index):
    def __wipe_in(self, event, index):    
        delta, delay = 40, 0
        # print(index)
        
        if self.haveEng == subStatus['HIDEALL'] or self.haveEng == subStatus['SHOWAWORD']:
            subString = self.textEng[index]
            for i in range(len(subString) + 1):
                s = subString[:i]
                update_text = lambda s=s: self.canvas[index%self.pagesize].itemconfigure(self.subEng[i%self.pagesize], text=s)
                self.canvas[index%self.pagesize].after(delay, update_text)
                delay += delta  
        if self.haveCht == subStatus['HIDEALL'] or self.haveCht == subStatus['SHOWAWORD']:
            subString = self.textCht[index]
            for i in range(len(subString) + 1):
                s = subString[:i]
                update_text = lambda s=s: self.canvas[index%self.pagesize].itemconfigure(self.subCht[i%self.pagesize], text=s)
                self.canvas[index%self.pagesize].after(delay, update_text)
                delay += delta 
             
        
    def refresh_page(self):
        row = 1
        # print("refresh_page %d" % self.pagesize)
        start = self.page * self.pagesize
        for i in range(0, self.totfield):
            if i >= start and i < start + self.pagesize:
                #print("i=%d" % i)
                if i < self.datasize:
                    self.index[i%self.pagesize].config(text = self.subs[i].index)
                    self.duration[i%self.pagesize].config(
                        text = self.__calc_seconds(self.subs[i].duration.hours,
                                                   self.subs[i].duration.minutes,
                                                   self.subs[i].duration.seconds,
                                                   self.subs[i].duration.milliseconds))
                    
                    # english
                    if self.haveEng == subStatus['SHOWALL']:
                        self.canvas[i%self.pagesize].itemconfig(self.subEng[i%self.pagesize], text = self.textEng[i])
                    elif self.haveEng == subStatus['HIDEALL']:
                        self.canvas[i%self.pagesize].itemconfig(self.subEng[i%self.pagesize], text = "")
                    elif self.haveEng ==  subStatus['SHOWAWORD']:
                        self.canvas[i%self.pagesize].itemconfig(self.subEng[i%self.pagesize], text = self.textEng[i].split(' ')[0])
                        
                    # chinese    
                    if self.haveCht == subStatus['SHOWALL']:
                        self.canvas[i%self.pagesize].itemconfig(self.subCht[i%self.pagesize], text = self.textCht[i])
                    elif self.haveCht == subStatus['HIDEALL']:
                        self.canvas[i%self.pagesize].itemconfig(self.subCht[i%self.pagesize], text = "")
                        
                    # bind
                    self.canvas[i%self.pagesize].bind("<Button-1>", lambda event, arg=i: self.__wipe_in(event, arg))
                    # self.canvas[i%6].tag_bind(self.subEng[i%6], "<Button-1>", 
                    #                           lambda event, 
                    #                           arg=i: self.__eng_wipe_in(event, arg))
                    # self.canvas[i%6].tag_bind(self.subCht[i%6], "<Button-1>", 
                    #                           lambda event, 
                    #                           arg=i: self.__cht_wipe_in(event, arg))
                    
                    sta = self.__calc_seconds(self.subs[i].start.hours,
                                                self.subs[i].start.minutes,
                                                self.subs[i].start.seconds,
                                                self.subs[i].start.milliseconds)
                    self.setAB(self.play_btn[i%self.pagesize], sta, float(self.duration[i%self.pagesize]['text']))
                    
                    # install page play button
                    if i % self.pagesize == 0:
                        pageStart = sta
                    end = self.__calc_seconds(self.subs[i].end.hours,
                                                self.subs[i].end.minutes,
                                                self.subs[i].end.seconds,
                                                self.subs[i].end.milliseconds)
                    pageDuration = end - pageStart
                    #print(pageDuration)
                    self.tt_play_btn.configure(state=tk.NORMAL, 
                            command = lambda:self.setABTimer(pageStart, 
                                                             pageDuration))
                else:
                    self.index[i%self.pagesize].config(text = "")
                    self.duration[i%self.pagesize].config(text = "")
                    self.canvas[i%self.pagesize].itemconfig(self.subEng[i%self.pagesize], text = "")
                    self.canvas[i%self.pagesize].itemconfig(self.subCht[i%self.pagesize], text = "")
                    self.canvas[i%self.pagesize].unbind("<Button-1>")
                    self.play_btn[i%self.pagesize].configure(state=tk.DISABLED)
                row+=2
                
        labelPage.configure(text = str(self.page+1) + "/" + str(self.totpage))
        
        
    def __calc_seconds(self, hour, min, sec, mili):
        # print("%d-%d-%d-%f" % (hour, min, sec, mili))
        return round(hour*3600 + min*60+sec+mili/1000, 2)
    
    def First(self):  # 首頁
        self.page = 0
        self.refresh_page()
     
    def Prev(self):  #上一頁
        if self.page > 0:
            self.page -= 1
            self.refresh_page()

    def Next(self): #下一頁
        if self.page < self.totpage-1:
            self.page += 1
            self.refresh_page()
        
    def Bottom(self): #最後頁
        self.page=self.totpage-1
        self.refresh_page()
        
    def Assign(self, event):
        page = event.widget.get()
        self.page = int(page) - 1
        self.refresh_page()
     
    def ChgRow(self, event): 
        pass
        # self.pagesize =  int(event.widget.get())
        # print(self.pagesize)
        # window()
     
    # Play and pause selected srt's mp3
    def play(self):
        pass
    
    # set AB play button
    def setAB(self, btn, start, duration):
        btn.configure(command = lambda:self.setABTimer(start, duration), state=tk.NORMAL)

    def playAB(self, start, duration):
        pyg.mixer.music.unload()
        pyg.mixer.music.load(song.getSong())
        pyg.mixer.music.play(loops=0, start = start)
        #print("helloworld %f - %f" % (start, duration))
        song.setSongStatus(songStatus['PLAYING'])

    def setABTimer(self, start, duration):
        self.playAB(start, duration)
        song.cancelTimer()
        song.newSongTimer(duration)
     

class Song():
    def __init__(self, song):
        self.song = song
        self.playing = 0
        self.stopTimer = 0   
        
    def getSong(self):
        return self.song
    
    def setSongStatus(self, status):
        self.playing = status
        
    def getSongStatus(self):
        return self.playing
        
    def newSongTimer(self, duration):
        self.stopTimer = threading.Timer(duration, self.stop)
        self.stopTimer.start()

    # Play and pause selected srt's mp3
    def play(self):
        pyg.mixer.music.unload()
        pyg.mixer.music.load(self.song)
        pyg.mixer.music.play(loops=0)
        print("song's play")
            
    def stop(self):
        song.setSongStatus(songStatus['INIT'])
        pyg.mixer.music.stop()
        #print("song's stop")    
        
    def cancelTimer(self):
        if self.stopTimer:
            self.stopTimer.cancel()       
            
    def closeSong(self):
        pyg.mixer.music.unload()
        
# Add Srt file Function
def add_srt(toolbar):
    global subtitles, song
    file = tkinter.filedialog.askopenfilename(initialdir = ".", 
                                              title = "選擇字幕", 
                                              filetypes =(("Subtitle Files","*.srt"),
                                                          ("advanced substation alpha","*.ass"),))
    toolbar.clrSongCmd()
    
    if file:
        win.title("Caption Player - " + file)
        if ".srt" in file:
            songfile = file.replace(".srt",".mp3") # 為了找同檔名的mp3檔
            subs = srt.open(file, encoding = "utf-8")
        elif ".ass" in file:
            songfile = file.replace(".ass",".mp3") # 為了找同檔名的mp3檔
            ass_file = open(file, "r", encoding="utf-8")
            subs123 = asstosrt.convert(ass_file)
            f = open('temp.srt', 'w', encoding="utf-8")
            f.write(subs123)
            f.close()
            subs = srt.open('temp.srt', encoding = "utf-8")
        
        subtitles.load_srt(subs, songfile)
        song = Song(songfile)
        createObj(songfile)
    
def createObj(songfile):
    global subtitles, song
    subtitles.First()
    toolbar.setLangBtn(subtitles)
    toolbar.setComboBoxPage(subtitles)
    # toolbar.setComboBoxRow(subtitles)
    toolbar.setLessonFlow(subtitles)
        
    if os.path.isfile(songfile) == False:
        tkinter.messagebox.showwarning("warning", "沒有對應的mp3")
    else:
        toolbar.setPageBtnEn()
        toolbar.setSongCmd(song)
    
    
def readme():
    tkinter.messagebox.showinfo("About Caption Player", "Caption Player \nV0.4")


def close_window():
    global song
    print("close_window")
    if os.path.exists('temp.srt'):
        remove('temp.srt')
    try:
        song
    except NameError:
        pass
    else:
        if song.getSongStatus() == songStatus['PLAYING']:
            song.stop()
            song.closeSong()
    win.destroy()
    
def open_yt():
    ytAddr = tkinter.simpledialog.askstring(title = '請輸入位址', 
                                       prompt='輸入youtube網址\t\t\t\t\t\t\t\t')
    # if ytAddr:
    #     yt = YouTube(ytAddr)
    #     #print(yt.streams)
    #     #print(yt.captions)
    #     pathdir = '.'
    #     print("開始下載聲音檔")
        
    #     caption = yt.captions.get_by_language_code('a.en')
    #     if caption:
    #         srt = caption.generate_srt_captions()
    #         srtfile = open(yt.title + '.srt', 'w', encoding = 'UTF-8')
    #         srtfile.write(srt)
    #         srtfile.close()
        
    #     yt.streams.filter(subtype='mp4').first().download(pathdir)
    #     filename = yt.title + '.mp4'
    #     targetname = yt.title + '.mp3'
    #     video = mv.VideoFileClip(filename)
    #     video.audio.write_audiofile(targetname)
    #     video.close()
    #     if os.path.exists(filename):
    #         remove(filename)
    #     tk.messagebox.showinfo("info", "下載完成")

    
if __name__ == '__main__':
    window()

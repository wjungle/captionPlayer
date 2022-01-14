# -*- coding: utf-8 -*-
"""
Created on Tue Jan 11 15:55:53 2022

@author: Jungle
"""

import pysrt as srt
import tkinter as tk
import tkinter.filedialog
import pygame as pyg
import time
import threading
import math
win=tk.Tk()
win.geometry("500x300")
win.title("FollowME")

page,pagesize=0,6
totpage,totfield=0,0

# Initialze Pygame Mixer
pyg.mixer.init()

# Add Srt file Function
def add_srt():
    global btnPlayAll
    #pass
    global subs,datasize,totpage,totfield,song
    file = tkinter.filedialog.askopenfilename(initialdir=".",title="選擇檔案",filetypes=(("Subtitle Files","*.srt"),))
    song = file.replace(".srt",".mp3") # 為了找同檔名的mp3檔
    subs = srt.open(file, encoding="utf-8")

    datasize=len(subs) #資料筆數
    totpage=math.ceil(datasize/pagesize) #總頁數
    totfield=pagesize*totpage #總欄位數

    #print("轉換完畢!") 
    btnPlayAll['state'] = tk.NORMAL
    First()
    disp_play()

def First():  # 首頁
    global page
    page=0
    pagevar.set(page+1)
    disp_data()
 
def Prev():  #上一頁
    global page
    if page>0:
        page -=1
        pagevar.set(page+1)
        disp_data()     
       
def Next(): #下一頁
    global page
    global totpage
    if page<totpage-1:
        page +=1
        pagevar.set(page+1)
        disp_data()
        
    
def Bottom(): #最後頁
    global page
    global totpage
    page=totpage-1
    pagevar.set(page+1)
    disp_data() 

global firstPlay
firstPlay = 0
    
# Play and pause selected srt's mp3
def play():
    global song,btntext
    global firstPlay
    if(btntext.get() == "|＞"):
        if firstPlay == 0:
            pyg.mixer.music.load(song)
            pyg.mixer.music.play(loops=0)
        else:
            pyg.mixer.music.unpause()
        btntext.set("| |")
    else:
        btntext.set("|＞")
        pyg.mixer.music.pause()
    firstPlay+=1
    
def stop():
    pyg.mixer.music.stop()

def play_slice():
    global song
    first_start = subs[0].start
    slice_st=calc_seconds(first_start.minutes,first_start.seconds,first_start.milliseconds)
    slice_dr=calc_seconds(subs[0].duration.minutes,subs[0].duration.seconds,subs[0].duration.milliseconds)
    #print(slice_st)
    #print(slice_dr)
    pyg.mixer.music.load(song)
    pyg.mixer.music.play(loops=0)
    pyg.mixer.music.set_pos(slice_st)
    t=threading.Timer(slice_dr,stop)
    t.start()
        
def disp_hdr():
    sep1=tk.Label(frameShow, text="\t",fg="white",width="20",font=("Calibri",10))  
    label1 = tk.Label(frameShow, text="subtitle",fg="white",bg="gray",width=40,font=("Calibri",12))
    # label2 = tk.Label(frameShow, text="英",fg="white",bg="gray",width=3,font=("新細明體",10))
    # chiSub = tk.StringVar()
    # entryChi = tk.Entry(frameShow, textvariable=chiSub)
    sep1.grid(row=0,column=0,sticky="w")  # 加第一列空白，讓版面美觀些   
    label1.grid(row=1,column=0,sticky="w",padx=20)
    # label2.grid(row=2,column=1)
    # entryChi.grid(row=1,column=2)
    disp_one()

def disp_one():
    global btntext,btnPlayAll
    btntext = tk.StringVar()
    sep1=tk.Label(frameShow, text="\t",fg="white",width="20",font=("Calibri",10))
    btnPlayAll = tk.Button(framePlayBtn,textvariable=btntext,width=3,font=("新細明體",10),command=play,state=tk.DISABLED)
    btntext.set("|＞")    
    sep1.grid(row=0,column=0,sticky="E")  # 加第一列空白，讓版面美觀些   
    btnPlayAll.grid(row=0,column=0,sticky="E")
    
def disp_data():
    global subs      
    row=2
    start=page * pagesize
    for i in range(0,totfield):
        if i >= start and i < start + pagesize:
            if i<datasize:
                labelE = tk.Label(frameShow,text='{}'.format(subs[i].text),width=40,font=("Calibri",12),anchor="w")
            else:
                labelE = tk.Label(frameShow,text="",width=40,font=("Calibri",12),anchor="w")
            labelE.grid(row=row,column=0,sticky="w",padx=20)
            row+=1

def disp_play():
    btnPlay1 = tk.Button(framePlayBtn,text="|＞",width=3,font=("新細明體",10),command=play_slice)
    btnPlay2 = tk.Button(framePlayBtn,text="|＞",width=3,font=("新細明體",10))
    btnPlay3 = tk.Button(framePlayBtn,text="|＞",width=3,font=("新細明體",10))
    btnPlay4 = tk.Button(framePlayBtn,text="|＞",width=3,font=("新細明體",10))
    btnPlay5 = tk.Button(framePlayBtn,text="|＞",width=3,font=("新細明體",10))
    btnPlay6 = tk.Button(framePlayBtn,text="|＞",width=3,font=("新細明體",10))
    btnPlay1.grid(row=1,column=0,sticky="E")
    btnPlay2.grid(row=2,column=0,sticky="E")
    btnPlay3.grid(row=3,column=0,sticky="E")
    btnPlay4.grid(row=4,column=0,sticky="E")
    btnPlay5.grid(row=5,column=0,sticky="E")
    btnPlay6.grid(row=6,column=0,sticky="E") 
    # Call the disp_time function to get song length
    #disp_time()

def disp_time():
    # Grab Current Song Elapsed Time
    current_time = pyg.mixer.music.get_pos() / 1000
    # convert to time format
    converted_current_time = time.strftime('%M:%S', time.gmtime(current_time))
    # Output time to status bar
    status_bar.config(text=converted_current_time)
    # update time
    status_bar.after(1000,disp_time)

def calc_seconds(min, sec, mili):
    return min*60+sec+mili/1000

# Create Menu
filemenu = tk.Menu(win)
win.config(menu=filemenu)
    
# Add Add srt menu
add_srt_menu = tk.Menu(filemenu,tearoff=0)
add_srt_menu.add_command(label='打開檔案',command=add_srt)
filemenu.add_cascade(label="檔案", menu=add_srt_menu)
filemenu.add_cascade(label="說明")

# main frame includes 音樂播放按鈕 & 字幕顯示區
frameMain = tk.Frame(win)
frameMain.pack()

# 音樂播放按鈕顯示區
framePlayBtn = tk.Frame(frameMain)
framePlayBtn.pack(side="left")

# 字幕顯示區
frameShow = tk.Frame(frameMain)  
frameShow.pack()
labelwords = tk.Label(frameMain,text="") #空白列
labelwords.pack() 

# 筆記顯示區

# 頁數及其他資訊顯示區
framePage = tk.Frame(win)
framePage.pack()
pagevar = tk.IntVar()
labelPage = tk.Label(framePage,textvariable=str(pagevar))
labelPage.pack()

# 翻頁按鈕容器顯示區
frameCommand = tk.Frame(win)  
frameCommand.pack()  
btnFirst = tk.Button(frameCommand, text="第一頁", width=8,command=First)
btnPrev = tk.Button(frameCommand, text="上一頁", width=8,command=Prev)
btnNext = tk.Button(frameCommand, text="下一頁", width=8,command=Next)
btnBottom = tk.Button(frameCommand, text="最末頁", width=8,command=Bottom)
btnFirst.grid(row=0, column=0, padx=5, pady=5)
btnPrev.grid(row=0, column=1, padx=5, pady=5)
btnNext.grid(row=0, column=2, padx=5, pady=5)        
btnBottom.grid(row=0, column=3, padx=5, pady=5)   

# Create Status Bar
status_bar = tk.Label(win,text='',bd=1,relief="groove",anchor="e")
status_bar.pack(fill="x", side="bottom", ipady=2)

disp_hdr()
win.mainloop()
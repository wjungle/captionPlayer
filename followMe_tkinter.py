# -*- coding: utf-8 -*-
"""
Created on Tue Jan 11 15:55:53 2022

@author: Jungle
"""

import pysrt as srt
import tkinter as tk
import tkinter.filedialog
import pygame as pyg
import math
win=tk.Tk()
win.geometry("500x300")
win.title("FollowME")

page,pagesize=0,6
totpage,totfield=0,0
datas=list() # 記錄字幕文字

# Initialze Pygame Mixer
pyg.mixer.init()

# Add Srt file Function
def add_srt():
    #pass
    global datasize,totpage,totfield,song
    file = tkinter.filedialog.askopenfilename(initialdir=".",title="選擇檔案",filetypes=(("Subtitle Files","*.srt"),))
    song = file.replace(".srt",".mp3") # 為了找同檔名的mp3檔
    subs = srt.open(file, encoding="utf-8")
    datas.clear()
    for sub in subs:
        datas.append(sub.text)
        #print(sub.index, END=",")
        #print(sub.text)

    datasize=len(subs) #資料筆數
    totpage=math.ceil(datasize/pagesize) #總頁數
    totfield=pagesize*totpage #總欄位數

    # 剩下的格數用空白取代，以免殘留上一頁的文字
    for i in range(datasize,totfield):
        datas.append("")
    #print("轉換完畢!") 
    First()
    

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

global firstPlay,inited
firstPlay = 0
inited = 0
    
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
        
def disp_data():      
    global inited
    if inited == 0:
        disp_play()
        inited = 1
        
    sep1=tk.Label(frameShow, text="\t",fg="white",width="20",font=("Calibri",10))  
    label1 = tk.Label(frameShow, text="subtitle",fg="white",bg="gray",width=40,font=("Calibri",12))
    # label2 = tk.Label(frameShow, text="英",fg="white",bg="gray",width=3,font=("新細明體",10))
    # label3 = tk.Label(frameShow, text='{:30}'.format(datas[0]),width=30,font=("Calibri",10))
    # chiSub = tk.StringVar()
    # entryChi = tk.Entry(frameShow, textvariable=chiSub)
    sep1.grid(row=0,column=0,sticky="w")  # 加第一列空白，讓版面美觀些   
    label1.grid(row=1,column=0,sticky="w",padx=20)
    # label2.grid(row=2,column=1)
    # label3.grid(row=2,column=2)
    # entryChi.grid(row=1,column=2)
    
    row=2
    start=page * pagesize
    for i in range(0,totfield):
        if i >= start and i < start + pagesize:
            labelE = tk.Label(frameShow,text='{}'.format(datas[i]),width=40,font=("Calibri",12),anchor="w")
            labelE.grid(row=row,column=0,sticky="w",padx=20)
            row+=1
    # sn=0       
    # for sub in subs:
    #     if n >= start and n < start + pagesize:
    #         #chiSub = tk.StringVar()
    #         #labelC = tk.Entry(frameShow, textvariable=chiSub) 
    #         labelE = tk.Label(frameShow,text='{}'.format(sub.text),width=40,font=("Calibri",12),anchor="w")
    #         labelE.grid(row=row,column=0,sticky="w",padx=20)
    #         row+=1
    #     n+=1

        
    
    #labeltest = tk.Label(frameShow,text="this is label",fg="red",font=("新細明體",10))   
    #labeltest.pack() 

def disp_play():
    global btntext
    sep1=tk.Label(frameShow, text="\t",fg="white",width="20",font=("Calibri",10))
    btntext = tk.StringVar()
    btnPlayAll = tk.Button(framePlayBtn,textvariable=btntext,width=3,font=("新細明體",10),command=play)
    btntext.set("|＞")
    btnPlay1 = tk.Button(framePlayBtn,text="|＞",width=3,font=("新細明體",10))
    btnPlay2 = tk.Button(framePlayBtn,text="|＞",width=3,font=("新細明體",10))
    btnPlay3 = tk.Button(framePlayBtn,text="|＞",width=3,font=("新細明體",10))
    btnPlay4 = tk.Button(framePlayBtn,text="|＞",width=3,font=("新細明體",10))
    btnPlay5 = tk.Button(framePlayBtn,text="|＞",width=3,font=("新細明體",10))
    btnPlay6 = tk.Button(framePlayBtn,text="|＞",width=3,font=("新細明體",10))
    sep1.grid(row=0,column=0,sticky="E")  # 加第一列空白，讓版面美觀些   
    btnPlayAll.grid(row=0,column=0,sticky="E")
    btnPlay1.grid(row=1,column=0,sticky="E")
    btnPlay2.grid(row=2,column=0,sticky="E")
    btnPlay3.grid(row=3,column=0,sticky="E")
    btnPlay4.grid(row=4,column=0,sticky="E")
    btnPlay5.grid(row=5,column=0,sticky="E")
    btnPlay6.grid(row=6,column=0,sticky="E") 

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

#First()
win.mainloop()
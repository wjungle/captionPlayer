# -*- coding: utf-8 -*-
"""
Created on Tue Jan 11 15:55:53 2022

@author: Jungle
"""

import pysrt as srt
import tkinter as tk
import math
win=tk.Tk()
win.geometry("500x300")
win.title("FollowME")

page,pagesize=0,6
datas=list()

subs = srt.open('Clean Up Trash Song.srt', encoding="utf-8")
for sub in subs:
    #datas[int("sub.index", base=10)]=sub.text
    datas.append(sub.text)
    #print(sub.index)
    #print(sub.text)
    #print()

datasize=len(subs) #資料筆數
totpage=math.ceil(datasize/pagesize) #總頁數
totfield=pagesize*totpage

for i in range(datasize,totfield):
    datas.append("")
print("轉換完畢!") 

#for i in range(0,datasize):
#    print(datas[i])

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
    if page<totpage-1:
        page +=1
        #print(">%d" % page)
        pagevar.set(page+1)
        #clear_data()
        disp_data()
        
    
def Bottom(): #最後頁
    global page
    page=totpage-1
    pagevar.set(page+1)
    disp_data() 

def clear_data():
    for i in range(2, pagesize+2):
        labelE = tk.Label(frameShow,text="")
        labelE.grid(row=i,column=0,sticky="w",padx=60)

def disp_data():      
    sep1=tk.Label(frameShow, text="\t",fg="white",width="20",font=("新細明體",10))  
    # btnPlay = tk.Button(frameShow,text="|＞",width=3,font=("新細明體",10))
    label1 = tk.Label(frameShow, text="subtitle",fg="white",bg="gray",width=40,font=("Calibri",12))
    # label2 = tk.Label(frameShow, text="英",fg="white",bg="gray",width=3,font=("新細明體",10))
    # label3 = tk.Label(frameShow, text='{:30}'.format(datas[0]),width=30,font=("Calibri",10))
    # chiSub = tk.StringVar()
    # entryChi = tk.Entry(frameShow, textvariable=chiSub)
    sep1.grid(row=0,column=0,sticky="w")  # 加第一列空白，讓版面美觀些   
    # btnPlay.grid(row=2,column=0)
    label1.grid(row=1,column=0,sticky="w",padx=60)
    # label2.grid(row=2,column=1)
    # label3.grid(row=2,column=2)
    # entryChi.grid(row=1,column=2)
    
    row=2
    start=page * pagesize
    for i in range(0,totfield):
        if i >= start and i < start + pagesize:
            labelE = tk.Label(frameShow,text='{}'.format(datas[i]),width=40,font=("Calibri",12),anchor="w")
            labelE.grid(row=row,column=0,sticky="w",padx=60)
            row+=1
    # sn=0       
    # for sub in subs:
    #     if n >= start and n < start + pagesize:
    #         #chiSub = tk.StringVar()
    #         #labelC = tk.Entry(frameShow, textvariable=chiSub) 
    #         labelE = tk.Label(frameShow,text='{}'.format(sub.text),width=40,font=("Calibri",12),anchor="w")
    #         labelE.grid(row=row,column=0,sticky="w",padx=60)
    #         row+=1
    #     n+=1

        
    
    #labeltest = tk.Label(frameShow,text="this is label",fg="red",font=("新細明體",10))   
    #labeltest.pack() 
    

# 單字顯示區
frameShow = tk.Frame(win)  
frameShow.pack()
labelwords = tk.Label(win,text="") #空白列
labelwords.pack() 

framePage = tk.Frame(win)
framePage.pack()
pagevar = tk.IntVar()
labelPage = tk.Label(framePage,textvariable=str(pagevar))
labelPage.pack()

# 翻頁按鈕容器
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

First()
win.mainloop()
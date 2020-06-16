import tkinter 
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import simpledialog
from tkinter import filedialog as fd
import sqlite3 as sqltor
import random
import csv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import logging
import threading


conn=sqltor.connect('main.db')
cursor=conn.cursor()
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
#options.add_argument('--incognito')
options.add_argument('--headless')

#######################################################
def fulltrack():
    trknumber=trnumber.get()
    if trknumber=='':
        return messagebox.showerror('Error','Enter Tracking Number')
    else:
        try:
            destination_time=[]
            destination_status=[]
            origin_time=[]
            origin_status=[]
            driver=webdriver.Chrome('PATH TO DRIVER',options=options)
            driver.get('https://t.17track.net/en#nums='+trknumber)
            time.sleep(7)
            driver.find_element_by_xpath('/html/body/div[6]/div/div[5]/a[1]').click()
            print('--Forwarding')                    
            time.sleep(2)
            driver.find_element_by_xpath('//*[@id="tn-'+trknumber+'"]/div[2]/div[2]/div[2]/div/button').click()
            driver.find_element_by_xpath('//*[@id="yq-modal-translate"]/div/div/div[2]/div[1]/div/div/a[1]').click()
            time.sleep(2)
            origin=driver.find_element_by_xpath('//*[@id="tn-'+trknumber+'"]/div[1]/div[2]/div[1]/div[2]/div/span').text
            destination=driver.find_element_by_xpath('//*[@id="tn-'+trknumber+'"]/div[1]/div[2]/div[3]/div[2]/div/span').text
            status=driver.find_element_by_xpath('//*[@id="tn-'+trknumber+'"]/div[1]/div[1]/div/p[2]').text
            pstatus=driver.find_element_by_xpath('//*[@id="tn-'+trknumber+'"]/div[1]/div[3]/p').text
            try:  #destination status
                st1=driver.find_element_by_class_name('des-block')
                icv=1
                while True:
                    dt_time=st1.find_element_by_xpath('//*[@id="tn-'+trknumber+'"]/div[2]/div[1]/dl[2]/dd['+str(icv)+']/div/time').text
                    dt_sts=st1.find_element_by_xpath('//*[@id="tn-'+trknumber+'"]/div[2]/div[1]/dl[2]/dd['+str(icv)+']/div/p').text
                    destination_time.append(dt_time)
                    destination_status.append(dt_sts)
                    icv=icv+1
            except:
                pass
            try: #origin status
                st2=driver.find_element_by_class_name('ori-block')
                inc=1
                while True:
                    dt_time=st2.find_element_by_xpath('//*[@id="tn-'+trknumber+'"]/div[2]/div[1]/dl[1]/dd['+str(inc)+']/div/time').text
                    dt_sts=st2.find_element_by_xpath('//*[@id="tn-'+trknumber+'"]/div[2]/div[1]/dl[1]/dd['+str(inc)+']/div/p').text
                    origin_time.append(dt_time)
                    origin_status.append(dt_sts)
                    inc=inc+1
            except:
                pass
            track=Toplevel()
            track.geometry('900x600')
            track.title('Tracking'+trknumber)
            track.configure(bg='SpringGreen2')
            track.iconbitmap('new.ico')
            windowWidth = track.winfo_reqwidth()
            windowHeight = track.winfo_reqheight()
            positionRight = int(track.winfo_screenwidth()/4 - windowWidth/2)
            positionDown = int(track.winfo_screenheight()/4 - windowHeight/2)
            track.geometry("+{}+{}".format(positionRight, positionDown))
            Label(track,text='Tracking:'+trknumber,font=('Times',18,'bold'),bg='SpringGreen2').place(x=330,y=7)
            Label(track,text='Origin: '+origin,bg='SpringGreen2',font=('Helvetica','15')).place(x=230,y=60)
            Label(track,text='Destination: '+destination,font=('Helvetica','15'),bg='SpringGreen2').place(x=570,y=60)
            Label(track,text='Status: '+status,bg='SpringGreen2',font=('Helvetica','15')).place(x=400,y=90)
            Label(track,text='Present Status: '+pstatus,bg='burlywood1',font=('Helvetica','14')).place(x=2,y=130)
            if len(destination_status)>=1:
                main=[]
                totalstatus=destination_status+origin_status
                totaltime=destination_time+origin_time
                for i in range(len(totalstatus)):
                    main1=(totaltime[i],totalstatus[i])
                    main.append(main1)
                scroll1=ttk.Scrollbar(track)
                scroll1.place(x=850,y=300)
                tb1=ttk.Treeview(track,columns=(1,2,3,4),show='headings',selectmode='browse')
                tb1.place(x=10,y=200)
                tb1.heading(1,text="Date & Time")
                tb1.column(1,minwidth=15,width=150,stretch=NO)
                tb1.heading(2,text="Status")
                tb1.column(2,minwidth=15,width=900,stretch=NO)
                tb1.heading(3,text="")
                tb1.column(3,minwidth=15,width=700,stretch=NO)
                tb1.heading(4,text="")
                tb1.column(4,minwidth=15,width=700,stretch=NO)
                scroll1.config(command=tb1.yview)
                for i in main: #appending details(subdetails)
                   tb1.insert('','end',values=i)
            else:
                totalstatus=origin_status
                totaltime=origin_time
        except:
            return messagebox.showerror('Error','Could not track your package!')            

home=Tk()
home.geometry('900x600')
home.title('Home Page')
home.configure(bg='SpringGreen2')
#home.iconbitmap('new.ico')   #icon-can-be-found-in-folder
#window-loc
windowWidth = home.winfo_reqwidth()
windowHeight = home.winfo_reqheight()
positionRight = int(home.winfo_screenwidth()/4 - windowWidth/2)
positionDown = int(home.winfo_screenheight()/4 - windowHeight/2)
home.geometry("+{}+{}".format(positionRight, positionDown))
#----#----
Button(home,text='     ℹ️',height =1,width=3,fg='black',font=('Times','10','bold'),bg='burlywood1').place(x=7,y=7) #info
Button(home,text='⚙',height =1,width=3,fg='black',font=('Times','10','bold'),bg='burlywood1').place(x=850,y=7)  #settings
Label(home,text='SmoothTrack_1.1',font=('Times','30','bold'),bg='SpringGreen2').place(x=300,y=10)
Label(home,text='Track all your shipments in one place!',bg='SpringGreen2',font=('Helvetica', '12')).place(x=450,y=60)
Button(home,text='SignIn',height=2,width=10,font=('Helvetica','15'),borderwidth=5,bg='burlywood1').place(x=280,y=130)
Button(home,text='Register',height=2,width=10,font=('Helvetica','15'),borderwidth=5,bg='burlywood1').place(x=500,y=130)
Label(home,text='Enter your tracking number:',bg='SpringGreen2',font=('Times','15')).place(x=190,y=250)
trnumber=StringVar()
Entry(home,width=35,bd=5,textvariable=trnumber).place(x=420,y=253)
def trstart():
    x=threading.Thread(target=fulltrack)
    x.start()
Button(home,text='Track',height=1,width=4,font=('Helvetica','10'),borderwidth=5,bg='burlywood1',command=trstart).place(x=650,y=251)
home.mainloop()


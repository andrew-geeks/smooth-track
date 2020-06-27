import tkinter 
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import simpledialog
from tkinter import filedialog as fd
import sqlite3 as sqltor
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import threading
from PIL import ImageTk,Image
import pkg_resources.py2_warn


path='mainfiles/geckodriver.exe'
#dbpath=''

conn=sqltor.connect('mainfiles/main.db')
cursor=conn.cursor()
options = webdriver.FirefoxOptions()
#options.add_argument('--ignore-certificate-errors')
#options.add_argument('--incognito')
options.add_argument('-headless')
#options.add_argument("--disable-gpu")
#options.add_argument("window-size=1200,1100")
def raise_frame(frame):
    frame.tkraise()

############################################
main=Tk()
main.geometry('900x600')
main.title('SmoothTrack_3.0')
main.iconbitmap('mainfiles/new.ico')
windowWidth = main.winfo_reqwidth()
windowHeight = main.winfo_reqheight()
positionRight = int(main.winfo_screenwidth()/4 - windowWidth/2)
positionDown = int(main.winfo_screenheight()/4 - windowHeight/2)
main.geometry("+{}+{}".format(positionRight, positionDown))

home=Frame(main)
track=Frame(main)
info=Frame(main)
register=Frame(main)
signin=Frame(main)
accwindow=Frame(main)
add=Frame(main)
loading=Frame(main)
settings=Frame(main)
for frame in(home,track,info,register,signin,accwindow,add,loading,settings):
    frame.place(x=0, y=0, width=100000, height=200000)



def Home(): #home_page
        global trnumber
        raise_frame(home)
        #home.configure(bg='SpringGreen2')
        img = Image.open('mainfiles/bg.png') 
        img = img.resize((900,600),Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)
        panel=Label(home,image=img)
        panel.image = img
        panel.place(x=0,y=0)       
        Button(home,text='     ℹ️',height =1,width=3,fg='black',font=('Times','10','bold'),bg='burlywood1',command=infow).place(x=7,y=7) #info
        Button(home,text='⚙',height =1,width=3,fg='black',font=('Times','10','bold'),bg='burlywood1',command=soon).place(x=850,y=7)  #settings
        Label(home,text='SmoothTrack_3.0',font=('Times','30','bold')).place(x=300,y=10)
        Label(home,text='Track all your shipments in one place!',font=('Helvetica', '12')).place(x=450,y=60)
        Button(home,text='SignIn',height=2,width=10,font=('Helvetica','15'),borderwidth=5,bg='burlywood1',command=signinw).place(x=280,y=130)
        Button(home,text='Register',height=2,width=10,font=('Helvetica','15'),borderwidth=5,bg='burlywood1',command=registerw).place(x=500,y=130)
        Label(home,text='Enter your tracking number:',font=('Helvetica','15')).place(x=160,y=250)
        Label(home,text='ℹ️ After clicking track button please wait for 10 to 15 seconds to complete the process!',font=('Times','15')).place(x=7,y=565)
        trnumber=StringVar()
        Entry(home,width=35,bd=5,textvariable=trnumber).place(x=420,y=253)
        def trstart():              
            x=threading.Thread(target=fulltrack,daemon=True)
            x.start()  
        Button(home,text='Track',height=1,width=4,font=('Helvetica','10'),borderwidth=5,bg='burlywood1',command=trstart).place(x=650,y=251)
        

def fulltrack(): #individual_tracking
    trknumber=trnumber.get()
    if trknumber=='':
        return messagebox.showerror('Error','Enter Tracking Number')
    else:
        raise_frame(loading)
        img = Image.open('mainfiles/bg.png') 
        img = img.resize((900,600),Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)
        panel=Label(loading,image=img)
        panel.image = img
        Label(loading,text='Loading.....',font=('Times','50','bold')).place(x=295,y=200)
        panel.place(x=0,y=0)      
        try:
            destination_time=[]
            destination_status=[]
            origin_time=[]
            origin_status=[]
            driver=webdriver.Firefox(executable_path=path,options=options)
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
            def passiver():
                track.forget()
                raise_frame(home)
            raise_frame(track)            
            img = Image.open('mainfiles/bg.png') 
            img = img.resize((900,600),Image.ANTIALIAS)
            img = ImageTk.PhotoImage(img)
            panel=Label(track,image=img)
            panel.image = img
            panel.place(x=0,y=0)      
            Label(track,text='Tracking:'+trknumber,font=('Times',18,'bold')).place(x=330,y=7)
            Button(track,text='Back to Home',command=passiver,bg='burlywood1',borderwidth=5).place(x=800,y=10)
            Label(track,text='Origin: '+origin,font=('Helvetica','15')).place(x=230,y=60)
            Label(track,text='Destination: '+destination,font=('Helvetica','15')).place(x=570,y=60)
            Label(track,text='Status: '+status,font=('Helvetica','15')).place(x=400,y=90)
            Label(track,text='Present Status: '+pstatus,font=('Helvetica','14')).place(x=2,y=130)
            if len(destination_status)>=1:
                main=[]
                totalstatus=destination_status+origin_status
                totaltime=destination_time+origin_time
                for i in range(len(totalstatus)):
                    main1=(totaltime[i],totalstatus[i])
                    main.append(main1)
                scroll1=ttk.Scrollbar(track)
                scroll1.place(x=814,y=300)
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
                for i in range(len(totalstatus)):
                    main1=(totaltime[i],totalstatus[i])
                    main.append(main1)
                scroll1=ttk.Scrollbar(track)
                scroll1.place(x=814,y=300)
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
             
        except:
            raise_frame(home)
            return messagebox.showerror('Error','Could not track your package!')

def soon():
    messagebox.showinfo('Wait!','Coming Soon!')


def account_tracking():  #tracking_from_acc_page
        desclist=[]
        trconn=sqltor.connect('mainfiles/main.db')
        cursor=trconn.cursor()
        cursor.execute('select description from track')
        data=cursor.fetchall()
        for i in range(len(data)):
            data1=data[i]
            desclist.append(data1[0])        
        if trkno in desclist:
            return messagebox.showerror('Error','Select a tracking number!')
        else:
            t=trkno.split(':')
            trknum=t[1]
            accload=Frame(accwindow) 
            img = Image.open('mainfiles/bg.png') 
            img = img.resize((900,600),Image.ANTIALIAS)
            img = ImageTk.PhotoImage(img)
            panel=Label(accload,image=img)
            panel.image = img
            panel.place(x=0,y=0)                   
            accload.place(x=247,y=150,height=800, width=1000)
            Label(accload,text='Loading.....',font=('Times','50','bold')).place(x=215,y=200)
            try:
                destination_time=[]
                destination_status=[]
                origin_time=[]
                origin_status=[]
                driver=webdriver.Firefox(executable_path=path,options=options)
                driver.get('https://t.17track.net/en#nums='+trknum)
                time.sleep(7)
                driver.find_element_by_xpath('/html/body/div[6]/div/div[5]/a[1]').click()
                print('--Forwarding')                    
                time.sleep(2)
                driver.find_element_by_xpath('//*[@id="tn-'+trknum+'"]/div[2]/div[2]/div[2]/div/button').click()
                driver.find_element_by_xpath('//*[@id="yq-modal-translate"]/div/div/div[2]/div[1]/div/div/a[1]').click()
                time.sleep(2)
                origin=driver.find_element_by_xpath('//*[@id="tn-'+trknum+'"]/div[1]/div[2]/div[1]/div[2]/div/span').text
                destination=driver.find_element_by_xpath('//*[@id="tn-'+trknum+'"]/div[1]/div[2]/div[3]/div[2]/div/span').text
                status=driver.find_element_by_xpath('//*[@id="tn-'+trknum+'"]/div[1]/div[1]/div/p[2]').text
                pstatus=driver.find_element_by_xpath('//*[@id="tn-'+trknum+'"]/div[1]/div[3]/p').text
                try:  #destination status
                    st1=driver.find_element_by_class_name('des-block')
                    icv=1
                    while True:
                        dt_time=st1.find_element_by_xpath('//*[@id="tn-'+trknum+'"]/div[2]/div[1]/dl[2]/dd['+str(icv)+']/div/time').text
                        dt_sts=st1.find_element_by_xpath('//*[@id="tn-'+trknum+'"]/div[2]/div[1]/dl[2]/dd['+str(icv)+']/div/p').text
                        destination_time.append(dt_time)
                        destination_status.append(dt_sts)
                        icv=icv+1
                except:
                    pass
                try: #origin status
                    st2=driver.find_element_by_class_name('ori-block')
                    inc=1
                    while True:
                        dt_time=st2.find_element_by_xpath('//*[@id="tn-'+trknum+'"]/div[2]/div[1]/dl[1]/dd['+str(inc)+']/div/time').text
                        dt_sts=st2.find_element_by_xpath('//*[@id="tn-'+trknum+'"]/div[2]/div[1]/dl[1]/dd['+str(inc)+']/div/p').text
                        origin_time.append(dt_time)
                        origin_status.append(dt_sts)
                        inc=inc+1
                    print('completed')
                except:
                    pass
                trapage=Frame(accwindow) 
                img = Image.open('mainfiles/bg.png') 
                img = img.resize((900,600),Image.ANTIALIAS)
                img = ImageTk.PhotoImage(img)
                panel=Label(trapage,image=img)
                panel.image = img
                panel.place(x=0,y=0)                   
                trapage.place(x=247,y=150,height=800, width=1000)
                accload.destroy()
                Label(trapage,text='Tracking:'+trknum,font=('Times',18,'bold')).place(x=210,y=15)                
                Label(trapage,text='Origin: '+origin,font=('Helvetica','15')).place(x=40,y=57)
                Label(trapage,text='Destination: '+destination,font=('Helvetica','15')).place(x=200,y=57)
                Label(trapage,text='Status: '+status,font=('Helvetica','15')).place(x=400,y=57)
                Label(trapage,text='Present Status: '+pstatus,font=('Helvetica','14')).place(x=4,y=90)            
                if len(destination_status)>=1:
                    main=[]
                    totalstatus=destination_status+origin_status
                    totaltime=destination_time+origin_time
                    for i in range(len(totalstatus)):
                        main1=(totaltime[i],totalstatus[i])
                        main.append(main1)
                    frame33 = Frame(trapage,height = 2500, width = 6000)
                    frame33.place(x=20,y=150)                   
                    tb1=ttk.Treeview(frame33,columns=(1,2,3),show='headings',selectmode='browse')     
                    tb1.pack(side='left')
                    scroll1=ttk.Scrollbar(frame33,command=tb1.yview,orient='vertical')
                    scroll1.pack(side=RIGHT, fill=Y)
                    tb1.heading(1,text="Date & Time")
                    tb1.column(1,minwidth=15,width=150,stretch=NO)
                    tb1.heading(2,text="Status")
                    tb1.column(2,minwidth=30,width=600,stretch=NO)
                    tb1.heading(3,text="")
                    tb1.column(3,minwidth=30,width=150,stretch=NO)
                    for i in main: #appending details(subdetails)
                       tb1.insert('','end',values=i)
                    tb1.configure(yscrollcommand=scroll1.set)
                else:
                    totalstatus=origin_status
                    totaltime=origin_time
                    for i in range(len(totalstatus)):
                        main1=(totaltime[i],totalstatus[i])
                        main.append(main1)
                    frame33 = Frame(trapage,height = 2500,width = 6000)
                    frame33.place(x=20,y=150)
                    
                    scroll1=ttk.Scrollbar(frame33,command=tb1.yview,orient='vertical')
                    scroll1.pack(side=RIGHT, fill=Y)
                    tb1=ttk.Treeview(frame33,columns=(1,2),show='headings',selectmode='browse')   
                    tb1.pack(side='left')
                    tb1.heading(1,text="Date & Time")
                    tb1.column(1,minwidth=15,width=150,stretch=NO)
                    tb1.heading(2,text="Status")  
                    tb1.column(2,minwidth=30,width=600,stretch=NO) 
                    tb1.heading(3,text="")
                    tb1.column(3,minwidth=30,width=150,stretch=NO)
                    for i in main: #appending details(subdetails)
                        tb1.insert('','end',values=i)
                    tb1.configure(yscrollcommand=scroll1.set)                 
            except:
               return messagebox.showerror('Error','Could not find your \n tracking number!')

def tratest(): #checking and adding
    raise_frame(loading)
    img = Image.open('mainfiles/bg.png') 
    img = img.resize((900,600),Image.ANTIALIAS)
    img = ImageTk.PhotoImage(img)
    panel=Label(loading,image=img)
    panel.image = img
    Label(loading,text='Loading.....',font=('Times','50','bold')).place(x=295,y=200)
    panel.place(x=0,y=0)     
    try:
        driver=webdriver.Firefox(executable_path=path,options=options)
        driver.get('https://t.17track.net/en#nums='+addtrkno)
        time.sleep(7)
        print('--Forwarding')
        driver.find_element_by_xpath('/html/body/div[6]/div/div[5]/a[1]').click()
        time.sleep(2)
        driver.find_element_by_xpath('//*[@id="tn-'+addtrkno+'"]/div[2]/div[2]/div[2]/div/button').click()
        time.sleep(2)
        driver.find_element_by_xpath('//*[@id="yq-modal-translate"]/div/div/div[2]/div[1]/div/div/a[1]').click()  
        description1=description+':'
        print('--Forwarding')
        connw=sqltor.connect('mainfiles/main.db')
        cursor=connw.cursor()            
        command='''INSERT INTO track(trackingnumber,description) VALUES(?,?)'''
        data=(addtrkno,description1)
        cursor.execute(command,(data))
        connw.commit()
        add.forget()
        connw.close()
        threading.Thread(target=accountwindow)
        raise_frame(accwindow)
        messagebox.showinfo('Success!','Tracking number added!')
    except:
        raise_frame(accwindow)
        return messagebox.showerror('Error','Could not find your \n tracking number!')
        


def tratest1(): #testing
    global description
    description=descp.get()
    if description=='':
        return messagebox.showerror('Error','Enter description')
    else:
        threading.Thread(target=tratest).start()
    
  
def accountwindow(): #account_page    
    def logout():        
        accwindow.forget()
        command="update account set status = 'notlogged' where username=?"
        cursor.execute(command,(username,))           
        cv.commit()
        cv.close()
        Home()
    def addtr(): #add tracking number
        global addtrkno
        global descp
        addtrkno=adtr.get()
        descp=StringVar()
        if addtrkno=='':
            return messagebox.showerror('Error','Enter tracking number!')           
        else:
            raise_frame(add)
            img = Image.open('mainfiles/bg.png') 
            img = img.resize((900,600),Image.ANTIALIAS)
            img = ImageTk.PhotoImage(img)
            panel=Label(add,image=img)
            panel.image = img
            panel.place(x=0,y=0)
            Button(add,text='Back >>',bd=5,bg='burlywood1',command=lambda:raise_frame(accwindow)).place(x=800,y=7)
            Label(add,text='Add Tracking Number',font=('Times','20','bold')).place(x=360,y=7)
            Label(add,text='Add description: ',font=('Times','15','bold')).place(x=250,y=100)
            Entry(add,width=30,bd=5,textvariable=descp).place(x=400,y=100)       
            Button(add,text='Add',bd=5,bg='burlywood1',command=tratest1).place(x=600,y=150)
            Label(add,text='ℹ️Adding description is a must for tagging your tracking number!',font=('Times','15')).place(x=7,y=200)
            Label(add,text='ℹ️When execution starts it takes upto 11 to 15 seconds to check and add the tracking number to your account!',font=('Times','15')).place(x=7,y=230)

            

    trnos=[] #tracking_number_list
    desc=[] #description_list
    cv=sqltor.connect('mainfiles/main.db')
    cursor=cv.cursor()
    cursor.execute('select username from account')
    data=cursor.fetchall()
    data1=data[0]
    username=data1[0] #username
    cursor.execute('select trackingnumber from track')
    trs=cursor.fetchall()
    for i in range(len(trs)): #tracking_no._inject
        trs1=trs[i]
        trs2=trs1[0]
        trnos.append(trs2)
    cursor.execute('select description from track')
    desc3=cursor.fetchall()
    for i in range(len(desc3)):
        desc1=desc3[i]
        desc2=desc1[0]
        desc.append(desc2)
    signin.forget()
    raise_frame(accwindow)
    img = Image.open('mainfiles/bg.png') 
    img = img.resize((900,600),Image.ANTIALIAS)
    img = ImageTk.PhotoImage(img)
    panel=Label(accwindow,image=img)
    panel.image = img
    panel.place(x=0,y=0)
    top=Frame(accwindow,height = 150, width = 1000)
    top.place(x=0,y=0)
    top.configure(bg='SpringGreen2')
    Label(accwindow,text='User@'+username,bg='SpringGreen2',font=('Times','20','bold')).place(x=20,y=7)
    Button(accwindow,text='🔄',command=accountwindow,bg='SteelBlue1',bd=5,font=('Times','14','bold')).place(x=770,y=7)
    Button(accwindow,text='LogOut',bg='burlywood1',bd=5,command=logout).place(x=830,y=7)
    Label(accwindow,text='Enter tracking number: ',bg='SpringGreen2',font=('Times','15')).place(x=290,y=70)
    adtr=StringVar()
    Entry(accwindow,width=30,bd=5,textvariable=adtr).place(x=487,y=72)
    Button(accwindow,text='Add',bd=5,bg='burlywood1',command=addtr).place(x=700,y=70)
    def ss():
        global trkno
        trkno=leftside.get('active')
        threading.Thread(target=account_tracking).start()     
        
    Button(accwindow,text='View Full Report',bd=5,bg='burlywood1',command=ss).place(x=50,y=100)
    if len(trnos)>0 and len(desc)>0:        
        frame1 = Frame(accwindow,height = 1700, width = 1000)
        frame1.place(x=0,y=150)        
        #frame1.configure(bg='red')
        scroll=Scrollbar(frame1)
        scroll.pack(side=RIGHT, fill=Y)
        leftside = Listbox(frame1, yscrollcommand = scroll.set,width=18,height=15,bd=5,font=('Times','19'),selectmode=BROWSE)
        for i in range(len(trnos)):
            leftside.insert(END,desc[i])
            leftside.insert(END,'🚚:'+trnos[i])
        leftside.pack(side=LEFT, fill=BOTH)
        scroll.config(command=leftside.yview)                    
    else:
        pass
    

def infow(): #info_page
    raise_frame(info)
    img = Image.open('mainfiles/bg.png') 
    img = img.resize((900,600),Image.ANTIALIAS)
    img = ImageTk.PhotoImage(img)
    panel=Label(info,image=img)
    panel.image = img
    panel.place(x=0,y=0)       
    Button(info,text='Go to Home >>',command=lambda:raise_frame(home),bg='burlywood1').place(x=800,y=7)
    Label(info,text='Info',font=('Helvetica','30',)).place(x=420,y=7)
    Label(info,text='Version Number: 3.0',font=('Times','20')).place(x=340,y=90)
    Label(info,text='License: Apache2.0',font=('Times','20')).place(x=360,y=140)
    Label(info,text='Owned By: Synite Solutions',font=('Times','20')).place(x=310,y=190)
    Label(info,text='Last Update: 25-06-2020',font=('Times','20')).place(x=330,y=240)
    Label(info,text='Browser Type: FireFox',font=('Times','20')).place(x=335,y=285)
    img = Image.open('mainfiles/new.ico') 
    img = img.resize((250, 250), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(img)
    panel=Label(info,image=img)
    panel.image = img 
    panel.place(x=335,y=340)



def signinw(): #signin_page
    def proceed():
        username=uname.get()
        password=pswd.get()
        cursor.execute('select username,password from account')
        data=cursor.fetchall()
        try:
            data1=data[0]
            dbuser=data1[0]
            dbpswd=data1[1]
        except:
            pass
        if len(data)==0:
            return messagebox.showerror('Error','No account found!')
        elif username=='':
            return messagebox.showerror('Error','Enter Username')
        elif password=='':
            return messagebox.showerror('Error','Enter Password')
        elif username!=dbuser:
            return messagebox.showerror('Error','Incorrect username/password')
        elif password!=dbpswd:
            return messagebox.showerror('Error','Incorrect username/password')
        else:
            command="update account set status = 'logged' where username=?"
            cursor.execute(command,(username,))
            conn.commit()
            accountwindow()
            
    uname=StringVar()
    pswd=StringVar()
    raise_frame(signin)
    img = Image.open('mainfiles/bg.png') 
    img = img.resize((900,600),Image.ANTIALIAS)
    img = ImageTk.PhotoImage(img)
    panel=Label(signin,image=img)
    panel.image = img
    panel.place(x=0,y=0)      
    Button(signin,text='Go to Home',font=('Times','10','bold'),bg='burlywood1',command=lambda:raise_frame(home)).place(x=820,y=7)
    Label(signin,text='SignIn',font=('Times','30','bold')).place(x=380,y=7)
    Label(signin,text='Enter Username: ',font=('Times','15')).place(x=270,y=90)
    Entry(signin,width=30,bd=5,textvariable=uname).place(x=420,y=91)
    Label(signin,text='Enter Password: ',font=('Times','15')).place(x=270,y=150)
    Entry(signin,width=30,bd=5,show='*',textvariable=pswd).place(x=420,y=150)
    Button(signin,text='LogIn',font=('Times','15'),bg='burlywood1',command=proceed).place(x=570,y=220)






    
def registerw(): #registration_page
        fname=StringVar()
        lname=StringVar()
        uname=StringVar()
        pswd=StringVar()
        pswdc=StringVar()
        def proceed():
            cursor.execute('select username from account')
            data=cursor.fetchall()                           
            firstname=fname.get()
            lastname=lname.get()
            username=uname.get()
            password=pswd.get()
            pswdcnf=pswdc.get() #password_confirm
            if len(data)==1:
                return messagebox.showerror('Error','Already account registered \n in this computer!')
            elif firstname=='':
                return messagebox.showerror('Error','Enter First name')
            elif lastname=='':
                return messagebox.showerror('Error','Enter Last name')
            elif username=='':
                return messagebox.showerror('Error','Enter username')
            elif password=='':
                return messagebox.showerror('Error','Enter password')
            elif pswdcnf=='':
                return messagebox.showerror('Error','Enter confirm password')
            elif password!=pswdcnf:
                return messagebox.showerror('Error','Password not matching!')
            elif len(password)<8:
                return messagebox.showerror('Error','Password less than 8 characters!')
            else:
                name=firstname+' '+lastname
                status='notlogged'
                command='insert into account (username,name,password,status) values (?,?,?,?)'
                data=(username,name,password,status)
                cursor.execute(command,data)
                conn.commit()
                register.forget()
                raise_frame(home)
                messagebox.showinfo('Success!','Account Created!')

        
        raise_frame(register)        
        img = Image.open('mainfiles/bg.png') 
        img = img.resize((900,600),Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)
        panel=Label(register,image=img)
        panel.image = img
        panel.place(x=0,y=0)
        Button(register,text='Go to Home',font=('Times','10','bold'),bg='burlywood1',command=lambda:raise_frame(home)).place(x=820,y=7)
        Label(register,text='Register',font=('Times','30','bold')).place(x=380,y=7)
        Label(register,text='FirstName:',font=('Times','15')).place(x=230,y=90)
        Entry(register,width=30,bd=5,textvariable=fname).place(x=370,y=90)
        Label(register,text='LastName:',font=('Times','15')).place(x=230,y=150)
        Entry(register,width=30,bd=5,textvariable=lname).place(x=370,y=150)
        Label(register,text='Username:',font=('Times','15')).place(x=230,y=210)
        Entry(register,width=30,bd=5,textvariable=uname).place(x=370,y=210)
        Label(register,text='Password:',font=('Times','15')).place(x=230,y=270)
        Entry(register,width=30,bd=5,textvariable=pswd,show='*').place(x=370,y=270)
        Label(register,text='Confirm Password:',font=('Times','15')).place(x=200,y=320)
        Entry(register,width=30,bd=5,textvariable=pswdc,show='*').place(x=370,y=320)
        Button(register,text='Proceed',bg='burlywood1',font=('Times','12','bold'),bd=5,command=proceed).place(x=550,y=400)

try:
    cursor.execute('select status from account')
    data=cursor.fetchall()
    data1=data[0]
    status=data1[0]
    if status=='logged':
        accountwindow()
    else:
        Home()
except:
    Home()
    
main.mainloop()

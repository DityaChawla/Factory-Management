from tkinter import Tk, Label, Frame, Button, Entry, Canvas, Scrollbar, BOTTOM
from PIL import ImageTk, Image
import mysql.connector as mysql
from datetime import date

#__________________________________________________________________________________________________________________________________________
# File Handling

try:
    file = open("nsasysytems.txt","a+")
except:
    file = open("nsasystems.txt","w+")

def fileget():
    file.seek(0)
    records = file.readlines()

    noOfRec = len(records)

    for i in range(noOfRec):
        records[i] = records[i].strip('\n').split()
        noOfCol = len(records[i])
        a = [int(i) for i in range(1,noOfCol-4)] 
        for j in range(noOfCol):
            if j in a:
                continue
            records[i][j] = int(records[i][j])
        
        if noOfCol > 6:
            s = ' '.join(records[i][1:noOfCol-4])
            for _ in range(noOfCol-6):
                records[i].pop(2)
            records[i][1] = s

    return records

def fileput(records):
    file.seek(0)
    file.truncate()

    noOfRec = len(records)

    for i in range(noOfRec):
        for j in range(6):
            if j==1:
                continue
            records[i][j] = str(records[i][j])

    for i in range(noOfRec):
        s = ' '.join(records[i])
        file.write(s+'\n')

#__________________________________________________________________________________________________________________________________________
# File Handling Worker

def fileadd(Id,wrkrName):
    records = fileget()
    records.append([Id,wrkrName,0,0,0,0])
    fileput(records)

def filedit(Id,wrkrName):
    records = fileget()
    noOfRec = len(records)
    for i in range(noOfRec):
        if records[i][0] == Id:
            records[i][1] = wrkrName
            break
    fileput(records)

def filermv(Id):
    records = fileget()
    noOfRec = len(records)
    for i in range(noOfRec):
        if records[i][0] == Id:
            records.pop(i)
            break
    fileput(records)

#__________________________________________________________________________________________________________________________________________
# SQL
#un = input("Enter MySQL Username: ")
#pswd = input("Enter MySQL Password: ")

mydb = mysql.connect(
    host = "localhost",
    username = 'root',
    password = 'vishu1812'
    )
mycursor = mydb.cursor()
mycursor.execute("SHOW DATABASES")
databases = mycursor.fetchall()
mycursor.execute("USE NSASystems")

#__________________________________________________________________________________________________________________________________________
# Welcome Screen

wlcm_scrn = Tk()
wlcm_scrn.title("NSA")
wlcm_scrn.attributes("-fullscreen", True)

fctry = ImageTk.PhotoImage(Image.open("/Users/arnavgupta/Desktop/DBS mini project/wlcm.jpeg"))
Label(wlcm_scrn,image=fctry).pack()

wlcm_scrn_frame = Frame(wlcm_scrn,bg="#FB5233",bd=10, padx = 25)
Label(wlcm_scrn_frame, text ="NSA SYSTEMS", font= ("Algerian",20),bg="#FB5233") .pack()
Button(wlcm_scrn_frame,text="Enter Password",command=wlcm_scrn.destroy,bg="#FFB51E").pack(side = BOTTOM,padx=10,pady=10)
wlcm_scrn_frame.place(x=575,y=300)

wlcm_scrn.mainloop()

#__________________________________________________________________________________________________________________________________
# Password Screen

masterPassword = "1"

def check():
    ntrd_psswrd = psswrd.get()
    if ntrd_psswrd == masterPassword:
        psswrd_crct.pack()
        psswrd_scrn.destroy()
    else:
        psswrd_ncrct.pack()

psswrd_scrn = Tk()
psswrd_scrn.title("Password")
psswrd_scrn.attributes("-fullscreen", True)

camo = ImageTk.PhotoImage(Image.open("/Users/arnavgupta/Desktop/DBS mini project/safe.jpg"))
Label(psswrd_scrn,image=camo).pack()

psswrd_scrn_frame = Frame(psswrd_scrn,bg="#9E9FA3",bd=10)
Label(psswrd_scrn_frame,text="Enter Password",font=("Calibri",20) ,bg="#9E9FA3",fg="Black").pack()
psswrd = Entry(psswrd_scrn_frame,width=50,borderwidth=5,bg="#9E9FA3",fg="Black")
psswrd.pack(pady = 5,padx=10)
psswrd.insert(0,"")
psswrd_crct = Label(psswrd_scrn_frame,text="Welcome",bg="#9E9FA3",fg="GREEN")
psswrd_ncrct = Label(psswrd_scrn_frame,text="Wrong Password\nRetry",bg="#9E9FA3",fg="RED")
Button(psswrd_scrn_frame,text="Enter",command=check,bg = "#9E9FA3",fg="Black",padx = 50, pady = 10).pack(side=BOTTOM, padx=10, pady=10)
psswrd_scrn_frame.place(x=515, y=500)
psswrd_scrn.mainloop()

#___________________________________________________________________________________________________________________________________
# Add Worker

global wrkr_scrn, addwrkr_scrn, rmvwrkr_scrn, editwrkr_scrn

def wrkr_sql():
    mycursor.execute("Select * from wrkr ORDER BY Salary DESC")
    records = mycursor.fetchall()
    return records

def add():
    Id = emp_idd.get()
    wrkrName = name.get()
    desc = designation.get()
    slry = salary.get()
    gndr=gender.get()
    addrs=Address.get()
    Id = int(Id)
    slry = int(slry)

    s = "INSERT INTO wrkr VALUES(%s,%s,%s,%s,%s,%s,%s)"
    val = [(Id,wrkrName,desc,slry,date.today(),gndr,addrs)]

    mycursor.executemany(s,val)
    mydb.commit()

    fileadd(Id,wrkrName)

    addwrkr_scrn.destroy()
    wrkr_scrn.destroy()
    wrkr()

def addwrkr():
    global addwrkr_scrn

    addwrkr_scrn = Tk()
    addwrkr_scrn.title("Add Worker")

    global emp_idd,name,designation,salary,startDate,gender,Address

    info = Frame(addwrkr_scrn,bg = "black")
    Label(info, text = "Enter Emp_ID:",bg="Black",fg="#F7761B").pack()
    emp_idd = Entry(info,width=50,borderwidth=5,bg="Black",fg="#F7761B")
    emp_idd.pack()

    Label(info, text = "Enter Name:",bg="Black",fg="#F7761B").pack()
    name = Entry(info,width=50,borderwidth=5,bg="Black",fg="#F7761B")
    name.pack()

    Label(info, text = "Enter Designation:",bg="Black",fg="#F7761B").pack()
    designation = Entry(info,width=50,borderwidth=5,bg="Black",fg="#F7761B")
    designation.pack()

    Label(info, text = "Enter Salary:",bg="Black",fg="#F7761B").pack()
    salary = Entry(info,width=50,borderwidth=5,bg="Black",fg="#F7761B")
    salary.pack()
    Label(info, text = "Enter Gender:",bg="Black",fg="#F7761B").pack()
    gender = Entry(info,width=50,borderwidth=5,bg="Black",fg="#F7761B")
    gender.pack()
    Label(info, text = "Enter Address:",bg="Black",fg="#F7761B").pack()
    Address = Entry(info,width=50,borderwidth=5,bg="Black",fg="#F7761B")
    Address.pack()

    Button(info, text = "Add", command=add,fg="Black",bg="#F7761B").pack()
    info.pack()


#___________________________________________________________________________________________________________________________________
# Remove Screen

def rmv():

    Id = emp_idd.get()
    Id = int(Id)

    s = "DELETE FROM wrkr WHERE Id = %s"
    val = [(Id)]

    mycursor.execute(s,val)
    mydb.commit()

    filermv(Id)

    rmvwrkr_scrn.destroy()
    wrkr_scrn.destroy()
    wrkr()

def rmvwrkr():

    global rmvwrkr_scrn

    rmvwrkr_scrn = Tk()
    rmvwrkr_scrn.title("Remove Worker")

    global emp_idd

    info = Frame(rmvwrkr_scrn,bg = "black")
    Label(info, text = "Enter emp_id:",bg="Black",fg="#F7761B").pack()
    emp_idd = Entry(info,width=50,borderwidth=5,bg="Black",fg="#F7761B")
    emp_idd.pack()

    Button(info,text = "Remove",command = rmv,fg="Black",bg="#F7761B").pack()
    info.pack()

#___________________________________________________________________________________________________________________________________
# Editing Screen

def edit():

    Id = emp_idd.get()
    wrkrName = name.get()
    desc = designation.get()
    slry = salary.get()
    strtDte = startDate.get()
    Id = int(Id)
    slry = int(slry)

    s = "UPDATE wrkr SET WorkerName = %s, Designation = %s, Salary = %s,Start = %s WHERE emp_idd = %s"
    val = [(wrkrName,desc,slry,strtDte,Id)]

    mycursor.executemany(s,val)
    mydb.commit()

    filedit(Id,wrkrName)

    editwrkr_scrn.destroy()
    wrkr_scrn.destroy()
    wrkr()

def editwrkr():
    global editwrkr_scrn

    editwrkr_scrn = Tk()
    editwrkr_scrn.title("Edit Worker")
    editwrkr_scrn.configure(bg="black")

    global emp_idd,name,designation,salary,startDate

    info = Frame(editwrkr_scrn, bg = "black")
    Label(info, text = "Enter Emp_id:",bg="black",fg="#F7761B").pack()
    emp_idd = Entry(info,width=50,borderwidth=5,bg="Black",fg="#F7761B")
    emp_idd.pack()

    Label(info, text = "Enter Name:",bg="black",fg="#F7761B").pack()
    name = Entry(info,width=50,borderwidth=5,bg="Black",fg="#F7761B")
    name.pack()

    Label(info, text = "Enter Designation:",bg="black",fg="#F7761B").pack()
    designation = Entry(info,width=50,borderwidth=5,bg="Black",fg="#F7761B")
    designation.pack()

    Label(info, text = "Enter Salary:",bg="black",fg="#F7761B").pack()
    salary = Entry(info,width=50,borderwidth=5,bg="Black",fg="#F7761B")
    salary.pack()

    Label(info, text = "Since:",bg="black",fg="#F7761B").pack()
    startDate = Entry(info,width=50,borderwidth=5,bg="Black",fg="#F7761B")
    startDate.pack()

    Button(info,text = "Edit",command = edit,bg = "#F7761B").pack()
    info.pack()

#___________________________________________________________________________________________________________________________________
# Worker Screen

def wrkr():

    global wrkr_scrn

    wrkr_scrn = Tk()
    wrkr_scrn.title("Workers")
    wrkr_scrn.attributes("-fullscreen",True)
    wrkr_scrn.configure(bg = "Black")
    
    Label(wrkr_scrn,text = "Workers",fg = "#F7761B",bg = "black",font=("Old English Text MT",30),pady = 2,padx = 80).place(x=530,y=30)

    records = wrkr_sql()

    data = [('EMPID','Workers','Description','Salary','Starting Date','Gender','Address')]
    data.extend(records)

    rows = len(data)
    columns = 7

    wrkr_frm = Frame(wrkr_scrn,bg="black")
    wrkr_cnvs = Canvas(wrkr_frm,height = 500,width = 976,bg="black")
    scroll_y = Scrollbar(wrkr_frm, orient="vertical", command=wrkr_cnvs.yview)
    wrkr_frm1 = Frame(wrkr_cnvs)
    
    wrkr_frm1.place(x = 250,y = 100)

    for i in range(rows):
        for j in range(columns):
            if i==0:
                l = Label(wrkr_frm1,text=data[i][j],bg = "black",fg = "#F7761B",padx=15,pady=3)
                l.configure(font =("Algerian",20))
                l.grid(row=i,column=j,sticky="nsew",padx = 1,pady=1)
            else:
                l = Label(wrkr_frm1,text=data[i][j],bg = "#F7761B",padx=3,pady=3)
                l.grid(row=i,column=j,sticky="nsew",padx = 1,pady=1)

    wrkr_cnvs.create_window(1000, 1000, anchor='nw', window=wrkr_frm1)
    wrkr_cnvs.update_idletasks()

    wrkr_cnvs.configure(scrollregion=wrkr_cnvs.bbox('all'),yscrollcommand=scroll_y.set)

    wrkr_cnvs.pack(fill='both', expand=True, side='left')
    scroll_y.pack(fill='y', side='right')

    wrkr_frm.place(x =180,y=100)

    wrkr_frm2 = Frame(wrkr_scrn,bg="Black", padx = 25, pady= 10)
    Button(wrkr_frm2,text="Add Worker",command = addwrkr,bg="#F7761B",padx = 120,pady=10).grid(row = 1,column = 1,padx=10,pady=10)
    Button(wrkr_frm2,text="Remove Worker",command=rmvwrkr,bg="#F7761B",padx=110,pady=10).grid(row = 1,column = 2)
    Button(wrkr_frm2,text="Edit Worker",command=editwrkr,bg="#F7761B",padx=121,pady=10).grid(row = 2,column = 1)
    Button(wrkr_frm2,text="Return",command=wrkr_scrn.destroy, bg="#F7761B",padx = 135,pady=10).grid(row = 2,column = 2)
    wrkr_frm2.place(x = 330,y = 615)

    wrkr_scrn.mainloop()

#___________________________________________________________________________________________________________________________________
# Salary Screen

def do():
    d.destroy()

    for i in range(noOfRec):
        if records[i][0] in present:
            string = "SELECT Salary FROM wrkr WHERE emp_idd = %s"%(records[i][0])
            mycursor.execute(string)
            salary = mycursor.fetchone()
            records[i][2]+=1
            records[i][-1]+=(salary[0]//30)
        else:
            records[i][3]+=1
    fileput(records)

    slry_scrn.destroy()
    slry()

def done():
    global d
    d = Tk()
    d.configure(bg="black")
    Button(d,text = "done",command = do,bg="#F7761B",fg="black").pack()

def p():
    present.append(adhaar)
    tndnce_scrn.destroy()
    indtndnce(num+1)

def ab():
    tndnce_scrn.destroy()
    indtndnce(num+1)

def indtndnce(i):
    if i>=noOfRec:
        done()
        return 0
    global name, adhaar,tndnce_scrn, num
    num = i
    name = records[i][1]
    adhaar = records[i][0]
    tndnce_scrn = Tk()
    tndnce_scrn.configure(bg="black")
    t = "Is %s there ?\nAdhar Number - %s"%(name,adhaar)
    Label(tndnce_scrn,text = t,bg = "black",fg = "#F7761B").pack()

    Button(tndnce_scrn,text = "Present", command = p,bg = "#F7761B",fg="black").pack()
    Button(tndnce_scrn,text = "Absent",command = ab,bg = "#F7761B",fg = "black").pack()

def mrktndnce():
    global present, noOfRec, records
    present = []
    records = fileget()
    noOfRec = len(records)
    indtndnce(0)

def vrtmDone():
    adhaarNumber = int(adhaar.get())
    noOfHr = int(noh.get())

    string = "SELECT Salary FROM wrkr WHERE emp_idd = %s"%(adhaarNumber)
    mycursor.execute(string)
    salary = mycursor.fetchone()
    salary = salary[0]//(30*24)

    vrtm_scrn.destroy()

    records = fileget()
    for i in range(len(records)):
        if records[i][0] == adhaarNumber:
            records[i][-2]+=noOfHr
            records[i][-1]+=(noOfHr*salary)
    
    fileput(records)

    slry_scrn.destroy()
    slry()

def vrtm():
    global vrtm_scrn, adhaar, noh
    vrtm_scrn = Tk()
    vrtm_scrn.title("Overtime")
    vrtm_scrn.configure(bg="black")
    vrtmFrame = Frame(vrtm_scrn,bg="black")

    Label(vrtmFrame,text="Enter Emp_ID: ",bg="black",fg="#F7761B").pack()
    adhaar = Entry(vrtmFrame, width=50,borderwidth=5,bg="black",fg="#F7761B")
    adhaar.pack(pady = 5,padx=10)

    Label(vrtmFrame,text="Enter Number of hours: ",bg="black",fg='#F7761B').pack()
    noh  = Entry(vrtmFrame, width=50,borderwidth=5,bg="black",fg="#F7761B")
    noh.pack(pady = 5,padx=10)
    
    Button(vrtmFrame,text="Done",command = vrtmDone,bg="#F7761B",fg="black").pack()

    vrtmFrame.pack()

def zrattndnce():
    records = fileget()
    noOfRec = len(records)
    for i in range(noOfRec):
        records[i][2],records[i][3],records[i][4],records[i][5]=0,0,0,0
    fileput(records)

    slry_scrn.destroy()
    slry()

def slry():
    global slry_scrn
    slry_scrn = Tk()
    slry_scrn.title("Salary")
    slry_scrn.attributes("-fullscreen",True)
    slry_scrn.configure(bg="black")

    Label(slry_scrn,text = "Salary",fg = "#F7761B",bg = "black",font=("Old English Text MT",30),pady = 2,padx = 80).place(x=545,y=30)
    
    records = fileget()

    data = [('EMPID','Workers','Attendance','Holidays','overtime','Salary')]
    data.extend(records)

    rows = len(data)
    columns = 6

    slry_frm = Frame(slry_scrn, bg="black")
    slry_cnvs = Canvas(slry_frm,height = 500,width = 1025,bg="black")
    scroll_y = Scrollbar(slry_frm, orient="vertical", command=slry_cnvs.yview)
    slry_frm1 = Frame(slry_cnvs)
    
    slry_frm1.place(x = 250,y = 100)

    for i in range(rows):
        for j in range(columns):
            if i==0:
                l = Label(slry_frm1,text=data[i][j],bg="black",fg = "#F7761B",padx=10,pady=3)
                l.configure(font = ("Algerian",20))
                l.grid(row=i,column=j,sticky="nsew",padx = 1,pady=1)
            else:
                l = Label(slry_frm1,text=data[i][j],bg="#F7761B",fg="black",padx=3,pady=3)
                l.grid(row=i,column=j,sticky="nsew",padx = 1,pady=1)

    slry_cnvs.create_window(1000, 1000, anchor='nw', window=slry_frm1)
    slry_cnvs.update_idletasks()

    slry_cnvs.configure(scrollregion=slry_cnvs.bbox('all'),yscrollcommand=scroll_y.set)

    slry_cnvs.pack(fill='both', expand=True, side='left')
    scroll_y.pack(fill='y', side='right')

    slry_frm.place(x = 175,y=100)

    slry_frm2 = Frame(slry_scrn,bg = "black")
    Button(slry_frm2,text="Mark Attendance",command = mrktndnce,bg="#F7761B",fg="black",padx = 102,pady=10).grid(row = 1,column = 1,padx=10,pady=10)
    Button(slry_frm2,text="Overtime",command = vrtm,bg="#F7761B",fg="black",padx = 116,pady=10).grid(row = 1,column = 2)
    Button(slry_frm2,text="Give Salary",command = zrattndnce,bg="#F7761B",fg="black",padx = 119,pady=10).grid(row = 2,column = 1)
    Button(slry_frm2,text="Return",command = slry_scrn.destroy,bg="#F7761B",fg="black",padx=122,pady=10).grid(row = 2,column = 2)
    slry_frm2.place(x = 375,y = 615)

    slry_scrn.mainloop()
#___________________________________________________________________________________________________________________________________
# department Screen
def dept_sql():
    mycursor.execute("Select * from department")
    records = mycursor.fetchall()
    return records
def dept():
    
    global dept_screen

    dept_scrn = Tk()
    dept_scrn.title("Department")
    dept_scrn.attributes("-fullscreen",True)
    dept_scrn.configure(bg = "Black")
    
    Label(dept_scrn,text = "Department",fg = "#F7761B",bg = "black",font=("Old English Text MT",30),pady = 2,padx = 80).place(x=530,y=30)

    records = dept_sql()

    data = [('Dname','Dnumber','Mgr_id','Manager_start')]
    data.extend(records)

    rows = len(data)
    columns = 4

    dept_frm = Frame(dept_scrn,bg="black")
    dept_cnvs = Canvas(dept_frm,height = 500,width = 976,bg="black")
    scroll_y = Scrollbar(dept_frm, orient="vertical", command=dept_cnvs.yview)
    dept_frm1 = Frame(dept_cnvs)
    
    dept_frm1.place(x = 250,y = 100)

    for i in range(rows):
        for j in range(columns):
            if i==0:
                l = Label(dept_frm1,text=data[i][j],bg = "black",fg = "#F7761B",padx=15,pady=3)
                l.configure(font =("Algerian",20))
                l.grid(row=i,column=j,sticky="nsew",padx = 1,pady=1)
            else:
                l = Label(dept_frm1,text=data[i][j],bg = "#F7761B",padx=3,pady=3)
                l.grid(row=i,column=j,sticky="nsew",padx = 1,pady=1)

    dept_cnvs.create_window(1000, 1000, anchor='nw', window=dept_frm1)
    dept_cnvs.update_idletasks()

    dept_cnvs.configure(scrollregion=dept_cnvs.bbox('all'),yscrollcommand=scroll_y.set)

    dept_cnvs.pack(fill='both', expand=True, side='left')
    scroll_y.pack(fill='y', side='right')

    dept_frm.place(x =180,y=100)

    dept_frm2 = Frame(dept_scrn,bg="Black", padx = 25, pady= 10)
    #Button(dept_frm2,text="Add Worker",command = adddept,bg="#F7761B",padx = 120,pady=10).grid(row = 1,column = 1,padx=10,pady=10)
    #Button(dept_frm2,text="Remove Worker",command=rmvdept,bg="#F7761B",padx=110,pady=10).grid(row = 1,column = 2)
    #Button(dept_frm2,text="Edit Worker",command=editdept,bg="#F7761B",padx=121,pady=10).grid(row = 2,column = 1)
    #Button(dept_frm2,text="Return",command=dept_scrn.destroy, bg="#F7761B",padx = 135,pady=10).grid(row = 2,column = 2)
    dept_frm2.place(x = 330,y = 615)

    dept_scrn.mainloop()

#___________________________________________________________________________________________________________________________________
# Main Menu Screen

mn_scrn = Tk()
mn_scrn.title("Main Screen")
mn_scrn.attributes("-fullscreen",True)

stats = ImageTk.PhotoImage(Image.open("/Users/arnavgupta/Desktop/DBS mini project/Factory.jpg"))
Label(mn_scrn,image=stats).pack()

mn_scrn_frame = Frame (mn_scrn,bg="#000000",bd = 10,pady=40)
Button(mn_scrn_frame,text="Workers",command=wrkr,bg = "#1B3E82",fg = "#000000",padx=100, pady=20).pack(padx=50, pady=10)
Button(mn_scrn_frame,text="Salary",command=slry,bg = "#1B3E82",fg = "#000000",padx=105, pady=20).pack(padx=50, pady=10)
Button(mn_scrn_frame,text="Department",command=dept,bg = "#1B3E82",fg = "#000000",padx=105, pady=20).pack(padx=50, pady=10)
Button(mn_scrn_frame,text="Exit",command=mn_scrn.destroy,bg = "#1B3E82",fg = "#000000",padx=110, pady=20).pack(padx=50, pady=10)
mn_scrn_frame.place(x=500,y=175)

mn_scrn.mainloop()

file.close()
mydb.close()

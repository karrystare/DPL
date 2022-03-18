import tkinter as tk
import tkinter.font as tkFont
import face_recognizer as recognizer
import image_generator as generator

database = {}

def output(txt):
    global message
    print(txt)
    message.set(txt)

def GButton_859_command():
    INPUT = GLineEdit_578.get("1.0", "end-1c")
    temp = ''
    if INPUT.find(',') != -1:
        names = INPUT.split(',')
        for name in names:
            output("Fetch Images for: " + name)
            temp = generator.fetch_picture(name)
    elif INPUT != '':
        output("Fetch Images for: " + INPUT)
        temp = generator.fetch_picture(INPUT)
    else:
        output("Input a Name")
        return None
    if temp == None:
        output("No Capture Device Found, ReCheck Settings")

def GButton_999_command():
    global database, message
    database = recognizer.fill_database()
    if not database:
        output("No Data Loaded")
        return None
    output("Database Created Successfully")

def GButton_112_command():
    global database, message
    if not database:
        output("Database is Empty")
        return None
    INPUT = GLineEdit_578.get("1.0", "end-1c")
    if INPUT != '':
        recognizer.save_database(database, INPUT)
    else:
        recognizer.save_database(database, "database")
    output("Database Saved Successfully")     

def GButton_217_command():
    global database, message
    database_temp = {}
    INPUT = GLineEdit_578.get("1.0", "end-1c")
    if INPUT != '':
        database_temp = recognizer.load_database(INPUT)
    else:
        database_temp = recognizer.load_database("database")
    if database_temp == None:
        output("No File To Load")
        return None
    database = database_temp
    output("Database Loaded Successfully")

def GButton_214_command():
    global database, message
    database_temp = {}
    INPUT = GLineEdit_578.get("1.0", "end-1c")
    if INPUT != '':
        database_temp = recognizer.add_database(database, INPUT)
    else:
        print("Input a Name")
        return None
    if database_temp == None:
        output("Can't Access Camera")
        return None
    database = database_temp
    output("Entry " + INPUT + " Added Successfully")  

def GButton_454_command():
    global database, message
    if not database:
        output("Database is Empty")
        return None
    INPUT = GLineEdit_578.get("1.0", "end-1c")
    if INPUT != '':
        database = recognizer.remove_database(database, INPUT)
    else:
        output("Input a Name")
        return None
    output("Entry " + INPUT + " Removed Successfully")
    
def GButton_851_command():
    global database, message
    attendance = set()
    if not database:
        output("Database is Empty")
        return None
    slot = GLineEdit_655.get("1.0", "end-1c")
    if slot != '':
        attendance = recognizer.verify_face(database, slot)
        if attendance == None:
            output("No Capture Device Found, ReCheck Settings")
            return None
    else:
        output("Input a Shift Name")
        return None
    output('Attended:\n' + ', '.join(attendance))

def GButton_325_command():
    global database, message
    if not database:
        output("Database is Empty")
        return None
    output(', '.join([*database]))

def GButton_750_command():
    root.destroy()
    
root = tk.Tk()
message = tk.StringVar()
message.set('')
#setting title
root.title("Attendance Marking Module")
#setting window size
width=600
height=500
screenwidth = root.winfo_screenwidth()
screenheight = root.winfo_screenheight()
alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
root.geometry(alignstr)
root.resizable(width=False, height=False)

GButton_859=tk.Button(root)
GButton_859["bg"] = "#e9e9ed"
ft = tkFont.Font(family='Times',size=10)
GButton_859["font"] = ft
GButton_859["fg"] = "#000000"
GButton_859["justify"] = "center"
GButton_859["text"] = "Take Picture"
GButton_859.place(x=10,y=10,width=125,height=40)
GButton_859["command"] = GButton_859_command

GButton_999=tk.Button(root)
GButton_999["bg"] = "#e9e9ed"
ft = tkFont.Font(family='Times',size=10)
GButton_999["font"] = ft
GButton_999["fg"] = "#000000"
GButton_999["justify"] = "center"
GButton_999["text"] = "Create Database"
GButton_999.place(x=10,y=60,width=125,height=40)
GButton_999["command"] = GButton_999_command

GButton_112=tk.Button(root)
GButton_112["bg"] = "#e9e9ed"
ft = tkFont.Font(family='Times',size=10)
GButton_112["font"] = ft
GButton_112["fg"] = "#000000"
GButton_112["justify"] = "center"
GButton_112["text"] = "Save Database"
GButton_112.place(x=10,y=110,width=125,height=40)
GButton_112["command"] = GButton_112_command

GButton_217=tk.Button(root)
GButton_217["bg"] = "#e9e9ed"
ft = tkFont.Font(family='Times',size=10)
GButton_217["font"] = ft
GButton_217["fg"] = "#000000"
GButton_217["justify"] = "center"
GButton_217["text"] = "Load Database"
GButton_217.place(x=10,y=160,width=125,height=40)
GButton_217["command"] = GButton_217_command

GButton_214=tk.Button(root)
GButton_214["bg"] = "#e9e9ed"
ft = tkFont.Font(family='Times',size=10)
GButton_214["font"] = ft
GButton_214["fg"] = "#000000"
GButton_214["justify"] = "center"
GButton_214["text"] = "Add Entry"
GButton_214.place(x=10,y=210,width=125,height=40)
GButton_214["command"] = GButton_214_command

GButton_454=tk.Button(root)
GButton_454["bg"] = "#e9e9ed"
ft = tkFont.Font(family='Times',size=10)
GButton_454["font"] = ft
GButton_454["fg"] = "#000000"
GButton_454["justify"] = "center"
GButton_454["text"] = "Remove Entry"
GButton_454.place(x=10,y=260,width=125,height=40)
GButton_454["command"] = GButton_454_command

GButton_851=tk.Button(root)
GButton_851["bg"] = "#e9e9ed"
ft = tkFont.Font(family='Times',size=10)
GButton_851["font"] = ft
GButton_851["fg"] = "#000000"
GButton_851["justify"] = "center"
GButton_851["text"] = "Run Attendance"
GButton_851.place(x=10,y=310,width=125,height=40)
GButton_851["command"] = GButton_851_command

GButton_325=tk.Button(root)
GButton_325["bg"] = "#e9e9ed"
ft = tkFont.Font(family='Times',size=10)
GButton_325["font"] = ft
GButton_325["fg"] = "#000000"
GButton_325["justify"] = "center"
GButton_325["text"] = "Show Saved Names"
GButton_325.place(x=10,y=360,width=125,height=40)
GButton_325["command"] = GButton_325_command

GLabel_557=tk.Label(root)
ft = tkFont.Font(family='Times',size=10)
GLabel_557["font"] = ft
GLabel_557["fg"] = "#333333"
GLabel_557["justify"] = "center"
GLabel_557["text"] = "List of Names (A, B, C)"
GLabel_557.place(x=270,y=20,width=228,height=30)

GLabel_804=tk.Label(root)
ft = tkFont.Font(family='Times',size=10)
GLabel_804["font"] = ft
GLabel_804["fg"] = "#333333"
GLabel_804["justify"] = "center"
GLabel_804["text"] = "Shift Name"
GLabel_804.place(x=300,y=220,width=166,height=30)

GLabel_142=tk.Label(root)
ft = tkFont.Font(family='Times',size=10)
GLabel_142["font"] = ft
GLabel_142["fg"] = "#333333"
GLabel_142["justify"] = "center"
GLabel_142["text"] = "Output"
GLabel_142.place(x=290,y=330,width=180,height=30)

GLineEdit_655=tk.Text(root)
GLineEdit_655["borderwidth"] = "1px"
ft = tkFont.Font(family='Times',size=10)
GLineEdit_655["font"] = ft
GLineEdit_655["fg"] = "#333333"
GLineEdit_655.place(x=190,y=250,width=400,height=70)

GLineEdit_578=tk.Text(root)
GLineEdit_578["borderwidth"] = "1px"
ft = tkFont.Font(family='Times',size=10)
GLineEdit_578["font"] = ft
GLineEdit_578["fg"] = "#333333"
GLineEdit_578.place(x=190,y=50,width=400,height=170)

GMessage_754=tk.Message(root)
ft = tkFont.Font(family='Times',size=10)
GMessage_754["font"] = ft
GMessage_754["fg"] = "#0006FD"
GMessage_754["justify"] = "center"
GMessage_754["textvariable"] = message
GMessage_754.place(x=190,y=360,width=400,height=125)

GButton_750=tk.Button(root)
GButton_750["bg"] = "#e9e9ed"
ft = tkFont.Font(family='Times',size=10)
GButton_750["font"] = ft
GButton_750["fg"] = "#000000"
GButton_750["justify"] = "center"
GButton_750["text"] = "Exit"
GButton_750.place(x=10,y=410,width=125,height=40)
GButton_750["command"] = GButton_750_command

root.mainloop()

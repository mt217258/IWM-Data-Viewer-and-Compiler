'''
Author:             Matthew McLaughlin
Contact:            mt217258@dal.ca
TODO List:          - add ability to swap between views (CO2/LOI/etc)
                    - move CO2 view to CO2_module
Version History: 
'''

#### MODULE VERSION ####
'''
X.Y.Z - X: External release, Y: Internal Release, Z: Prototype version. 
If incremented, set all values to the right to 0. Ex: 0.1.12 -> 1.0.0
'''
CONST_GUI_VERSION = "0.1.0"  

#### LIBRARIES ####
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from matplotlib import *

from CO2_module import *
from shared import *

#### GLOBAL VARIABLES ####
window_main = Tk()
CO2_filename = StringVar()

#### CLASSES ####
    #### Magic Methods
    #### Mangled Methods
    #### Muggle Methods
    
#### VULGER METHODS #### (They have no class)
def create_main_window():
    global window_main
    window_main.title("IWM Data Viewer and Report Generator")
    window_main.geometry('1200x600')
    
    #Menu Bar
    menuBar = Menu(window_main, tearoff=False)
    window_main.config(menu=menuBar)
    
    #File
    file_menu = Menu(menuBar, tearoff=False)
    #file_menu.add_command(label='Connect') #TODO - live feed connection
    file_menu.add_command(label='Exit', command=window_main.destroy)
    
    #Tools
    tool_menu = Menu(menuBar, tearoff=False)
    
    #Help
    help_menu = Menu(menuBar, tearoff=False)
    help_menu.add_command(label='About', command=popUpAbout)
    
    menuBar.add_cascade(label="File",menu=file_menu,underline=0)
    menuBar.add_cascade(label="Tools",menu=tool_menu,underline=0)
    menuBar.add_cascade(label="Help",menu=help_menu,underline=0)
    
    return window_main

def popUpAbout():
    messagebox.showinfo("About","GUI Version: {gui_ver}\n"
                                "CO2 Module Version: {co2_ver}\n"
                                "Contact: mt217278@dal.ca"
                                .format(gui_ver=CONST_GUI_VERSION, 
                                        co2_ver=CONST_CO2MODULE_VERSION))

def updateGraph(data):
    print("Updating plot")

def loadCO2File(label):
    global CO2_filename 
    global CO2_data
    
    CO2_filename.set(askopenfilename(defaultextension='.csv', filetypes=[("csv files", '*.csv')], title="Choose file to load:")) 
    CO2_data = loadCO2Data(CO2_filename.get())

def generateCO2ReportButton():
    global CO2_data
    global CO2_summary
    
    CO2_summary = generateCO2Report(CO2_data)

#### MAIN ####
def main():   
    global CO2_filename
    global CO2_summary
      
    window_main = create_main_window()    
    window_main.grid_rowconfigure(1, weight=1)
    window_main.grid_columnconfigure(0, weight=1)
    
    #### Title Frame < window ####
    titleFrame = Frame(window_main, bg="red")
    titleFrame.grid(row = 0, column = 0, sticky = "nsew")
    titleFrame.grid_columnconfigure(0, weight=1)
    
    viewTitle = Label(titleFrame, text="CO2 Data Report", bg=pallette["c5"], fg="white").grid(row = 0, column = 0, sticky = "nsew")
    
    #### Main Frame < window #### 
    mainFrame = Frame(window_main, bg=pallette["c2"])
    mainFrame.grid(row = 1, column = 0, columnspan=1, rowspan=1, sticky = "nsew")
    mainFrame.grid_columnconfigure(0, weight=1)
    mainFrame.grid_columnconfigure(1, weight=2)
    mainFrame.grid_rowconfigure(0, weight=1)
    mainFrame.grid_rowconfigure(1, weight=1)
    
    #### File IO Frame < main ####
    buttonFrameT = Frame(mainFrame, bg=pallette["c1"])
    buttonFrameT.grid(row = 0, column = 0, sticky = "nsew") 
    buttonFrameT.grid_columnconfigure(0, weight=1)
    
    Label(buttonFrameT, text="File Input & Outputs", bg=pallette["c4"], fg="white").grid(row = 0, column = 0, sticky = "nsew")
    
    buttonFrame = Frame(buttonFrameT, bg=pallette["c1"])
    buttonFrame.grid(row = 1, column = 0, sticky = "nsew")
    buttonFrame.grid_columnconfigure(1, weight=1)
    
    inputFileLabel = Label(buttonFrame, textvariable= CO2_filename, bg="white", fg="black").grid(column = 1, row = 1, sticky = "ew")
    Button(buttonFrame, text="Load Data", bg="tan", width= 15, command=lambda:loadCO2File(inputFileLabel)).grid(column=0, row=1)
    Button(buttonFrame, text="Generate Report", bg="tan", width= 15, command=generateCO2ReportButton).grid(column=0, row=2)
    Button(buttonFrame, text="Save Report", bg="tan", width= 15, command=lambda:saveCO2Report(CO2_summary, CO2_filename.get())).grid(column=0, row=3)
    
    #### Data Select Frame < main ####
    dataSelectFrame = Frame(mainFrame, bg=pallette["c1"])
    dataSelectFrame.grid(row = 1, column = 0, sticky = "nsew")
    
    window_main.mainloop()
    
if __name__ == '__main__':
    main()
import tkinter as tk
from tkinter import *
from tkinter.ttk import *
from PIL import Image, ImageTk
from urllib.request import urlopen
from io import BytesIO
from tkinter import filedialog
from tkinter import messagebox
import os
import io
import PyPDF2
import gtts
from gtts import gTTS
# import subprocess ## Add this if you want to open the pdf file

# Creating our application window GUI
window = tk.Tk()
# Giving the window a special icon
URL = "https://i.postimg.cc/dVZy2ZRW/TTS-Logo.png"
urlhand = urlopen(URL)
raw_data = urlhand.read()
urlhand.close()
img = Image.open(BytesIO(raw_data))
logo = ImageTk.PhotoImage(img)
window.tk.call('wm', 'iconphoto', window._w, logo)
# Giving the window a Title
window.title("PDF Reader - TTS")
# Gets the requested values of the height and widht
windowWidth = window.winfo_reqwidth()
windowHeight = window.winfo_reqheight()
# Gets half the screen width/height and the full window width/height
positionRight = int(window.winfo_screenwidth()/2 - windowWidth)
positionDown = int(window.winfo_screenheight()/2 - windowHeight)
# Positions the window in the center of the screen
window.geometry("+{}+{}".format(positionRight, positionDown))

# Create the command function for SelectFile_btn
def OFD():
    global F_Name
    File_Name.delete(0,END)
    F_Name = filedialog.askopenfilename(initialdir="C:/",
                                            filetypes =(("PDF File", "*.pdf"),("All Files","*.*")),
                                            title = "Choose a File to Read")
    #Using try in case user types in unknown file or closes without choosing a file
    try:
        File_Name.insert(0, os.path.basename(F_Name))
        #subprocess.Popen([F_Name], shell=True) ## You can include this if you want to open the pdf
        PageNum_radio['state']=NORMAL
        PageRange_radio['state']=NORMAL
    except:
        messagebox.showinfo("Error Message", "No File has been Choosen")

# Create function to get the number of pages the selected file has   
def Pnum():
    global book 
    global pdfReader
    book = open(F_Name, 'rb')
    pdfReader = PyPDF2.PdfFileReader(book)
    Page_num = pdfReader.numPages
    TotalPages_lbl.config(text="of "+str(Page_num))
    PageNum_spinbox['state']=NORMAL
    PageNum_spinbox.config(to = Page_num)
    FromRange_txtbox['state']=DISABLED
    ToRange_txtbox['state']=DISABLED

# Create function to get the range of pages we want to read
def Rnum():
    global book 
    global pdfReader
    book = open(F_Name, 'rb')
    pdfReader = PyPDF2.PdfFileReader(book)
    Page_num = pdfReader.numPages
    TotalPagesR_lbl.config(text="of "+str(Page_num))
    FromRange_txtbox['state']=NORMAL
    ToRange_txtbox['state']=NORMAL
    PageNum_spinbox['state']=DISABLED

# Create the command function for Lang_Combox 
def LangSelected(event):
    if (Lang.get()!='' and Speed.get()!=''):
        SaveFile_btn['state']=NORMAL
    return Lang.get()

# Create the command function for Speed_Combox
def SpeedSelected(event):
    if (Lang.get()!='' and Speed.get()!=''):
        SaveFile_btn['state']=NORMAL
    return Speed.get()
        
# TTS function
def TTSmain():
    global Ftext
    global langV
    global tts
    LangSelected
    gTTS_Lang = dict()
    gTTS_Lang = { 'Afrikaans':'af', 'Arabic':'ar', 'Bengali':'bn', 'Bosnian':'bs', 'Catalan':'ca', 'Czech':'cs', 'Welsh':'cy',
              'Danish':'da', 'German':'de', 'Greek':'el', 'English':'en', 'Esperanto':'eo', 'Spanish':'es', 'Estonian':'et',
              'Finnish':'fi', 'French':'fr', 'Gujarati':'gu', 'Hindi':'hi', 'Croatian':'hr', 'Hungarian':'hu', 'Armenian':'hy',
              'Indonesian':'id', 'Icelandic':'is', 'Italian':'it', 'Japanese':'ja', 'Javanese':'jw', 'Khmer':'km', 'Kannada':'kn',
              'Korean':'ko', 'Latin':'la', 'Latvian':'lv', 'Macedonian':'mk', 'Malayalam':'ml', 'Marathi':'mr', 'Myanmar':'my',
              'Nepali':'ne', 'Dutch':'nl', 'Norwegian':'no', 'Polish':'pl', 'Portuguese':'pt', 'Romanian':'ro', 'Russian':'ru',
              'Sinhala':'si', 'Slovak':'sk', 'Albanian':'sq', 'Serbian':'sr', 'Sundanese':'su', 'Swedish':'sv', 'Swahili':'sw',
              'Tamil':'ta', 'Telugu':'te', 'Thai':'th', 'Filipino':'tl', 'Turkish':'tr', 'Ukrainian':'uk', 'Urdu':'ur',
              'Vietnamese':'vi', 'Chinese':'zh-CN', 'Taiwan':'zh-TW', 'Mandarin':'zh'}
    langV = gTTS_Lang.get(Lang.get())

    fullText = list()
    Ftext = ''
    if (PageNum_spinbox.get()!=''):
        fromPage = int(PageNum_spinbox.get())-1
        for iPage in range(pdfReader.getNumPages()):
            if iPage < fromPage: continue
            elif iPage == fromPage:
                page = pdfReader.getPage(iPage)
                text = page.extractText()
                fullText.append(text)
        for element in range(len(fullText)):
            Ftext = Ftext + fullText[element]

    if (FromRange_txtbox.get()!='' and ToRange_txtbox.get()!=''):
        fromPage = int(FromRange_txtbox.get())-1
        toPage = int(ToRange_txtbox.get())
        for iPage in range (fromPage, toPage):
            if (iPage < fromPage or iPage > toPage): continue
            page = pdfReader.getPage(iPage)
            text = page.extractText()
            fullText.append(text)
        for element in range(len(fullText)):
            Ftext = Ftext + fullText[element]
    
    if (Speed.get() == 'Normal'):
        tts = gTTS(Ftext, lang=langV, slow=False)
    elif (Speed.get() == 'Slower'):
        tts = gTTS(Ftext, lang=langV, slow=True)

# Create the command function for Save button
def save():
    TTSmain()
    Name = F_Name.split('.')
    S_Name = Name[0]
    if (Speed.get() == 'Normal'):
        tts.save(S_Name+'.mp3')
        #os.system("start "+S_Name+".mp3") ## include this if you want the program to play the audio file after saving it
    elif (Speed.get() == 'Slower'):
        tts.save(S_Name+'_slow.mp3')
        #os.system("start "+S_Name+"_slow.mp3") ## include this if you want the program to play the audio file after saving it
    book.close()
    messagebox.showinfo("Save Audio File Message", "Your PDF file has been Converted to an Audio file")
    PageNum_spinbox.delete(0,END)
    FromRange_txtbox.delete(0,END)
    ToRange_txtbox.delete(0,END)
    PageNum_spinbox['state']=DISABLED
    FromRange_txtbox['state']=DISABLED
    ToRange_txtbox['state']=DISABLED

# Create a label for the file name
FileName_lbl = Label(window, text="File Name :")
FileName_lbl.grid(row=0, column=0, sticky= W+E, padx=(20,5), pady=10)

# Create a textbox for the file name
global File_Name
File_Name = Entry(window, width = 20, justify=CENTER)
File_Name.grid(row=0, column=1, padx=(5,10), pady=10)

# Create a select file button
SelectFile_btn = Button(window, text="Select a File", command=OFD)
SelectFile_btn.grid(row=0, column=2, columnspan=2, sticky= W+E, padx=(10,20), pady=10)

# Create a frame for the features
Features_frame = LabelFrame(window, text="Feautres Section")
Features_frame.grid(row=1, column=0, columnspan=4, sticky= W+E, padx=20, pady=(0,10))

# Create Page Number Radio Button
global PageNum_radio
PageNum_radio = Radiobutton(Features_frame, text="Specify a Page Number", value=1, command=Pnum)
PageNum_radio['state']=DISABLED
PageNum_radio.grid(row=0, column=0, sticky=W, padx=10, pady=10)
global PageNum_spinbox
PageNum_spinbox = Spinbox(Features_frame, from_= 1, to = 0 ,width=5, justify=CENTER)
PageNum_spinbox['state']=DISABLED
PageNum_spinbox.grid(row=0, column=1, sticky=W, padx=10, pady=10)
global TotalPages_lbl
TotalPages_lbl = Label(Features_frame, text="of ")
TotalPages_lbl.grid(row=0, column=1, sticky=W, padx=(70,10), pady=10)

# Create Page Range Number Radio Button
global PageRange_radio
PageRange_radio = Radiobutton(Features_frame, text="Specify a Page Range", value=2, command=Rnum)
PageRange_radio['state']=DISABLED
PageRange_radio.grid(row=1, column=0, sticky=W, padx=10, pady=10)
global FromRange_txtbox
FromRange_txtbox = Entry(Features_frame, width=5, justify=CENTER)
FromRange_txtbox['state']=DISABLED
FromRange_txtbox.grid(row=1, column=1, sticky=W, padx=10, pady=10)
global ToRange_txtbox
ToRange_txtbox = Entry(Features_frame, width=5, justify=CENTER)
ToRange_txtbox['state']=DISABLED
ToRange_txtbox.grid(row=1, column=1, sticky=W, padx=(60,0), pady=10)
global TotalPagesR_lbl
TotalPagesR_lbl = Label(Features_frame, text="of ")
TotalPagesR_lbl.grid(row=1, column=1, sticky=W, padx=(100,10), pady=10)

# Create Language DropDown Menu
Lang_lbl = Label(Features_frame, text="Specify a Language")
Lang_lbl.grid(row=2, column=0, sticky=W, padx=(28,0), pady=10)
gTTS_List = [ 'Afrikaans', 'Arabic', 'Bengali', 'Bosnian', 'Catalan', 'Czech', 'Welsh',
              'Danish', 'German', 'Greek', 'English', 'Esperanto', 'Spanish', 'Estonian',
              'Finnish', 'French', 'Gujarati', 'Hindi', 'Croatian', 'Hungarian', 'Armenian',
              'Indonesian', 'Icelandic', 'Italian', 'Japanese', 'Javanese', 'Khmer', 'Kannada',
              'Korean', 'Latin', 'Latvian', 'Macedonian', 'Malayalam', 'Marathi', 'Myanmar',
              'Nepali', 'Dutch', 'Norwegian', 'Polish', 'Portuguese', 'Romanian', 'Russian',
              'Sinhala', 'Slovak', 'Albanian', 'Serbian', 'Sundanese', 'Swedish', 'Swahili',
              'Tamil', 'Telugu', 'Thai', 'Filipino', 'Turkish', 'Ukrainian', 'Urdu',
              'Vietnamese', 'Chinese', 'Taiwan', 'Mandarin' ]
global Lang_Combox
Lang = StringVar()
Lang_Combox = tk.ttk.Combobox(Features_frame, width=15, justify=CENTER, value=gTTS_List, textvariable=Lang)
#Lang_Combox.current(-1)
Lang_Combox.bind('<<ComboboxSelected>>', LangSelected)
Lang_Combox.grid(row=2, column=1, padx=(0,10), pady=10)

# Create Speed DropDown Menu
Speed_lbl = Label(Features_frame, text="Specify Speech Speed")
Speed_lbl.grid(row=3, column=0, sticky=W, padx=(28,0), pady=10)
Speed_li = [ 'Normal', 'Slower' ]
global Speed_Combox
Speed = StringVar()
Speed_Combox = tk.ttk.Combobox(Features_frame, width=15, justify=CENTER, value=Speed_li, textvariable=Speed)
Speed_Combox.bind('<<ComboboxSelected>>', SpeedSelected)
Speed_Combox.grid(row=3, column=1, padx=(0,10), pady=10)

# Create Save as External Audio File button
SaveFile_btn = Button(window, text="Save as Audio", command=save)
SaveFile_btn['state']=DISABLED
SaveFile_btn.grid(row=5, column=0, columnspan=5, sticky= W+E, padx=20, pady=10)

window.mainloop()
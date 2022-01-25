from dbfread import DBF
from tkinter import *
import tkinter
from tkinter import Label
from project_functions import *


def wind():


    global window
    global listbox
    global scrollbar
    global scrollbar2

    global listbox2
    global frame2
    global button

    # Main Window
    window = tkinter.Tk()
    window.resizable(False, False)
    window.title('DBFtoCSV')
    window.geometry('1000x700')

    # Auction List Box
    frame = Frame(window, padx=5, pady=5, width=500, height=400)
    frame.pack(side=LEFT, anchor= "s")
    frame.propagate(0)

    scrollbar = Scrollbar(frame, orient='vertical')
    scrollbar.pack(side = RIGHT, fill = Y)
    scrollbar2 = Scrollbar(frame, orient='horizontal')
    scrollbar2.pack(side = BOTTOM, fill = X)

    listbox = Listbox(frame, bd = 1, height=10, font=('Times', 14), activestyle="none")

    listbox.config(yscrollcommand = scrollbar.set, xscrollcommand = scrollbar2.set)

    counter = 0
    another_counter=1
    some_list = []
    
    #for line in eventhead_dbf_read:
        #listbox.insert(counter, line['EVENTNAME'])
        #listbox.insert()
        #another_counter= another_counter+1
        #counter = counter+1


    for line in eventhead_dbf_read:
        some_list.append(line['EVENTNAME'])
    listbox.insert(counter, *some_list)
    another_counter= another_counter+1
    counter = counter+1

    listbox.bind('<<ListboxSelect>>', go)


    listbox.pack(side=TOP, fill=BOTH, expand=TRUE)

    scrollbar.config(command = listbox.yview)
    scrollbar2.config(command = listbox.xview)

    label = Label(window, text="List of Auctions", relief="sunken").place(x=200, y=270)

    # Items List Box
    frame2 = Frame(window, padx=5, pady=5, width=500, height=400)
    frame2.pack(side=RIGHT, anchor= "s")
    frame2.propagate(0)

    scrollbar3 = Scrollbar(frame2, orient='vertical')
    scrollbar3.pack(side = RIGHT, fill = Y)
    scrollbar4 = Scrollbar(frame2, orient='horizontal')
    scrollbar4.pack(side = BOTTOM, fill = X)

    listbox2 = Listbox(frame2, bd=1, height=10, font=('Times', 12), activestyle="none")

    listbox2.config(yscrollcommand = scrollbar3.set, xscrollcommand = scrollbar4.set)

    listbox2.pack(side=TOP, fill=BOTH, expand=TRUE)

    scrollbar3.config(command = listbox2.yview)
    scrollbar4.config(command = listbox2.xview)

    label2 = Label(window, text="List of Items in the Selected Auction", relief="sunken").place(x=650, y=270)

    # Input Buttonx
    button = tkinter.Entry(window)
    button.place(x=400, y=100)
    input = button.get()


    make_csv_button = tkinter.Button(window, text="To CSV", height=2, width=8, command=make_csv_but).place(x=125, y=150)
    buttonClear = tkinter.Button(window, text="Clear", height=2, width=8, command=clear).place(x=225, y=150)
    imageButton = tkinter.Button(window, text="Images", height=2, width=8, command=images).place(x=625, y=150)

    window.mainloop()

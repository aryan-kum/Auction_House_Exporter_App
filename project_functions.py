import csv
from dbfread import DBF
from tkinter import *
import tkinter
import project_window
import cv2
import numpy as np
from PIL import Image
import os
import time



some_counter = 0

some_counter2 = 0

auctions_path = "C:\\AuctionFlex\\Data"

images_path = "C:\\AuctionFlex\\Images\\"

pictures_read = DBF(auctions_path+'\\'+'PICTURES.DBF', load=True)

items_dbf_read = DBF(auctions_path+'\\'+'ITEMS.DBF', load=True)

eventhead_dbf_read = DBF(auctions_path+'\\'+'EVENTHEAD.DBF', load=True)
    
eventitems_dbf_read = DBF(auctions_path+'\\'+'EVENTITEMS.DBF', load=True)

def item_list():

    global pic_location_list

    pic_location_list = []
    new_list = []                                       
    
    for line in eventitems_dbf_read:
        new_list = []
        if line['EVENT_ID'] == event_id:
            new_list.append(line['ITEM_ID'])
        for x in new_list:
            for line in pictures_read:
                if x == line['ITEM_ID']:
                    pic_location_list.append(line['PICTURE_LO'])

def resize(image_pil, width, height):

    global some_counter

    some_counter = some_counter + 1
    '''
    Resize PIL image keeping ratio and using white background.
    '''
    ratio_w = width / image_pil.width
    ratio_h = height / image_pil.height
    if ratio_w < ratio_h:
        # It must be fixed by width
        resize_width = width
        resize_height = round(ratio_w * image_pil.height)
    else:
        # Fixed by height
        resize_width = round(ratio_h * image_pil.width)
        resize_height = height
    image_resize = image_pil.resize((resize_width, resize_height), Image.ANTIALIAS)
    background = Image.new('RGBA', (width, height), (255, 255, 255, 255))
    offset = (round((width - resize_width) / 2), round((height - resize_height) / 2))
    background.paste(image_resize, offset)
    background.save('practice2-pil.png')
    im1 = Image.open(r'practice2-pil.png')
    rgb_im = im1.convert('RGB')
    os.remove("practice2-pil.png")
    rgb_im.save(r'C:\\AuctionFlex\\Exported_Images\\Auction_Id-'+str(event_id)+'\\'+str(some_counter)+'.jpg')

def resizeAndPad(img, size, padColor=0):

    global some_counter2

    some_counter2 = some_counter2 + 1

    h, w = img.shape[:2]
    sh, sw = size

    # interpolation method
    if h > sh or w > sw: # shrinking image
        interp = cv2.INTER_AREA
    else: # stretching image
        interp = cv2.INTER_CUBIC

    # aspect ratio of image
    aspect = w/h  # if on Python 2, you might need to cast as a float: float(w)/h

    # compute scaling and pad sizing
    if aspect > 1: # horizontal image
        new_w = sw
        new_h = np.round(new_w/aspect).astype(int)
        pad_vert = (sh-new_h)/2
        pad_top, pad_bot = np.floor(pad_vert).astype(int), np.ceil(pad_vert).astype(int)
        pad_left, pad_right = 0, 0
    elif aspect < 1: # vertical image
        new_h = sh
        new_w = np.round(new_h*aspect).astype(int)
        pad_horz = (sw-new_w)/2
        pad_left, pad_right = np.floor(pad_horz).astype(int), np.ceil(pad_horz).astype(int)
        pad_top, pad_bot = 0, 0
    else: # square image
        new_h, new_w = sh, sw
        pad_left, pad_right, pad_top, pad_bot = 0, 0, 0, 0

    # set pad color
    if len(img.shape) == 3 and not isinstance(padColor, (list, tuple, np.ndarray)): # color image but only one color provided
        padColor = [padColor]*3

    # scale and pad
    scaled_img = cv2.resize(img, (new_w, new_h), interpolation=interp)
    scaled_img = cv2.copyMakeBorder(scaled_img, pad_top, pad_bot, pad_left, pad_right, borderType=cv2.BORDER_CONSTANT, value=padColor)

    cv2.imwrite('C:\\AuctionFlex\\Exported_Images\\Auction_Id-'+str(event_id)+'\\'+str(some_counter2)+'.jpg',scaled_img) 

    return scaled_img

def auction_item_listing(auction_name):
    global event_id

    counter = 1

    project_window.listbox2.delete(0,END)
    another_counter = 0
    item_id = 0
    event_id = 0
    auction_item_list = []
    for line in eventhead_dbf_read:
        if line['EVENTNAME'] == auction_name:
            event_id = line['EVENT_ID']
    for line in eventitems_dbf_read:
        if line['EVENT_ID'] == event_id:
            item_id = line['ITEM_ID']
            auction_item_list.append(item_id)
    for x in auction_item_list:
        for line in items_dbf_read:
            if x == line['ITEM_ID']:
                project_window.listbox2.insert(another_counter, str(counter)+": "+line['LEAD'])
                another_counter = another_counter+1
                counter = counter + 1

def make_1stcsv(x2):  
    new_list = []
    item_id = 0                                         
        
    with open("liveauctioneersCatalog.csv", "w", newline='') as fw:
        writer = csv.writer(fw)
        writer.writerow(['LotNum', 'Title', 'Description', 'LowEst', 'HighEst', 'StartPrice'])
        for line in eventitems_dbf_read:
            new_list = []
            if line['EVENT_ID'] == event_id:
                item_id = line['ITEM_ID']
                new_list.append(line['LOTNUM'])
                for x in items_dbf_read:
                    if x['ITEM_ID'] == item_id:
                        new_list.append(x['LEAD'])
                        new_list.append(x['DESCRIPTIO'])
                        new_list.append(x['PRESALEEST'])
                        new_list.append(x['PRESALEES2'])
                        new_list.append(0)
                writer.writerow(new_list)


def make_2stcsv(x2):
    new_list = []
    item_id = 0 

    with open("InvaluablesCatalog.csv", "w", newline='') as fw:
        writer = csv.writer(fw)
        writer.writerow(['lotnum', 'lead', 'description1', 'presaleestmin', 'presaleestmax'])
        for line in eventitems_dbf_read:
            new_list = []
            if line['EVENT_ID'] == event_id:
                item_id = line['ITEM_ID']
                new_list.append(line['LOTNUM'])
                for x in items_dbf_read:
                    if x['ITEM_ID'] == item_id:
                        new_list.append(x['LEAD'])
                        new_list.append(x['DESCRIPTIO'])
                        new_list.append(x['PRESALEEST'])
                        new_list.append(x['PRESALEES2'])
                writer.writerow(new_list)


    
def make_csv(x):
    make_1stcsv(x)
    make_2stcsv(x)



# on-click function for Auction List Box
def go(event):
    global text_entry

    project_window.button.delete("0", "end")
    cs = project_window.listbox.curselection()
    text_entry = project_window.listbox.get(cs)
    project_window.button.insert(0, text_entry)
    auction_item_listing(text_entry)
    clear_eventid()


# Functions
global make_csv_but
global clear

def make_csv_but():
    global answerLabel
    make_csv("C:\AuctionFlex\Data")
    answerLabel = tkinter.Label(project_window.window, height=1, width=50, text="DONE!!!")
    answerLabel.pack()
    answerLabel.place(x=700, y=150)

def clear():
    project_window.button.delete("0", "end")
    project_window.listbox2.delete(0,END)
    project_window.listbox.selection_clear(0, 'end')
    
    # Destroy the variable answerLabel only if it was created via make_csv()
    if 'answerLabel' in globals():
        answerLabel.destroy()

    if 'answerLabel2' in globals():
        answerLabel2.destroy()

    answerLabel3 = tkinter.Label(project_window.window, height=1, width=50, text="Auction not Selected")
    answerLabel3.pack()
    answerLabel3.place(x=300, y=250)


def images():

    global answerLabel2

    mydir = ('C:\\AuctionFlex\\Exported_Images')
    check_folder = os.path.isdir(mydir)
    if not check_folder:
        os.makedirs(mydir)
    item_list()
    mydir = ('C:\\AuctionFlex\\Exported_Images\\Auction_Id-'+str(event_id))
    check_folder = os.path.isdir(mydir)
    if not check_folder:
        os.makedirs(mydir)
    start_time = time.time()
    for x in pic_location_list:
        v_img = cv2.imread(images_path+x)
        resizeAndPad(v_img, (1500,1500), 255)
    answerLabel2 = tkinter.Label(project_window.window, height=1, width=50, text="DONE Images")
    answerLabel2.pack()
    answerLabel2.place(x=600, y=200)
    print("My program took", time.time() - start_time, "to run") 

def clear_eventid():
    global answerLabel3

    answerLabel3 = tkinter.Label(project_window.window, height=1, width=50, text="Event ID: " + str(event_id))
    answerLabel3.pack()
    answerLabel3.place(x=300, y=250)
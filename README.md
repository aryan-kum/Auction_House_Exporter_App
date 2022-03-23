# Auction_House_Exporter_App


This software was made for an Online Auction House.


project1.py - This file is calling main which includes the application window.

project_functions.py - This file has all the functions defined and all the functionality of the application.

project_window.py - This file is responsible for generating a window for the application and making the buttons work when clicked on.




For this project, I was required to generate 2 CSV files based on a certain criteria and user selection. Data was being read from multiple database files(.DBF) and then being converted into CSV's. Furthermore, I was required to display all the items in the auction selected by user. Adding on, I was required to process images as well whose path were in a different DBF file. I was required to resize the images of user selected auction to a specific resolution(1500x1500) while maintaining their aspect ratio. I used tkinter module to get the mainframe of the application and used several other module such as csv to generate CSV files, dbfread to read DBF files and cv2 to process the images.

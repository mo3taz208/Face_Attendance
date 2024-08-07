import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk

from tkinter import filedialog, messagebox
import shutil
import os

# Face dedection and recognetion For Attendance
import cv2
import face_recognition
import os
import numpy as np
import datetime
import pyttsx3
# from PIL import ImageGrab
# print("Now:", datetime.datetime.now())
path = 'E:/Face Attendance Project with GUI/Face Attendance Project with GUI/image'
images = []
classNames = []
myList = os.listdir(path)
print(myList)

count = 0
for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}') # f outside to make it read the path
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])
print(classNames)
#print(classNames[0][0:14])
#print(classNames[0][14:-1])

def add_photos():
    # Open file dialog to select photos
    file_paths = filedialog.askopenfilenames(title="Select Photos", filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.gif")])
    
    if file_paths:
        # Folder where photos will be added
        destination_folder = 'E:/Face Attendance Project with GUI/Face Attendance Project with GUI/image'  # Change this to your specific folder path
        
        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)
        
        for file_path in file_paths:
            try:
                shutil.copy(file_path, destination_folder)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add photo: {e}")
                return
        
        messagebox.showinfo("Success", "Photos added successfully!")

def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

def markAttendance(num,img):
    with open('E:/Face Attendance Project with GUI/Face Attendance Project with GUI/attendance.csv', 'r+') as f:
        myDataList = f.readlines()
        numList =[]
        print(myDataList)
        for line in myDataList:
            entry = line.split(',')
            numList.append(entry[0])
        if num not in numList:
            current_datetime = datetime.datetime.now()
            dtString = current_datetime.strftime('%x %X')
            # Calling the strftime() function to convert
            # the above current datetime into excel serial date number
            #print(current_datetime.strftime('%x %X'))
            f.writelines(f'{num}, {dtString}, 1 \n')
            global count
            count += 1

encodeListKnown = findEncodings(images)
print(len(encodeListKnown))

cap = cv2.VideoCapture(0)


def open_file():
    browse_text.set("RUN")
    while True:
        success , img = cap.read()
        imgS = cv2.resize(img,(0,0),None,0.25,0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
        
        facesCurFrame = face_recognition.face_locations(imgS)
        encodesCurFrame = face_recognition.face_encodings(imgS,facesCurFrame)
        
        for encodeFace,faceLoc in zip(encodesCurFrame,facesCurFrame):      # we use zip to put them in same loop
            matches =face_recognition.compare_faces(encodeListKnown,encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown,encodeFace) #return list and gave distance to best match
            print(faceDis)
            matchIndex = np.argmin(faceDis)    #lost element in lest is best match
            
            if matches[matchIndex]:
                namee = classNames[matchIndex].upper()
                print(namee)
                num = namee[0:14]
                name = namee[14:-1]
                print(name)
                y1,x2,y2,x1 = faceLoc
                y1,x2,y2,x1 = y1*4,x2*4,y2*4,x1*4
                #print("################################################################")
                #print(y2,x1)
                #print("################################################################")
                cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
                cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
                cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
                markAttendance(num,img)
                engine = pyttsx3.init()
                engine.say(name)
                engine.runAndWait()
                
            if not matches[matchIndex]:
                name = "Unknown"
                print(name)
                y1,x2,y2,x1 = faceLoc
                y1,x2,y2,x1 = y1*4,x2*4,y2*4,x1*4
                cv2.rectangle(img,(x1,y1),(x2,y2),(0,0,255),2)
                cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,0,255),cv2.FILLED)
                cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,0,0),2)
                engine = pyttsx3.init()
                engine.say(name)
                engine.runAndWait()
                # Create main window
                if (cv2.waitKey(1) & 0xFF) == ord('s'):
                    root = tk.Tk()
                    root.title("Photo Adder")
                    root.geometry("300x200")

                    # Create and place the button
                    add_photos_button = tk.Button(root, text="Add Photos", command=add_photos)
                    add_photos_button.pack(pady=20)

                # Run the application
                root.mainloop()
                
            cv2.putText(img,str(count),(550,50),cv2.FONT_HERSHEY_COMPLEX,1,(255,0,0),2)
            
        cv2.imshow('Original',img)
        if (cv2.waitKey(1) & 0xFF) == ord('q'):
            cv2.destroyAllWindows()
            browse_text.set("RUN")
            break

    


root = tk.Tk(className=' Face Attendance Project')

# set window size
#gui.geometry("400x200")

#set window color
#root['bg']='white'

canvas = tk.Canvas(root, width=600, height=100)
canvas.grid(columnspan=3, rowspan=3)

#logo
logo = Image.open('E:/Face Attendance Project with GUI/Face Attendance Project with GUI/logo1.png')
logo = ImageTk.PhotoImage(logo)
logo_label = tk.Label(image=logo)
logo_label.image = logo
logo_label.grid(column=1, row=0)

#logo names 
logo = Image.open('E:/Face Attendance Project with GUI/Face Attendance Project with GUI/names.png')
logo = ImageTk.PhotoImage(logo)
logo_label = tk.Label(image=logo)
logo_label.image = logo
logo_label.grid(column=1, row=1)

#instructions
instructions = tk.Label(root, text="Click Button To Run and S for save new person and Press Q To Exit", font="Raleway")
instructions.grid(columnspan=3, column=0, row=2)

#browse button
browse_text = tk.StringVar()
browse_btn = tk.Button(root, textvariable=browse_text, command=lambda:open_file(), font="Raleway", bg="#20bebe", fg="white", height=1, width=15)
browse_text.set("RUN")
browse_btn.grid(column=1, row=3)

canvas = tk.Canvas(root, width=600, height=100)
canvas.grid(columnspan=3)

root.mainloop()
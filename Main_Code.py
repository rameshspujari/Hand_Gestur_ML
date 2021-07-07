from tkinter import *
import tkinter as tk
import math
from tkinter import filedialog
import os
import numpy as np
from PIL import ImageFile                            
ImageFile.LOAD_TRUNCATED_IMAGES = True
import imutils
from PIL import Image
from PIL import ImageTk
# global variables
bg = None
import time
from PIL import ImageTk, Image
from resizeimage import resizeimage
import cv2
global jk
jk=0

def imageFiltering(frame):

	#area of intereset(hand)
	roi = frame

	#applying gaussian blurr to reduce the noise
	blur = cv2.GaussianBlur(roi,(5,5),0)
	#converting from coloured to HSV
	hsv = cv2.cvtColor(blur,cv2.COLOR_BGR2HSV)

	#applying a mask which makes skin color white and others black
	mask = cv2.inRange(hsv,np.array([2,50,50]),np.array([20,255,255]))

	kernel = np.ones((5,5))
	#reducing noise
	filtered = cv2.GaussianBlur(mask,(3,3),0)
	ret,thresh = cv2.threshold(filtered,127,255,0) #thesholding the image
	thesh = cv2.GaussianBlur(thresh,(5,5),0) #reducing the noise
	#finding contours in the image. Will be used later in complex hull algorithm
	contours,hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)


	return roi,thresh,contours

def callback(selection):
    global xname
    xname=selection

    
class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)                 
        self.master = master

        # changing the title of our master widget      
        self.master.title("Project")
        
        self.pack(fill=BOTH, expand=1)
        w = tk.Label(root, 
		 text=" Sign Language Recognition Using Hand Gesture Recognition ",
		 fg = "light green",
		 bg = "dark green",
		 font = "Helvetica 20 bold italic")
        w.pack()
        w.place(x=200, y=0)
        # creating a button instance
        quitButton = Button(self,command=self.start, text="Start Camera",fg="blue",activebackground="dark red",width=20)
        quitButton.place(x=10, y=100)
        quitButton = Button(self,command=self.process,text="Process",fg="blue",activebackground="dark red",width=20)
        quitButton.place(x=10, y=200)
        #quitButton = Button(self,command=self.stopprocess, text="Stop Process",fg="blue",activebackground="dark red",width=20)
        #quitButton.place(x=10, y=300)
        quitButton = Button(self,command=self.stop,text="Stop Camera",activebackground="dark red",fg="blue",width=20)
        quitButton.place(x=10, y=300)
        


        load = Image.open("logo.png")
        render = ImageTk.PhotoImage(load)

        image2=Label(self, image=render,borderwidth=5, highlightthickness=5, height=180, width=180, bg='white')
        image2.image = render
        image2.place(x=180, y=70)

        image3=Label(self, image=render,borderwidth=5, highlightthickness=5, height=180, width=180, bg='white')
        image3.image = render
        image3.place(x=400, y=70)

        image4=Label(self, image=render,borderwidth=5, highlightthickness=5, height=180, width=180, bg='white')
        image4.image = render
        image4.place(x=650, y=70)
        
#       2nd row
        contents ="  Waiting for Results..."
        global T
        T = Text(self, height=19, width=25)
        T.pack()
        T.place(x=860, y=50)
        T.insert(END,contents)
        print(contents)
        
#       3rd row
        #image5.place(x=300, y=490)

#       Functions

    def start(self, event=None):
        contents ="Loading Image..."
        global T
        T = Text(self, height=19, width=25)
        #T.pack()
        T.place(x=860, y=50)
        T.insert(END,contents)
        print(contents)
        global cap,jk
        cap = cv2.VideoCapture(0)
        x = 100
        y = 100
        w = 250
        h = 250
        while True:
            ret,frame = cap.read() #read video frame by frame
            #img= cv2.resize(frame,(200,200))
            
            print('Reading frame by frame')
            time.sleep(.1)
            cv2.rectangle(frame,(y,x), (y+h,x+w), (0,255,0), 2)
            cv2.imshow("Frame", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                cimg=frame[y:y+h,x:x+w]
                cimg= cv2.resize(cimg,(200,200))
                cv2.imwrite('temp.jpg',cimg)
                break
        #self.from_array = Image.fromarray(frame)
        load = Image.open("temp.jpg")
        render = ImageTk.PhotoImage(load)
        image2=Label(self, image=render,borderwidth=5, highlightthickness=5, height=200, width=200, bg='white')
        image2.image = render
        image2.place(x=180, y=70)
        cv2.destroyAllWindows()
        contents="Image Captured successfully !!"
        
        T = Text(self, height=19, width=25)
        #T.pack()
        T.place(x=860, y=50)
        T.insert(END,contents)
        print(contents)
        
    def close_window(): 
        Window.destroy()
        
    def process(self, event=None):
        global T,rep,rep1
        global xname
        global data
        contents="Loading Massage ..."
        T = Text(self, height=19, width=25)
        #T.pack()
        T.place(x=860, y=50)
        T.insert(END,contents)
        roi,thresh,contours = imageFiltering(cv2.imread('temp.jpg')) #getting the filtered image
        #blank image which will be used to show the contours and defects
        drawing = np.zeros(roi.shape,np.uint8)
        #count_defects = 0
        
        #finding contour with max area
        contour = max(contours,key=lambda x: cv2.contourArea(x),default=0)
        #print(contour)
        #print(contour.shape)
        ch=0
        if (np.array(contour)).any()>=1:
            #convex hull. This creates a convex polygon.
            hull = cv2.convexHull(contour)

            #draw contours
            cv2.drawContours(drawing,[contour],-1,(0,255,0),0)
            cv2.drawContours(drawing,[hull],-1,(0,0,255),0)
            
            
            #finding defects in the convex polygon formed using convex hull algorithm
            hull = cv2.convexHull(contour,returnPoints = False)
            defects = cv2.convexityDefects(contour,hull)

            count_defects = 0 #defaults initially set to 0
            ch=1
            #finding defects and displaying them on the image
            for i in range(defects.shape[0]):
                    s,e,f,d = defects[i,0] #defect returns 4 arguments
                    #using start, end, far to find the defects location
                    start = tuple(contour[s][0])
                    end = tuple(contour[e][0])
                    far = tuple(contour[f][0])

                    #finding the angle of the defect using cosine law
                    a = math.sqrt((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2)
                    b = math.sqrt((far[0] - start[0]) ** 2 + (far[1] - start[1]) ** 2)
                    c = math.sqrt((end[0] - far[0]) ** 2 + (end[1] - far[1]) ** 2)
                    angle = (math.acos((b ** 2 + c ** 2 - a ** 2) / (2 * b * c)) * 180) / 3.14

                    #we know, angle between 2 fingers is within 90 degrees.
                    #so anything greater than that isn;t considered
                    if angle <= 90:
                            count_defects += 1
                            ch+=1
                            print(count_defects )
                            cv2.circle(drawing,far,5,[0,0,255],-1) #displaying defect

                    cv2.line(drawing,start,end,[0,255,0],2)
            #print(count_defects )
        else:
                ch=0
        

        #cv2.imshow("thresh",thresh)
        #cv2.imshow("drawing",drawing)
	#cv2.imshow("img",frame)
	
        #img= cv2.resize(thresh,(200,200), interpolation = cv2.INTER_AREA)
        self.from_array = Image.fromarray(thresh)
        render = ImageTk.PhotoImage(self.from_array)
        image3=Label(self, image=render,borderwidth=5, highlightthickness=5, height=180, width=180, bg='white')
        image3.image = render
        image3.place(x=400, y=70)
        
        #img= cv2.resize(drawing,(200,200), interpolation = cv2.INTER_AREA)
        self.from_array = Image.fromarray(drawing)
        render = ImageTk.PhotoImage(self.from_array)
        image4=Label(self, image=render,borderwidth=5, highlightthickness=5, height=180, width=180, bg='white')
        image4.image = render
        image4.place(x=650, y=70)
        if ch==0:
            contents="Image Processed successfully !!   and Recognized Sign is = No sign"
        else:
            contents="Image Processed successfully !!   and Recognized Sign is = "+str(count_defects+1)
        
        T = Text(self, height=19, width=25)
        #T.pack()
        T.place(x=860, y=50)
        T.insert(END,contents)
        print(contents)
            
    def stopprocess(self, event=None):
        contents =" Processing..."
        global T,rep,rep1
        global xname,data
        T = Text(self, height=19, width=25)
        #T.pack()
        from PIL import Image
        T.place(x=950, y=150)
        T.insert(END,contents)
        print(contents)
        
            
        
        img= cv2.resize(img,(200,200), interpolation = cv2.INTER_AREA)
        self.from_array = Image.fromarray(img)
        render = ImageTk.PhotoImage(self.from_array)
        image2=Label(self, image=render,borderwidth=5, highlightthickness=5, height=200, width=200, bg='white')
        image2.image = render
        image2.place(x=500, y=50)
        T = Text(self, height=20, width=25)
        #T.pack()
        T.place(x=950, y=150)
        T.insert(END,' successfully')
       
    def stop(self, event=None):
        
        global T,cap
        
        cap.release()
        T = Text(self, height=20, width=25)
        #T.pack()
        T.place(x=860, y=50)
        T.insert(END,'Camera cloased successfully')
        


     
root = Tk()
root.geometry("1100x450")
app = Window(root)
root.mainloop()

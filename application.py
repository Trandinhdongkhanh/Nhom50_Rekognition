import tkinter as tk
import os
from tkinter import filedialog
from PIL import ImageTk, Image
from rekognitionAPI import Rekognition
from tkinter.scrolledtext import ScrolledText
import json

WINDOW_WIDTH = 900
WINDOW_HEIGHT = 700
PIC_WIDTH = 450
PIC_HEIGHT = 300
BTN_WIDTH = 10
BTN_HEIGHT = 2
LOGO_WIDTH = 100


CLIENT = None
BUCKET = None
S3_RESOURCE = None
TABLE = None
DynamoDB = None
COLLECTION_ID = None
PARTITION_KEY = None

class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Nhận diện người nổi tiếng')
        self.geometry('900x700')
        self.resizable(False, False)

class App():
    def __init__(self):
        self.win = Window()
        self.upFrame = tk.Frame(self.win, height=350, width=900, bg='#808B96')
        self.downFrame = tk.Frame(self.win, height=350, width=900, bg='#7FB3D5')
        self.lbl_Pic = tk.Label(self.upFrame)
        self.lbl_resultPic = tk.Label(self.downFrame, bg='#17202A')
        self.st = ScrolledText(self.downFrame, wrap=tk.WORD)

        logo = ImageTk.PhotoImage(
            Image.open('Images/rekognition_logo.png').resize((WINDOW_WIDTH - (PIC_WIDTH + 40), 100), Image.ANTIALIAS))
        self.pic_logo = tk.Label(self.upFrame, image=logo)
        self.pic_logo.image = logo

        self.btn_upload = tk.Button(self.upFrame, width=BTN_WIDTH, height=BTN_HEIGHT, text='Upload', command=self.upload_img)
        self.btn_detectLabels = tk.Button(self.upFrame, width=BTN_WIDTH, height=BTN_HEIGHT, text='Detect Labels',
                                            command=self.detect_labels)
        self.btn_analyze = tk.Button(self.upFrame, width=BTN_WIDTH, height=BTN_HEIGHT, text='Detect Celebs',
                                            command=self.detect_celebs)
        self.btn_detectText = tk.Button(self.upFrame, width=BTN_WIDTH, height=BTN_HEIGHT, text='Detect Text',
                                            command=self.detect_text)
        self.btn_facialAnalysis = tk.Button(self.upFrame, width=BTN_WIDTH, height=BTN_HEIGHT, text='Facial Analysis',
                                            command=self.facial_analysis)

        self.upFrame.pack()
        self.downFrame.pack()

        self.lbl_Pic.place(x=20, y=20, width=PIC_WIDTH, height=PIC_HEIGHT)
        self.lbl_resultPic.place(x=20, y=20, width=PIC_WIDTH - 70, height=PIC_HEIGHT)
        self.pic_logo.place(x=PIC_WIDTH+30, y=20, width=WINDOW_WIDTH - (PIC_WIDTH + 40), height=100)

        self.btn_upload.place(x=650, y=160)
        self.st.place(x=430, y=20, width=PIC_WIDTH, height=PIC_HEIGHT)
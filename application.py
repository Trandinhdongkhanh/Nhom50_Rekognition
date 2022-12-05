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

    def upload_img(self):
        global file
        file = FileBrowser.browseFile()
        if file == '':        #If browseFile() return an empty string on cancel
            return
        img = Image.open(file).resize((PIC_WIDTH, PIC_HEIGHT), Image.ANTIALIAS)
        input_img = ImageTk.PhotoImage(img)
        self.lbl_Pic.configure(image=input_img)
        self.lbl_Pic.image = input_img
        self.display_btn()
        self.reset()

    def display_btn(self):
        self.btn_analyze.place(x=500, y=220)
        self.btn_detectLabels.place(x=600, y=220)
        self.btn_detectText.place(x=700, y=220)
        self.btn_facialAnalysis.place(x=800, y=220)

    def reset(self):
        self.lbl_resultPic.configure(image=None)
        self.lbl_resultPic.image = None
        self.st.configure(state='normal')
        self.st.delete(1.0, tk.END)
        self.st.configure(state='disabled')


    def detect_celebs(self):
        self.st.configure(state='normal')
        rekAPI = Rekognition(CLIENT)
        result = rekAPI.recognize_celebrities_v2(S3_RESOURCE, BUCKET, file)
        if(len(result) == 0):
            print("No celeb detected !")
            self.st.insert(tk.INSERT, "No celeb detected !")
            self.st.configure(state='disabled')
            return
        print(result)
        print()
        for obj in result:
            face_id = rekAPI.search_faces_by_image(COLLECTION_ID, BUCKET, obj)
            celeb = DynamoDB.query(TABLE, PARTITION_KEY, face_id)
            ID = 'ID: ' + celeb[0]['face_id'] + '\n'
            Gender = 'KnownGender: ' + celeb[0]['KnownGender'] + '\n'
            Info = 'Info: ' + celeb[0]['Info'] + '\n'
            Name = 'Name: ' + celeb[0]['Name'] + '\n'
            self.st.insert(tk.INSERT, Name)
            self.st.insert(tk.INSERT, ID)
            self.st.insert(tk.INSERT, Gender)
            self.st.insert(tk.INSERT, Info)
            self.st.insert(tk.INSERT, '\n')
            print('\nResult from DynamoDB: ')
            print(celeb)
            print('------------------------------------')

        self.st.configure(state='disabled')
        self.copy_img()

    def detect_labels(self):
        self.st.configure(state='normal')
        rekAPI = Rekognition(CLIENT)
        result = rekAPI.detect_labels(file)
        self.st.insert(tk.INSERT, result)
        self.st.configure(state='disabled')
        self.copy_img()

    def detect_text(self):
        self.st.configure(state='normal')
        rekAPI = Rekognition(CLIENT)
        result = rekAPI.detect_text(file)
        self.st.insert(tk.INSERT, result)
        self.st.configure(state='disabled')
        self.copy_img()

    def facial_analysis(self):
        self.st.configure(state='normal')
        rekAPI = Rekognition(CLIENT)
        result = rekAPI.facial_analysis(file)
        self.st.insert(tk.INSERT, result)
        self.st.configure(state='disabled')
        self.copy_img()

    def copy_img(self):
        img = Image.open(file).resize((PIC_WIDTH, PIC_HEIGHT), Image.ANTIALIAS)
        output_img = ImageTk.PhotoImage(img)
        self.lbl_resultPic.configure(image=output_img)
        self.lbl_resultPic.image = output_img

class FileBrowser():
    def __init__(self):
        pass

    @staticmethod
    def browseFile():
        currdir = os.getcwd()  # current python directory when open filedialog
        filename = filedialog.askopenfilename(initialdir=currdir, title='Please select an image', filetypes=[
            ("image", ".jpeg"),
            ("image", ".png"),
            ("image", ".jpg"),
        ])
        return filename
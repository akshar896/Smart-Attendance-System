import cv2
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from datetime import datetime
import threading
import subprocess
import os
import face_recognition
import pickle



class CameraApp:
    def __init__(self, window, window_title, video_source=0):
        self.window = window
        self.window.title(window_title)

        self.video_source = video_source
        self.cap = cv2.VideoCapture(self.video_source)

        self.canvas = tk.Canvas(window, width=self.cap.get(cv2.CAP_PROP_FRAME_WIDTH), height=self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.canvas.pack()

        self.btn_capture = tk.Button(window, text="Capture", command=self.capture_image, bg='#cccccc')
        self.btn_capture.pack(pady=10)

        self.update()
        self.window.mainloop()

    def update(self):
        ret, frame = self.cap.read()
        if ret:
            self.photo = self.convert_to_tkinter_image(frame)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)
        self.window.after(10, self.update)

    def capture_image(self):
        ret, frame = self.cap.read()
        if ret:
            file_name = input()
            save_path = os.path.join('training_images', f'{file_name}.jpg')
            cv2.imwrite(save_path, frame)

            print(f"Image captured and saved as {file_name}")
        path = 'training_images'
        images = []
        classNames = []
        myList = os.listdir(path)
        print(myList)

        for cl in myList:
            curImg = cv2.imread(f'{path}/{cl}')
            images.append(curImg)
            classNames.append(os.path.splitext(cl)[0])
        print(classNames)

        # Load saved encodings if available, otherwise create and save them
        encodings_file = 'encodings.pkl'

        encodeListKnown = []
        for image in images:
            face_encodings = face_recognition.face_encodings(image)
            if len(face_encodings) > 0:
                encodeListKnown.append(face_encodings[0])
            with open(encodings_file, 'wb') as f:
                pickle.dump(encodeListKnown, f)
        print('Encodings saved to file.')

    def convert_to_tkinter_image(self, frame):
        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(rgb_image)
        photo = ImageTk.PhotoImage(image=pil_image)
        return photo

    def __del__(self):
        if self.cap.isOpened():
            self.cap.release()
    def start_external_script(self):
        external_script_thread = threading.Thread(target=self.run_external_script)
        external_script_thread.start()

    def run_external_script(self):
        script_path = 'add new person.py'  # Replace with the actual path to your script
        subprocess.run(['python', script_path])


if __name__ == "__main__":
    # Specify the video source (use 0 for the default camera)
    video_source = 0

    # Create the application window
    app_window = tk.Tk()
    app = CameraApp(app_window, "Camera App", video_source)

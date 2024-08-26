import os
import tkinter as tk
from tkinter import ttk, messagebox
import cv2
import pickle
import face_recognition

def remove_person_gui():
    def remove_selected_person():
        selected_person = combo_person.get()

        if selected_person:
            try:
                os.remove(f"training_images/{selected_person}.jpg")
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
                messagebox.showinfo("Success", f"{selected_person} removed successfully!")
                refresh_dropdown()
            except FileNotFoundError:
                messagebox.showerror("Error", f"Image file not found for {selected_person}!")

    def refresh_dropdown():
        # Refresh the dropdown menu with updated names from the folder
        person_names = [os.path.splitext(cl)[0] for cl in os.listdir("training_images")]
        combo_person['values'] = person_names

    root = tk.Tk()
    root.title("Remove Person from Training Images")

    # Create a style and configure the combobox style
    style = ttk.Style()
    style.configure('Custom.TCombobox', fieldbackground='#cccccc', background='#cccccc')

    label_select_person = ttk.Label(root, text="Select person to remove:")
    label_select_person.pack(pady=10)

    # Fetch names from the folder "training_images"
    person_names = [os.path.splitext(cl)[0] for cl in os.listdir("training_images")]

    combo_person = ttk.Combobox(root, values=person_names, state="readonly", style='Custom.TCombobox')
    combo_person.pack(pady=10)

    button_remove_person = tk.Button(root, text="Remove Person", command=remove_selected_person, bg='#cccccc')
    button_remove_person.pack(pady=10)

    refresh_dropdown()  # Initial population of the dropdown

    root.mainloop()

# Call the function to display the GUI
remove_person_gui()

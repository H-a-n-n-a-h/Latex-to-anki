############################################################################
# FRONT END
############################################################################
import tkinter as tk
from tkinterdnd2 import TkinterDnD, DND_FILES
from Backend import auto_unzip, find_tex_files, get_content, process, save_as_array, write_html_maths_all

user_input = ""

#-------------- Functions to call ------------------------
def handle_file_drop(event):
    # Get the full path of the dropped file
    global user_input
    user_input = event.data.strip()
    if user_input[0] == "{":
        user_input = user_input[1:-1]
    print(f"\n user input is \"{user_input}\". \n")
    print(f"Short is \"{user_input.split('/')[-1][0:-4]}\".\n")
    folder_label.config(text=f"Path: {user_input}")

def convert_html_click():
    global user_input
    print("\n \n Starting HTML conversion... \n \n")
    print(f"\n user input is {user_input}. \n")
    folder_path = auto_unzip(user_input)
    print(f"Folder path to unzipped is{folder_path}")
    tex_files = find_tex_files(folder_path)
    for tex_file in tex_files:
        text = get_content(tex_file)
        process(text)
    write_html_maths_all()
    save_as_array()
    print("...HTML done! :)!")

def testing_mode():
    global user_input
    print("Starting testing mode")
    test_path = "testing_files"
    test_tex_files = find_tex_files(test_path)
    for tex_file in test_tex_files:
        text = get_content(tex_file)
        process(text)
    write_html_maths_all()
    print("...HTML testing done! :)!")

#-------------- set GUI  ------------------------
def set_root():
    root = TkinterDnD.Tk()  # Use TkinterDnD's Tk class instead of tkinter.Tk
    root.title("Drag-and-Drop File Example")
    root.geometry("500x300")
    return root

root = set_root()

instruction_label = tk.Label(root, text="Drag and drop here", font=(14))
instruction_label.pack()
folder_label = tk.Label(root, text="Path: (No file dropped)", font=(12))
folder_label.pack(pady=10)

htmlconvert = tk.Button(root, text="Card HTML Convert", command=convert_html_click)
htmlconvert.pack(pady=10)

root.drop_target_register(DND_FILES) # Enable drag-and-drop 
root.dnd_bind("<<Drop>>", handle_file_drop)
root.mainloop() # starts program loop

#testing_mode()
#save_as_array()
import os
import datetime
import PIL.Image
import time
timestamp_now = time.time()
import tkinter as tk

def tk_open_image(image_path):
    from PIL import ImageTk, Image

    # This creates the main window of an application
    window = tk.Tk()
    window.title("Join")
    window.geometry("300x300")
    window.configure(background='grey')

    path = image_path

    # Creates a Tkinter-compatible photo image, which can be used everywhere Tkinter expects an image object
    print(image_path)
    img = ImageTk.PhotoImage(Image.open(path))

    # The Label widget is a standard Tkinter widget used to display a text or image on the screen.
    panel = tk.Label(window, image=img)

    # The Pack geometry manager packs widgets in rows or columns.
    panel.pack(side="bottom", fill="both", expand="yes")

    # Start the GUI
    window.mainloop()

def open_image(image_path):
    image = PIL.Image.open(image_path)
    image.show()
def get_latest_image(folder_path):
    latest_jpeg = None
    latest_timestamp = timestamp_now
    for file in os.listdir(folder_path):
        if file.endswith(".jpeg") or file.endswith(".png") or file.endswith(".jpg"):
            timestamp = os.path.getmtime(os.path.join(folder_path, file))
            if latest_timestamp is None or timestamp > latest_timestamp:

                latest_jpeg = file
                latest_timestamp = timestamp
    return latest_jpeg

def open_latest_image(path = "~/Desktop/example"):
    folder_path = path
    latest_image = get_latest_image(folder_path)
    if latest_image is not None:
        print(f"The latest Image in the folder is {latest_image}")
    else:
        print("There are no Images in the folder")
        return None
    img_path = os.path.join(folder_path, latest_image)
    return img_path

def run_auto_open(path = "~/Desktop/example", time_period = 0.5):
    viewed_images = []
    while True:
        time.sleep(time_period)
        latest_image_path = open_latest_image(path=path)
        if latest_image_path and latest_image_path not in viewed_images:
            open_image(latest_image_path)
            viewed_images.append(latest_image_path)

def  main():
    run_auto_open(path =  "/Users/trapbookpro/Desktop/example")

if __name__ == "__main__":
    main()
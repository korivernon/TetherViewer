
import tkinter as tk
from PIL import ImageTk, Image
# This creates the main window of an application
def main():
    window = tk.Tk()
    window.title("Join")
    window.geometry("300x300")
    window.configure(background='grey')

    path = "kori.png"

    # Creates a Tkinter-compatible photo image, which can be used everywhere Tkinter expects an image object
    photo = ImageTk.PhotoImage(Image.open(path))

    # The Label widget is a standard Tkinter widget used to display a text or image on the screen.
    label = tk.Label(window, image=photo)
    label.image = photo

    # The Pack geometry manager packs widgets in rows or columns.
    label.pack()

    # Start the GUI
    window.mainloop()
main()
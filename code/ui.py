import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageTk
import os

class DesktopUI(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Desktop UI")
        self.geometry("800x600")

        self.UPLOADED_PICTURE = None
        self.UPLOADED_HINT = None
        

        # Left Sidebar
        self.left_sidebar = tk.Frame(self, bg="grey", width=240)  # Adjusted width
        self.left_sidebar.pack(side=tk.LEFT, fill=tk.Y)


        # Main Content
        self.main_content = tk.Frame(self, bg="white")
        self.main_content.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)


        # # Canvas for displaying selected image
        # self.canvas = tk.Canvas(self.main_content, bg="white", width=400, height=400)
        # self.canvas.pack(pady=20)

        self.canvas1 = tk.Canvas(self.main_content, bg="white", width=400, height=400)
        self.canvas1.grid(row=0, column=0, pady=20, padx=20)

        self.canvas2 = tk.Canvas(self.main_content, bg="white", width=400, height=400)
        self.canvas2.grid(row=0, column=1, pady=20, padx=20)
        

        self.load_images()
        
        self.create_buttons()

        self.unshow_button = ttk.Button(self, text="Unshow Image", command=self.unshow_image)
        self.unshow_button.pack(side=tk.RIGHT, padx=10, pady=10)
        self.unshow_button.pack_forget()  # Initially hidden



    def load_images(self):
        assets_folder = "assets/results"
        if os.path.exists(assets_folder):
            image_files = [f for f in os.listdir(assets_folder) if f.endswith(('.png', '.jpg', '.jpeg'))]

            for image_file in image_files:
                image_path = os.path.join(assets_folder, image_file)
                image = Image.open(image_path)
                image.thumbnail((200, 200))
                tk_image = ImageTk.PhotoImage(image)

                label = ttk.Label(self.left_sidebar, image=tk_image, padding=10)
                label.image = tk_image
                label.pack(anchor=tk.W)

                label.bind("<Button-1>", lambda event, path=image_path: self.show_image(path))

    def show_image(self, image_path):
        # Hide buttons and show the unshow button
        # for child in self.main_content.winfo_children():
        #     child.pack_forget()

        # self.unshow_button.pack()

        # Display the selected image on the canvas
        image = Image.open(image_path)
        image = image.resize((400, 400))
        self.tk_image = ImageTk.PhotoImage(image)
        self.canvas1.create_image(0, 0, anchor=tk.NW, image=self.tk_image)
        self.canvas1.image = self.tk_image



    def unshow_image(self):
        # Clear canvas and show buttons
        self.canvas.delete("all")
        self.unshow_button.pack_forget()

        # Show the buttons in the main content area
        self.create_buttons()


    def create_buttons(self):
        plus_image = Image.open("assets/UI assets/plus.jpg")
        plus_image.thumbnail((100, 100))
        plus_tk_image = ImageTk.PhotoImage(plus_image)

        btn1 = ttk.Button(self.main_content, text="Upload Picture", image=plus_tk_image, compound=tk.TOP, command=self.upload_picture)
        btn1.image = plus_tk_image
        btn1.grid(row=1, column=0, padx=(0, 20))

        btn2 = ttk.Button(self.main_content, text="Upload Hint", image=plus_tk_image, compound=tk.TOP, command=self.upload_hint)
        btn2.image = plus_tk_image
        btn2.grid(row=1, column=1, padx=(20, 0))

        btn3 = ttk.Button(self.main_content, text='Solve',command=self.solve)
        btn3.grid(row=1, column=2, padx=(20, 0))
   
    

    def upload_picture(self):
        
        file_path = filedialog.askopenfilename()
        image = Image.open(file_path)
        image = image.resize((400, 400))
        self.tk_image = ImageTk.PhotoImage(image)
        self.UPLOADED_PICTURE = self.tk_image
        self.canvas1.create_image(0, 0, anchor=tk.NW, image=self.tk_image)
        self.canvas1.image = self.tk_image


    def upload_hint(self):
        file_path = filedialog.askopenfilename()
        image = Image.open(file_path)
        image = image.resize((400, 400))
        self.tk_image = ImageTk.PhotoImage(image)
        self.UPLOADED_HINT = self.tk_image
        self.canvas2.create_image(0, 0, anchor=tk.NW, image=self.tk_image)
        self.canvas2.image = self.tk_image

    def solve(self):
        # use here UPLOADED_PICTURE & UPLOADED_HINT from up guys
        None


if __name__ == "__main__":
    app = DesktopUI()
    app.mainloop()        
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageTk
from pathlib import Path
from tkinter import messagebox
import os
from gridPuzzle import solve_grid_puzzle


class GUI(tk.Tk):
    def __init__(self):
        super().__init__()

        self.tk_image = None
        self.UPLOADED_PICTURE = None
        self.img_path = None

        self.title("Desktop UI")
        self.geometry("1280x720")

        # Left Sidebar Scrollbar
        self.left_scrollbar = tk.Scrollbar(self, orient=tk.VERTICAL)
        self.left_scrollbar.pack(side=tk.LEFT, fill=tk.Y)

        # Left Sidebar Canvas
        self.left_canvas = tk.Canvas(self, bg="grey", width=200, height=720, yscrollcommand=self.left_scrollbar.set)
        self.left_canvas.pack(side=tk.LEFT, fill=tk.Y)
        self.left_scrollbar.config(command=self.left_canvas.yview)

        # Left Sidebar Frame
        self.left_sidebar = tk.Frame(self.left_canvas, bg="grey", width=320)
        self.left_canvas.create_window((0, 0), window=self.left_sidebar, anchor=tk.NW)

        # Left Sidebar Resize
        self.left_canvas.bind("<Configure>", self.on_left_sidebar_configure)

        # Main Content
        self.main_content = tk.Frame(self, bg="white")
        self.main_content.pack(side=tk.LEFT, fill=tk.Y, expand=True)

        # Sup Frame
        self.control = tk.Frame(self, bg="gray", width=320, height=320)
        self.control.pack(side=tk.RIGHT, fill=tk.Y, expand=True)

        # Image display
        self.canvas1 = tk.Canvas(self.main_content, bg="white", width=640, height=320)
        self.canvas1.grid(row=0, column=0, pady=20, padx=20)
        self.canvas2 = tk.Canvas(self.main_content, bg="white", width=640, height=320)
        self.canvas2.grid(row=1, column=0, pady=20, padx=20)

        # Control
        self.labelX = tk.Label(self.control, text='N cut on X', font=('Arial', 14))
        self.labelX.grid(row=1, column=0, padx=20, pady=10)
        self.labelX = tk.Label(self.control, text='N cut on Y', font=('Arial', 14))
        self.labelX.grid(row=1, column=1, padx=20, pady=10)

        self.textX = tk.Text(self.control, height=1, width=10, font=('Arial', 16))
        self.textX.grid(row=2, column=0, padx=20, pady=20)
        self.textY = tk.Text(self.control, height=1, width=10, font=('Arial', 16))
        self.textY.grid(row=2, column=1, padx=20, pady=20)

        self.load_images()
        self.initiate_controls()

    def load_images(self):
        for widget in self.left_sidebar.winfo_children():
            widget.destroy()
        assets_folder = "results"
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
        image = Image.open(image_path)
        image = image.resize((640, 320))
        self.tk_image = ImageTk.PhotoImage(image)
        self.canvas2.create_image(0, 0, anchor=tk.NW, image=self.tk_image)
        self.canvas2.image = self.tk_image

    def initiate_controls(self):

        btn1 = ttk.Button(self.control, text="Upload Picture", command=self.upload_picture)
        btn1.grid(row=0, column=0, padx=20, pady=20)

        btn2 = ttk.Button(self.control, text="Refresh", command=self.load_images)
        btn2.grid(row=0, column=1, padx=20, pady=20)

        btn3 = ttk.Button(self.control, text='Solve Grid', command=self.solve_grid)
        btn3.grid(row=3, column=0, padx=20, pady=20)

        btn4 = ttk.Button(self.control, text='Hint Solve', command=self.solve_grid)
        btn4.grid(row=3, column=1, padx=20, pady=20)

        btn5 = ttk.Button(self.control, text='Solve puzzle', command=self.solve_grid)
        btn5.grid(row=4, column=0, padx=20, pady=20)

        btn6 = ttk.Button(self.control, text='hint Solve', command=self.solve_grid)
        btn6.grid(row=4, column=1, padx=20, pady=20)

    def upload_picture(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", (".png", ".jpg", ".jpeg"))])
        fileTest = Path(file_path)
        if not fileTest.is_file():
            messagebox.askyesno('No Selection!', message='You haven\'t selected an image.')
        self.img_path = file_path
        print(self.img_path)
        image = Image.open(file_path)
        # self.UPLOADED_PICTURE = image
        image = image.resize((640, 320))
        self.tk_image = ImageTk.PhotoImage(image)
        self.UPLOADED_PICTURE = self.tk_image
        self.canvas1.create_image(0, 0, anchor=tk.NW, image=self.tk_image)
        self.canvas1.image = self.tk_image

    def solve_grid(self):
        x_cut = int(self.textX.get('1.0', tk.END))
        y_cut = int(self.textY.get('1.0', tk.END))
        fileTest = Path(self.img_path)
        if not fileTest.is_file():
            messagebox.askyesno(title='Image not Found', message='You haven\'t selected an image or no cut entered!?')
        else:
            solve_grid_puzzle(self.img_path, x_cut, y_cut)
        self.load_images()

    def on_left_sidebar_configure(self, event):
        self.left_canvas.configure(scrollregion=self.left_canvas.bbox("all"))


if __name__ == "__main__":
    app = GUI()
    app.mainloop()

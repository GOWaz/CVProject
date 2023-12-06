import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk, Image

# Global variables to store original and resized images
original_image = None
resized_image = None
hint_image = None
resized_hint = None


def open_image():
    global original_image, resized_image
    file_path = filedialog.askopenfilename()
    if file_path:
        original_image = Image.open(file_path)
        resized_image = original_image.copy()
        resized_image.thumbnail((300, 300))  # Resize for display
        display_image(resized_image, image_label)


def open_hint():
    global hint_image, resized_hint
    file_path = filedialog.askopenfilename()
    if file_path:
        hint_image = Image.open(file_path)
        resized_hint = hint_image.copy()
        resized_hint.thumbnail((300, 300))  # Resize for display
        display_image(resized_hint, hint_label)


def display_image(img, label):
    img = ImageTk.PhotoImage(img)
    label.config(image=img)
    label.image = img  # Keep a reference to the image to prevent garbage collection


def solve():
    # Use 'original_image' and 'hint_image' for solving logic or any other processing
    if original_image is not None and hint_image is not None:
        # Example: Printing the dimensions of the original image and hint image
        print("Original Image Dimensions:", original_image.size)
        print("Hint Image Dimensions:", hint_image.size)
        # Implement your solving logic here using 'original_image' and 'hint_image'


# Create the main window
root = tk.Tk()
root.title("Image Solver")

# Create labels to display images
image_label = tk.Label(root)
image_label.pack(side=tk.LEFT, padx=10, pady=10)

hint_label = tk.Label(root)
hint_label.pack(side=tk.RIGHT, padx=10, pady=10)

# Create buttons
upload_button = tk.Button(root, text="Upload Picture", command=open_image)
upload_button.pack(padx=10, pady=5)

hint_button = tk.Button(root, text="Upload Hint", command=open_hint)
hint_button.pack(padx=10, pady=5)

solve_button = tk.Button(root, text="Solve", command=solve)
solve_button.pack(padx=10, pady=5)

# Run the application
root.mainloop()

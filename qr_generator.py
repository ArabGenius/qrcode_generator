import tkinter as tk
from tkinter import messagebox, filedialog  # Import filedialog properly
import qrcode
from PIL import Image, ImageTk

def generate_qr_code(save=False):
    try:
        # Get the input (link or text) from the input field
        data = entry.get()

        if not data:
            messagebox.showwarning("Input Error", "Please enter some text or a link!")
            return

        # Create QR code instance
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )

        # Add data to the QR code
        qr.add_data(data)
        qr.make(fit=True)

        # Create an image from the QR Code instance
        img = qr.make_image(fill_color="black", back_color="white").convert("RGB")  # Convert to RGB

        if save:
            # Ask the user where to save the QR code
            file_path = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG files", "*.png"), ("All files", "*.*")],
                title="Save QR Code As"
            )

            if not file_path:  # User canceled the save dialog
                return

            # Save the image
            img.save(file_path)
            messagebox.showinfo("Success", f"QR code saved as {file_path}")

        # After generating the QR code, resize the window
        root.geometry("400x500")  # Resize window to fit QR code properly

        # Display the QR code in the GUI
        img = img.resize((200, 200), Image.LANCZOS)  # FIX: Ensure resizing works with RGB
        img_tk = ImageTk.PhotoImage(img)
        qr_label.config(image=img_tk)
        qr_label.image = img_tk  # Keep a reference

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def clear_fields():
    entry.delete(0, tk.END)  # Clear the input field
    qr_label.config(image=None)  # Clear the QR code display
    root.geometry("400x200")  # Reset window size when clearing

# Create the main window
root = tk.Tk()
root.title("QR Code Generator [By Ahmed]")

# Set initial window size
window_width = 400
window_height = 200
root.geometry(f"{window_width}x{window_height}")

# Center the window on the screen
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
center_x = (screen_width - window_width) // 2
center_y = (screen_height - window_height) // 2
root.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")

root.resizable(False, False)  # Disable resizing

# Create and place widgets
label = tk.Label(root, text="Enter text or a link to convert to QR code:")
label.pack(pady=10)

entry = tk.Entry(root, width=50)
entry.pack(pady=10)

# Frame to hold buttons
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

# Generate and Save QR Code Button
generate_button = tk.Button(button_frame, text="Generate and Save QR Code", command=lambda: generate_qr_code(save=True))
generate_button.pack(side=tk.LEFT, padx=5)

# View QR Code Button (without saving)
view_button = tk.Button(button_frame, text="View QR Code", command=lambda: generate_qr_code(save=False))
view_button.pack(side=tk.LEFT, padx=5)

# Clear Button
clear_button = tk.Button(root, text="Clear", command=clear_fields)
clear_button.pack(pady=10)

# Add a label to display the QR code
qr_label = tk.Label(root)
qr_label.pack(pady=20)

# Run the application
root.mainloop()

import tkinter as tk
from tkinter import font
import re
from tkinter import END, DISABLED, NORMAL

# Function to clean input by removing newlines and extra spaces
def clean_input(input_text):
    return input_text.strip()

# Function to display an error message in red for 2 seconds
def show_error_message(widget, message):
    # Insert the error message in red
    widget.config(fg="red")
    widget.insert("1.0", message)
    
    # Clear the error message after 2 seconds and reset the text color to white
    widget.after(2000, lambda: [widget.delete("1.0", "end"), widget.config(fg="white")])

    

# Function to shift focus to the next input field
def focus_next_widget(event):
    current_widget = event.widget
    widget_name = current_widget.winfo_name()  # Get the name of the widget

    # Clean the text from the current widget
    cleaned_text = clean_input(current_widget.get("1.0", "end"))

    # Clear and reinsert cleaned text
    current_widget.delete("1.0", "end")
    current_widget.insert("1.0", cleaned_text)

    # Prevent shifting focus if the field is empty
    if cleaned_text == "":
        print(f"[Warning] {widget_name} cannot be empty!")
        return

    # Define the barcode pattern: "TN" followed by exactly 14 digits
    barcode_pattern = r"^TN\d{14}$"

    # Logic to check if the cleaned_text follows the barcode format when current widget is box_barcode
    if widget_name in ["box_barcode", "device_barcode"] and not re.match(barcode_pattern, cleaned_text):
        print(f"[Error] {widget_name} must start with 'TN' followed by 14 digits.")
        current_widget.delete("1.0", "end")  # Clear the content
        show_error_message(current_widget, "Invalid QR code")
        return  # Do not shift focus if the condition is not met

    # Define the MAC address pattern
    mac_pattern = r"^([0-9A-Fa-f]{2}:){5}([0-9A-Fa-f]{2})$"

    # Logic to check if the cleaned_text follows MAC address format when current widget is box_qr or device_qr
    if widget_name in ["box_qr", "device_qr"] and not re.match(mac_pattern, cleaned_text):
        print(f"[Error] {widget_name} must start with 'TN'.")
        current_widget.delete("1.0", "end")  # Clear the content
        show_error_message(current_widget, "Invalid QR code")
        # current_widget.config(fg="white")
        return  # Do not shift focus if the condition is not met

    # Move focus based on the widget name
    widget_focus_map = {
        "box_qr": entry_device_qr,
        "entry_device_qr": clear_button
    }
    next_widget = widget_focus_map.get(widget_name)
    if next_widget:
        next_widget.focus()
    else:
        check_barcodes()
        clear_button.focus()

# # Function to check if the QR codes match

# Function to check if the barcodes and QR codes match (case-insensitive)
def check_barcodes():
    print("[debug] check_barcodes is triggered.")
    # box_barcode = clean_input(entry_box_barcode.get("1.0", "end")).replace("\n", "").replace(" ", "").upper()
    box_qr = clean_input(entry_box_qr.get("1.0", "end")).replace("\n", "").replace(" ", "").upper()
    # device_barcode = clean_input(entry_device_barcode.get("1.0", "end")).replace("\n", "").replace(" ", "").upper()
    device_qr = clean_input(entry_device_qr.get("1.0", "end")).replace("\n", "").replace(" ", "").upper()

    # Check if the barcodes and QR codes match
    qr_code_match = (box_qr == device_qr)

    # Display results
    result_value_2.config(text="Match" if qr_code_match else "No Match", fg="green" if qr_code_match else "red")


# Function to clear all inputs and results
def clear_all():
    for entry in [entry_box_qr, entry_device_qr]:
        entry.delete("1.0", "end")

    # Reset the result labels
    # result_value_1.config(text="n/a", fg="grey")
    result_value_2.config(text="n/a", fg="grey")

    # Set focus back to the first input field
    entry_box_qr.focus()

# Function to change the color of the Next Battery button when focused
def on_focus_in(event):
    event.widget.config(bg="lightblue")

def on_focus_out(event):
    event.widget.config(bg="SystemButtonFace")  # Default button color for MacOS

# Set up the main GUI window
root = tk.Tk()
root.title("QR Code Reader")
root.geometry("500x250")  # Adjusted the width of the window for a narrower look
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)  # Add a second column for the Next Battery button

monospace_font = font.Font(family="Courier", size=16)

# Create input fields and labels
def create_label(text, row):
    label = tk.Label(root, text=text, font=monospace_font, anchor='w')
    label.grid(row=row, column=0, sticky='w', padx=10, pady=5, columnspan=2)
    return label

def create_entry(name, row):
    entry = tk.Text(root, height=2, width=40, font=monospace_font, name=name)  # Narrower text fields
    entry.grid(row=row, column=0, padx=10, pady=5, sticky='ew', columnspan=2)
    entry.bind("<Return>", lambda event: focus_next_widget(event))
    return entry

create_label("1. Scan Box QR Code:", 3)
entry_box_qr = create_entry("box_qr", 4)

create_label("2. Scan Device QR Code:", 7)
entry_device_qr = create_entry("device_qr", 8)

# Create the Next Battery button (Top-right)
clear_button = tk.Button(root, text="Next Battery", command=clear_all, height=2, width=20, font=monospace_font)
clear_button.grid(row=0, column=1, padx=5, pady=5, sticky='ne')  # Aligned to the top-right
clear_button.bind("<FocusIn>", on_focus_in)
clear_button.bind("<FocusOut>", on_focus_out)

# Create a result frame for displaying barcode and QR code match results (Top-left)
result_frame = tk.Frame(root, bd=2, relief="solid", bg="#070015")  # Added border and background color
result_frame.grid(row=0, column=0, padx=20, pady=10, sticky='nw')  # Aligned to the top-left
result_frame.grid_columnconfigure(0, weight=1)
result_frame.grid_columnconfigure(1, weight=1)

# Create result labels and values
result_label_2 = tk.Label(result_frame, text="QR Code:", font=monospace_font, bg="#070015", fg="white")
result_value_2 = tk.Label(result_frame, text="n/a", font=monospace_font, bg="#070015", fg="grey")
result_label_2.grid(row=1, column=0, sticky='w', padx=0)
result_value_2.grid(row=1, column=1, sticky='w', padx=50)

# Set initial focus
entry_box_qr.focus_set()

# Start the Tkinter event loop
root.mainloop()

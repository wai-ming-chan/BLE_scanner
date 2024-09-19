import tkinter as tk
from tkinter import font

# Function to clean input by removing newlines and extra spaces
def clean_input(input_text):
    return input_text.strip()

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
    
    # Move focus based on the widget name
    widget_focus_map = {
        "box_barcode": entry_box_qr,
        "box_qr": entry_device_barcode,
        "device_barcode": entry_device_qr
    }
    next_widget = widget_focus_map.get(widget_name)
    if next_widget:
        next_widget.focus()
    else:
        check_barcodes()
        clear_button.focus()

# Function to check if the barcodes and QR codes match
def check_barcodes():
    print("[debug] check_barcodes is triggered.")
    box_barcode = clean_input(entry_box_barcode.get("1.0", "end")).replace("\n", "").replace(" ", "")
    box_qr = clean_input(entry_box_qr.get("1.0", "end")).replace("\n", "").replace(" ", "")
    device_barcode = clean_input(entry_device_barcode.get("1.0", "end")).replace("\n", "").replace(" ", "")
    device_qr = clean_input(entry_device_qr.get("1.0", "end")).replace("\n", "").replace(" ", "")

    # Check if the barcodes and QR codes match
    barcode_match = (box_barcode == device_barcode)
    qr_code_match = (box_qr == device_qr)

    # Display results
    result_value_1.config(text="Match" if barcode_match else "No Match", fg="green" if barcode_match else "red")
    result_value_2.config(text="Match" if qr_code_match else "No Match", fg="green" if qr_code_match else "red")

# Function to clear all inputs and results
def clear_all():
    for entry in [entry_box_barcode, entry_box_qr, entry_device_barcode, entry_device_qr]:
        entry.delete("1.0", "end")

    # Reset the result labels
    result_value_1.config(text="n/a", fg="grey")
    result_value_2.config(text="n/a", fg="grey")

    # Set focus back to the first input field
    entry_box_barcode.focus()

# Function to change the color of the Next Battery button when focused
def on_focus_in(event):
    event.widget.config(bg="lightblue")

def on_focus_out(event):
    event.widget.config(bg="SystemButtonFace")  # Default button color for MacOS

# Set up the main GUI window
root = tk.Tk()
root.title("Barcode Reader")
root.geometry("500x450")  # Adjusted the width of the window for a narrower look
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

# Create barcode and QR code fields
create_label("1. Scan Box Barcode:", 1)
entry_box_barcode = create_entry("box_barcode", 2)

create_label("2. Scan Box QR Code:", 3)
entry_box_qr = create_entry("box_qr", 4)

create_label("3. Scan Device Barcode:", 5)
entry_device_barcode = create_entry("device_barcode", 6)

create_label("4. Scan Device QR Code:", 7)
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
result_label_1 = tk.Label(result_frame, text="Barcode:", font=monospace_font, bg="#070015", fg="white")
result_value_1 = tk.Label(result_frame, text="n/a", font=monospace_font, bg="#070015", fg="grey")
result_label_1.grid(row=0, column=0, sticky='w', padx=5)
result_value_1.grid(row=0, column=1, sticky='w', padx=50)

result_label_2 = tk.Label(result_frame, text="QR Code:", font=monospace_font, bg="#070015", fg="white")
result_value_2 = tk.Label(result_frame, text="n/a", font=monospace_font, bg="#070015", fg="grey")
result_label_2.grid(row=1, column=0, sticky='w', padx=5)
result_value_2.grid(row=1, column=1, sticky='w', padx=50)

# Set initial focus
entry_box_barcode.focus_set()

# Start the Tkinter event loop
root.mainloop()

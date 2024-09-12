import tkinter as tk
from tkinter import messagebox
from tkinter import font
import Penguin_scanner as p_scanner

# Function to clean input by removing \n characters
def clean_input(input_text):
    return input_text.replace('\n', '').strip()

# Function to shift focus to the next input field
def focus_next_widget(event):
    event.widget.tk_focusNext().focus()

# Function to query the scanner and process the results
def query_scanner():
    # Extract and clean the input data
    box_barcode = clean_input(entry_box_barcode.get("1.0", "end"))
    box_qr = clean_input(entry_box_qr.get("1.0", "end"))
    device_barcode = clean_input(entry_device_barcode.get("1.0", "end"))
    device_qr = clean_input(entry_device_qr.get("1.0", "end"))
    
    # Call the scanner using the device QR code
    try:
        MAC, PN, SoC, Temperature = p_scanner.run_scanner(device_qr)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to run scanner: {e}")
        return

    # Check if MAC and QR codes match
    qr_code_match = (box_qr == device_qr and device_qr == MAC)
    
    # Check if Barcodes match
    barcode_match = (box_barcode == device_barcode and device_barcode == PN)

    # Display the results in a left-aligned, two-column format
    result_label_1.config(text=f"Barcode:")
    # print "Match" if it is a match, else print "No Match"
    # result_value_1.config(text=f"{'Match' if barcode_match else 'No Match'}")
    result_value_1.config(
        text="Match" if barcode_match else "No Match", 
        fg="green" if barcode_match else "red"
    )
    
    result_label_2.config(text=f"QR Code:")
    # print "Match" if it is a match, else print "No Match"
    # result_value_2.config(text=f"{'Match' if qr_code_match else 'No Match'}")
    result_value_2.config(
        text="Match" if qr_code_match else "No Match", 
        fg="green" if qr_code_match else "red"
    )
    
    
    result_label_3.config(text=f"SN:")
    result_value_3.config(text=f"{PN}")
    
    result_label_4.config(text=f"MAC:")
    result_value_4.config(text=f"{MAC}")
    
    result_label_5.config(text=f"SoC:")
    result_value_5.config(text=f"{SoC}%")
    
    result_label_6.config(text=f"Temp:")
    result_value_6.config(text=f"{Temperature}F")

# Function to clear all inputs and results, then focus on the first textbox
def clear_all():
    # Clear all the textboxes
    entry_box_barcode.delete("1.0", "end")
    entry_box_qr.delete("1.0", "end")
    entry_device_barcode.delete("1.0", "end")
    entry_device_qr.delete("1.0", "end")
    
    # Clear the result labels
    for label in result_labels + result_values:
        label.config(text="")
    
    # Focus back to the first textbox
    entry_box_barcode.focus()

# Set up the main GUI window
root = tk.Tk()
root.title("Penguin Scanner")

monospace_font = font.Font(family="Courier", size=14) # Define a larger monospace font

# Input labels and textboxes
label_box_barcode = tk.Label(root, text="1. Scan Box Barcode:", font=monospace_font)
label_box_barcode.pack()
entry_box_barcode = tk.Text(root, height=2, width=50)
entry_box_barcode.pack()
entry_box_barcode.bind("<Return>", focus_next_widget)

# Set initial focus to the first textbox
entry_box_barcode.focus()

label_box_qr = tk.Label(root, text="2. Scan Box QR Code:", font=monospace_font)
label_box_qr.pack()
entry_box_qr = tk.Text(root, height=2, width=50)
entry_box_qr.pack()
entry_box_qr.bind("<Return>", focus_next_widget)

label_device_barcode = tk.Label(root, text="3. Scan Device Barcode:", font=monospace_font)
label_device_barcode.pack()
entry_device_barcode = tk.Text(root, height=2, width=50)
entry_device_barcode.pack()
entry_device_barcode.bind("<Return>", focus_next_widget)

label_device_qr = tk.Label(root, text="4. Scan Device QR Code:", font=monospace_font)
label_device_qr.pack()
entry_device_qr = tk.Text(root, height=2, width=50)
entry_device_qr.pack()
entry_device_qr.bind("<Return>", focus_next_widget)

# Query button
query_button = tk.Button(root, text="Query", command=query_scanner, height=2, width=20, font=monospace_font)
query_button.pack(pady=10)

# Result frame (for two-column layout)
result_frame = tk.Frame(root)
result_frame.pack(pady=10)

# Left column labels
result_label_1 = tk.Label(result_frame, text="Barcode:", font=monospace_font)
result_label_2 = tk.Label(result_frame, text="QR Code:", font=monospace_font)
result_label_3 = tk.Label(result_frame, text="SN:", font=monospace_font)
result_label_4 = tk.Label(result_frame, text="MAC:", font=monospace_font)
result_label_5 = tk.Label(result_frame, text="SoC:", font=monospace_font)
result_label_6 = tk.Label(result_frame, text="Temp:", font=monospace_font)

# Right column values
result_value_1 = tk.Label(result_frame, text="", font=monospace_font)
result_value_2 = tk.Label(result_frame, text="", font=monospace_font)
result_value_3 = tk.Label(result_frame, text="", font=monospace_font)
result_value_4 = tk.Label(result_frame, text="", font=monospace_font)
result_value_5 = tk.Label(result_frame, text="", font=monospace_font)
result_value_6 = tk.Label(result_frame, text="", font=monospace_font)

# Place labels and values in two columns
result_label_1.grid(row=0, column=0, sticky='w')
result_value_1.grid(row=0, column=1, sticky='w')

result_label_2.grid(row=1, column=0, sticky='w')
result_value_2.grid(row=1, column=1, sticky='w')

result_label_3.grid(row=2, column=0, sticky='w')
result_value_3.grid(row=2, column=1, sticky='w')

result_label_4.grid(row=3, column=0, sticky='w')
result_value_4.grid(row=3, column=1, sticky='w')

result_label_5.grid(row=4, column=0, sticky='w')
result_value_5.grid(row=4, column=1, sticky='w')

result_label_6.grid(row=5, column=0, sticky='w')
result_value_6.grid(row=5, column=1, sticky='w')

# Keep track of the result labels and values
result_labels = [result_label_1, result_label_2, result_label_3, result_label_4, result_label_5, result_label_6]
result_values = [result_value_1, result_value_2, result_value_3, result_value_4, result_value_5, result_value_6]

# Clear button
clear_button = tk.Button(root, text="Clear", command=clear_all, height=2, width=20, font=monospace_font)
clear_button.pack(pady=10)

# Start the Tkinter event loop
root.mainloop()

import tkinter as tk
from tkinter import messagebox
from tkinter import font
import Penguin_scanner as p_scanner

# Function to clean input by removing \n characters
def clean_input(input_text):
    # return input_text.replace('\n', '').strip()
    #
    #
    # Remove only trailing newline characters and strip spaces
    return input_text.rstrip('\n').strip()

# Function to shift focus to the next input field
def focus_next_widget(event):
    
    current_widget = event.widget
    widget_name = str(current_widget)  # Get the name or identifier of the widget

    # Clean up any trailing newlines or spaces before shifting focus
    text = current_widget.get("1.0", "end-1c")  # Get the text in the widget excluding the last newline
    cleaned_text = text.rstrip()  # Remove any trailing newlines and spaces
    current_widget.delete("1.0", "end")  # Clear the current content
    current_widget.insert("1.0", cleaned_text)  # Insert the cleaned content back
    
    print(f'widget_name: {widget_name} | len(text): {len(text)} | len(cleaned_text): {len(cleaned_text)}')

    # if len(cleaned_text) < 0, then the widget is empty, so don't shift focus
    if len(cleaned_text) < 1:
        # clear the whole text field in the current widget
        current_widget.delete("0", "end")

        return


    if '.!text' in widget_name:
        event.widget.tk_focusNext().focus()  # Move to box QR code
        print(f'moving from {widget_name} to box_qr')
    elif '.!text2' in widget_name:
        # event.widget.tk_focusNext().focus()  # Move to device barcode
        
        # move the focus to the widget with the name '.!text3'
        event.widget.master.nametowidget('.!text3').focus()
        
        print(f'moving from {widget_name} to device_barcode')
    elif '.!text3' in widget_name:
        event.widget.tk_focusNext().focus()  # Move to device QR code
        print(f'moving from {widget_name} to device_qr')
    elif '.!text4' in widget_name:
        event.widget.tk_focusNext().focus()  # Move to query button
        print(f'moving from {widget_name} to query_button')
    elif 'query_button' in widget_name:
        event.widget.tk_focusNext().focus()  # Move to clear button
        print(f'moving from {widget_name} to clear_button')
    elif 'clear_button' in widget_name:
        # Move focus back to box barcode to create a loop
        event.widget.master.focus_set()  # Move focus back to root
        box_barcode = event.widget.master.nametowidget('box_barcode')  # Assume the box barcode has a name
        box_barcode.focus()
        print(f'moving from {widget_name} to box_barcode')

# Bind the function to your input widgets as needed, for example:
# widget.bind("<Return>", focus_next_widget)

    

# Function to query the scanner and process the results
def query_scanner():
    # Extract and clean the input data
    # box_barcode = clean_input(entry_box_barcode.get("1.0", "end"))
    # box_qr = clean_input(entry_box_qr.get("1.0", "end"))
    # device_barcode = clean_input(entry_device_barcode.get("1.0", "end"))
    # device_qr = clean_input(entry_device_qr.get("1.0", "end"))
    box_barcode = clean_input(entry_box_barcode.get("1.0", "end")).strip().replace("\n", "").replace(" ", "")
    box_qr = clean_input(entry_box_qr.get("1.0", "end")).strip().replace("\n", "").replace(" ", "")
    device_barcode = clean_input(entry_device_barcode.get("1.0", "end")).strip().replace("\n", "").replace(" ", "")
    device_qr = clean_input(entry_device_qr.get("1.0", "end")).strip().replace("\n", "").replace(" ", "")


    # debug
    print(f"Box Barcode: {box_barcode}")
    print(f"Box QR Code: {box_qr}")
    print(f"Device Barcode: {device_barcode}")
    print(f"Device QR Code: {device_qr}")
    print('-' * 50)
     
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

# Function to limit input in the Text widget
def limit_input(event, max_chars=100):
    widget = event.widget
    current_text = widget.get("1.0", "end-1c")  # Get current text excluding the last newline
    
    # Check if the text length exceeds the maximum allowed characters
    if len(current_text) > max_chars:
        # Limit the input to max_chars
        widget.delete("1.0", "end")  # Clear the current content
        widget.insert("1.0", current_text[:max_chars])  # Insert truncated content


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

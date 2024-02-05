import tkinter as tk
from tkinter import filedialog


#allows user to upload files 
def upload_file():
    file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf"), ("Word Files", "*.docx")])
    # Process the selected file here
    # Add logic to process the files 
    print(f"Selected File: {file_path}")



def compare_documents():
    purchase_order = purchase_order_entry.get()
    # Implement document comparison logic here
    print(f"Comparing with Purchase Order: {purchase_order}")

# Create the main window with tkinter
root = tk.Tk()
root.title("Label Approval Tool")

# Create UI elements to upload and compare documents 
upload_button = tk.Button(root, text="Upload Document", command=upload_file)
purchase_order_label = tk.Label(root, text="Enter Purchase Order:")
purchase_order_entry = tk.Entry(root)
compare_button = tk.Button(root, text="Compare Documents", command=compare_documents)

# Place UI elements using grid
upload_button.grid(row=0, column=0)
purchase_order_label.grid(row=1, column=0)
purchase_order_entry.grid(row=1, column=1)
compare_button.grid(row=2, column=0)

# Start the Tkinter main loop
root.mainloop()

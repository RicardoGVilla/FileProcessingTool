import difflib
import tkinter as tk
from tkinter import filedialog
import docx
import fitz

# Initialize variables
file_path = None
export_instructions_selected = None
producer_input = None
product_input = None 
export_info = {}

# Function to upload files
def upload_file():
    global file_path, export_instructions_selected, producer_input, product_input, export_instructions

    if file_path is None and export_instructions_selected is None:
        file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf"), ("Word Files", "*.docx")])
        process_document(file_path)
    elif file_path and export_instructions_selected is None:
        export_instructions_selected = get_export_instructions()

# Function to get export instructions
def get_export_instructions():
    global export_instructions_selected, export_info
    export_instructions_selected = filedialog.askopenfilename(filetypes=[("Word Files", "*.docx")])
    process_export_instructions(export_instructions_selected)

def process_document(file):
    global file_path
    file_path = {}  # Reset file_path variable
    with fitz.open(file) as pdf_doc:  # Open PDF file using fitz
        for page_num in range(len(pdf_doc)):
            page = pdf_doc.load_page(page_num)  # Load each page
            text = page.get_text()  # Extract text from the page
            print(text)
            process_text(text)  # Process extracted text

def process_text(text):
    global file_path
    key = None
    value_buffer = ''
    for line in text.split('\n'):
        if ":" in line:
            if key:
                value_buffer = value_buffer.replace(" ,", ",")
                file_path[key] = normalize_text(' '.join(value_buffer.split())) 
                value_buffer = ''
            key, value = line.split(":", 1)
            key = key.strip()
            value_buffer = value.strip()
        else:
            value_buffer = value_buffer + ' ' + line.strip()
    if key:
        value_buffer = value_buffer.replace(" ,", ",")
        file_path[key] = normalize_text(' '.join(value_buffer.split()))

def process_export_instructions(instruction_text):
    global export_info, file_path
    word_doc = docx.Document(instruction_text)

    key_mapping = {
        "Product": "product",
        "Producer": "producer",
        "Importer": "importer",
        "Lot Number": "lot"
    }

    for paragraph in word_doc.paragraphs:
        for line in paragraph.text.split('\n'): 
            if ":" in line:
                key, value = line.split(":", 1)
                key = key.strip()
                if key in key_mapping:
                    export_info[key_mapping[key]] = value.strip()

    return export_info

def highlight_difference(widget, start, end):
    widget.tag_add("diff", start, end)
    widget.tag_config("diff", background="yellow")

def compare_documents():
    global export_info, file_path, pdf_text_widget, export_instructions_text_widget

    #Check for export instruction
    if not export_info:
        response = tk.messagebox.askyesno("No Export Instructions", "Do you want to upload export instructions?")
        if response:
            get_export_instructions()
        return
    
    display_document_content()

    line_index = 1 

    for export_key, export_value in export_info.items():

        found_key = next((file_key for file_key in file_path.keys() if export_key.lower() in file_key.lower()), None)

        if found_key:
            # Prepare text for comparison
            normalized_export_value = normalize_text(export_value)
            normalized_file_value = normalize_text(file_path[found_key])

            # Compare the values
            diff = list(difflib.ndiff(normalized_export_value.split(), normalized_file_value.split()))
            
            # Process the differences for highlighting
            process_differences(diff, export_key, normalized_file_value, line_index)
            line_index = line_index + 2 
        else:
            print(f"No matching key found for '{export_key}' in the document.")
        
        
def process_differences(diff, export_key, file_value, line_number):
      
     # Insert the key and its corresponding value from the document before highlighting differences
    pdf_text_widget.insert(tk.END, f"{export_key.upper()}: {file_value}\n\n")
    
    current_char_index = len(export_key) + 1

    for word in diff:
        if word.startswith("-"):
         continue  
           
        word_length = len(word)
        current_char_index += word_length
        
        if word.startswith("+ "):
            start_index = f"{line_number}.{current_char_index - word_length}"
            end_index = f"{line_number}.{current_char_index}"
            
             # Apply highlight using calculated positions
            pdf_text_widget.tag_add("highlight" , start_index, end_index)
            pdf_text_widget.tag_config("highlight", background="yellow")
        


def normalize_text(text):
    text = text.replace(" - ", "-")
    text = ' '.join(text.split())
    return text

def display_document_content():
    # Clear the current content of the text widgets
    export_instructions_text_widget.delete('1.0', tk.END)

    # Export Instructions
    if export_instructions_selected:
        for key, value in export_info.items():
            export_instructions_text_widget.insert(tk.END, f"{key.upper()}: {value.upper()}\n")

# Create the main window with tkinter
root = tk.Tk()
root.title("Label Approval Tool")


def enable_export_instructions_button():
    global export_instructions_button
    export_instructions_button.config(state=tk.NORMAL)

upload_button = tk.Button(root, text="Upload Label", command=upload_file)
export_instructions_button = tk.Button(root, text="Upload Export Instructions", command=get_export_instructions)
producers = ['Producer 1', 'Producer 2', 'Producer 3']  
products = ['Product A', 'Product B', 'Product C']  
export_instructions = {}
producer_var = tk.StringVar(root)
producer_var.set(producers[0])
product_var = tk.StringVar(root)
product_var.set(products[0])
compare_button = tk.Button(root, text="Compare Documents", command=lambda: compare_documents())

# Text widgets for displaying document content
pdf_text_widget = tk.Text(root, height=50, width=100)
export_instructions_text_widget = tk.Text(root, height=50, width=100)
pdf_text_widget.grid(row=4, column=0)
export_instructions_text_widget.grid(row=4, column=1)


# Place UI elements using grid
upload_button.grid(row=0, column=0)
export_instructions_button.grid(row=1, column=0)
compare_button.grid(row=3, column=0)

# Start the Tkinter main loop
root.mainloop()
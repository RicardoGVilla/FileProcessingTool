import difflib
import tkinter as tk
from tkinter import filedialog
import docx
import PyPDF2

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
    pdf_doc = PyPDF2.PdfReader(file)
    counter = 0
    file_path = {}
    key = None
    value_buffer = ''
    for page_num in range(len(pdf_doc.pages)):
        page = pdf_doc.pages[page_num]
        for line in page.extract_text().split('\n'):
            if ":" in line:
                if key:
                    value_buffer = value_buffer.replace(" ,", ",")
                    file_path[key] = normalize_text(' '.join(value_buffer.split())) 
                    value_buffer = ''
                key, value = line.split(":", 1)
                key = key.strip()
                value_buffer = value.strip()
                counter += 1
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
    counter = 0 
    for paragraph in word_doc.paragraphs:
        for line in paragraph.text.split('\n'): 
            counter = counter + 1
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
    global export_info, file_path

    if export_info:
        for export_key, export_value in export_info.items():
            found_key = None
            for file_key in file_path.keys():
                if export_key.lower() in file_key.lower():
                    found_key = file_key
                    break

            if found_key:
                normalized_export_value = normalize_text(export_value)
                export_instructions_text_widget.insert(tk.END, f"{export_key.upper()}: {normalized_export_value}\n\n")

                normalized_file_value = normalize_text(file_path[found_key])
                pdf_text_widget.insert(tk.END, f"{found_key.upper()}: {normalized_file_value}\n\n")

                diff = list(difflib.ndiff([normalized_export_value], [normalized_file_value]))
                
                # Initialize indices for highlighting
                export_index = 1
                file_index = 1
                for i, s in enumerate(diff):
                    if s[0] == ' ':
                        export_index += 1
                        file_index += 1
                    elif s[0] == '-':
                        # Highlight in export instructions
                        start = f"{export_index}.{len(s) - 2}"
                        export_index += 1
                        end = f"{export_index}.0"
                        highlight_difference(export_instructions_text_widget, start, end)
                    elif s[0] == '+':
                        # Highlight in pdf text
                        start = f"{file_index}.{len(s) - 2}"
                        file_index += 1
                        end = f"{file_index}.0"
                        highlight_difference(pdf_text_widget, start, end)
            else:
                print(f"No matching key found for '{export_key}' in the document.")
    else: 
        response = tk.messagebox.askyesno("No Export Instructions", "Do you want to upload export instructions?")
        if response:
            get_export_instructions()


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
            export_instructions_text_widget.insert(tk.END, f"{key}: {value}\n")

# Create the main window with tkinter
root = tk.Tk()
root.title("Label Approval Tool")

def select_producer(supplier):
    global producer_input
    producer_input = supplier
    print("now you have a producer:", producer_input)

def select_product(item):
    global product_input
    product_input = item 
    print("now you have an item:", product_input)

def enable_export_instructions_button():
    global export_instructions_button
    export_instructions_button.config(state=tk.NORMAL)

upload_button = tk.Button(root, text="Upload Document", command=upload_file)
export_instructions_button = tk.Button(root, text="Upload Export Instructions", command=get_export_instructions, state=tk.DISABLED)
producers = ['Producer 1', 'Producer 2', 'Producer 3']  
products = ['Product A', 'Product B', 'Product C']  
export_instructions = {}
producer_var = tk.StringVar(root)
producer_var.set(producers[0])
product_var = tk.StringVar(root)
product_var.set(products[0])
producer_dropdown = tk.OptionMenu(root, producer_var, *producers, command=select_producer)
product_dropdown = tk.OptionMenu(root, product_var, *products, command=select_product)
compare_button = tk.Button(root, text="Compare Documents", command=lambda: compare_documents())

# Text widgets for displaying document content
pdf_text_widget = tk.Text(root, height=50, width=100)
export_instructions_text_widget = tk.Text(root, height=50, width=100)
pdf_text_widget.grid(row=4, column=0)
export_instructions_text_widget.grid(row=4, column=1)


# Place UI elements using grid
upload_button.grid(row=0, column=0)
export_instructions_button.grid(row=1, column=0)
producer_dropdown.grid(row=2, column=0)
product_dropdown.grid(row=2, column=1)
compare_button.grid(row=3, column=0)

# Start the Tkinter main loop
root.mainloop()
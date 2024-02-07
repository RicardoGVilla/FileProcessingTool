import tkinter as tk
from tkinter import filedialog
import docx
import PyPDF2


#allows user to upload files 
def upload_file(file_path=None, export_instructions_selected=None):
    # Reading pdf files 

    if file_path is None and export_instructions_selected is None:
        file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf"), ("Word Files", "*.docx")])
        return
        
    if file_path and not export_instructions_selected:
        get_export_instructions()
    compare_documents(file_path,get_export_instructions)

        

def get_export_instructions():
        export_instructions_selected = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf"), ("Word Files", "*.docx")])
       



    
def print_pdf(file_path):
    pdf_reader = PyPDF2.PdfReader(file_path)
    
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        for line in page.extract_text().split('\n'):
            if line.strip():
                print(line)


def print_word(file_path):
    word_read = docx.Document(file_path)
    for paragraph in word_read.paragraphs:
        text = paragraph.text.strip()
        if text:
            print(text)

def compare_documents(document, export_instructions):
    print("Hello from compare documents")
    # print(f"Selected File: {file_path}")
    #     if file_path.lower().endswith(".pdf"):
    #         print_pdf(file_path)
    #     elif file_path.lower().endswith(".docx"):
    #         print_word(file_path)


    """
    We identify the type of file it is 
    We look for other documents that possesses that specific reference number
    if not found we ask the user for export instructions 
    We save the export instruction, proceed approving the doc.  
    If found we compare each of the fields against each other 
    If corret we print document is approved and we save it 
    If not correct we return where those files are wrong and ask for amendment
    Once amended, the file, if approved, will be stored for future references 
    """

# Create the main window with tkinter
root = tk.Tk()
root.title("Label Approval Tool")

# Initialize variables
file_path = None
export_instructions_selected = None

# Create UI elements to upload and compare documents 
upload_button = tk.Button(root, text="Upload Document", command=lambda: upload_file(file_path, export_instructions_selected))
export_instructions = tk.Button(root, text="Upload Export Instructions", command=lambda: upload_file(file_path, export_instructions_selected))
purchase_order_label = tk.Label(root, text="Enter Purchase Order:")
purchase_order_entry = tk.Entry(root)
compare_button = tk.Button(root, text="Compare Documents", command=lambda: compare_documents(file_path, export_instructions_selected))

# Place UI elements using grid
upload_button.grid(row=0, column=0)
export_instructions.grid(row=1, column=0)
purchase_order_label.grid(row=2, column=0)
purchase_order_entry.grid(row=2, column=1)
compare_button.grid(row=3, column=0)

# Start the Tkinter main loop
root.mainloop()
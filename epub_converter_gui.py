import tkinter as tk
from tkinter import filedialog, messagebox
from threading import Thread
from bs4 import BeautifulSoup
import bs4
import re
from ebooklib import epub
from pathlib import Path

def _convert_file_path(path):
    path_obj = Path(path)
    new_name = "converted-" + path_obj.name
    new_path = path_obj.with_name(new_name)
    return str(new_path)

def convert_to_bionic_str(soup: BeautifulSoup, s: str):
    new_parent = soup.new_tag("span")
    words = re.split(r'.,;:!?-|\s', s)
    for word in words:
        if len(word) >= 4:
            mid = (len(word) // 2) + 1
            first_half, second_half = word[:mid], word[mid:]
            b_tag = soup.new_tag("b")
            b_tag.append(soup.new_string(first_half))
            new_parent.append(b_tag)
            new_parent.append(soup.new_string(second_half + " "))
        else:
            new_parent.append(soup.new_string(word + " "))
    return new_parent

def convert_to_bionic(content: str):
    soup = BeautifulSoup(content, 'html.parser')
    for e in soup.descendants:
        if isinstance(e, bs4.element.Tag):
            if e.name == "p":
                children = list(e.children)
                for child in children:
                    if isinstance(child, bs4.element.NavigableString):
                        if len(child.text.strip()):
                            child.replace_with(convert_to_bionic_str(soup, child.text))
    return str(soup).encode()

def convert_book(book_path):
    source = epub.read_epub(book_path)
    for item in source.items:
        if item.media_type == "application/xhtml+xml":
            content = item.content.decode('utf-8')
            item.content = convert_to_bionic(content)
    epub.write_epub(_convert_file_path(book_path), source)

def select_file():
    file_path = filedialog.askopenfilename(filetypes=[("EPUB files", "*.epub")])
    if file_path:
        file_path_var.set(file_path)

def start_conversion():
    book_path = file_path_var.get()
    if book_path:
        try:
            thread = Thread(target=convert_book, args=(book_path,))
            thread.start()
            thread.join()
            messagebox.showinfo("Success", "Book converted successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    else:
        messagebox.showwarning("Warning", "Please select a book first.")

app = tk.Tk()
app.title("EPUB Converter")

file_path_var = tk.StringVar()

frame = tk.Frame(app)
frame.pack(padx=10, pady=10)

select_button = tk.Button(frame, text="Select Book", command=select_file)
select_button.pack(side=tk.LEFT, padx=(0, 10))

path_entry = tk.Entry(frame, textvariable=file_path_var, width=50)
path_entry.pack(side=tk.LEFT, expand=True, fill=tk.X)

convert_button = tk.Button(app, text="Convert", command=start_conversion)
convert_button.pack(pady=(10, 0))

app.mainloop()
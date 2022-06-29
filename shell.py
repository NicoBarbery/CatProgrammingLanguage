from turtle import width
import cat
from tkinter import *
from tkinter import ttk
from tkinter.filedialog import asksaveasfilename, askopenfilename
from tkinter.scrolledtext import ScrolledText
import tkinter as tk

# create an instance for window
window = Tk()
# set title for window
window.title("CAT IDE")

# create and configure menu
menu = Menu(window)
window.config(menu=menu)

# create input frame
input_frame = Frame(window)
input_frame.pack(side=LEFT, padx=15, pady=20)

# Title Label
title_label = Label(input_frame, text = "CAT COMPILER", font=("Arial Bold", 20, 'underline'), fg = "#2B3239")
title_label.pack(side=TOP, padx=25, pady=15)

# Title Label
#input_label = Label(input_frame, text="INPUT", font=("Arial Bold", 12), fg="#2B3239")
#input_label.pack(pady=10, expand=1)

# create input_window window for writing code
input_window = ScrolledText(input_frame, font=("Arial", 10), wrap=None, height=15)
input_window.pack(padx = 10, side=LEFT, fill=BOTH, expand=1)
input_window.focus()

file_path = ""

# function to open files
def open_file(event=None):
    global code, file_path
    # code = input_window.get(1.0, END)
    open_path = askopenfilename(filetypes=[("CAT File", "*.cat")])
    file_path = open_path
    with open(open_path, "r") as file:
        code = file.read()
        input_window.delete(1.0, END)
        input_window.insert(1.0, code)

window.bind("<Control-o>", open_file)


# function to save files
def save_file(event=None):
    global code, file_path
    if file_path == '':
        save_path = asksaveasfilename(defaultextension=".cat", filetypes=[("CAT File", "*.cat")])
        file_path = save_path
    else:
        save_path = file_path
    with open(save_path, "w") as file:
        code = input_window.get(1.0, END)
        file.write(code)

window.bind("<Control-s>", save_file)


# function to save files as specific name
def save_as(event=None):
    global code, file_path
    # code = input_window.get(1.0, END)
    save_path = asksaveasfilename(defaultextension=".cat", filetypes=[("CAT File", "*.cat")])
    file_path = save_path
    with open(save_path, "w") as file:
        code = input_window.get(1.0, END)
        file.write(code)

window.bind("<Control-S>", save_as)

def print_tokens(tokens):
    if len(tokens) > 0:
        tokens_list = tokens.copy()
        tokens_list.reverse()
        tokens_window.delete(1.0, END)
        for token in tokens_list:
            tokens_window.insert(1.0, token)
            tokens_window.insert(1.0, "\n")

# function to execute the code and
# display its output
def run(event=None):
    global code, file_path

    code = input_window.get(1.0, END)

    if True:
        result, error = cat.run('<stdin>', code)
        if error:
            # delete the previous text from output_windows
            output_window.delete(1.0, END)
            output_window.insert(1.0, error.as_string())
            print(error.as_string())
        elif result:
            if len(result.elements) == 1:
                print(repr(result.elements[0]))
                # delete the previous text from output_windows
                output_window.delete(1.0, END)
                #print tokens
                print_tokens(cat.tokens)
                # insert the new output text in output_windows
                output_window.insert(1.0, repr(result.elements[0]))
                output_window.insert(1.0, "\n")
                output_window.insert(1.0, cat.output)
                
            else:
                print(result)
                # delete the previous text from output_windows
                output_window.delete(1.0, END)
                #print tokens
                print_tokens(cat.tokens)
                # insert the new output text in output_windows
                output_window.insert(1.0, repr(result.elements))
                output_window.insert(1.0, "\n")
                output_window.insert(1.0, cat.output)
            
window.bind("<F5>", run)

# function to close IDE window
def close(event=None):
    window.destroy()

window.bind("<Control-q>", close)

# define function to cut
# the selected text
def cut_text(event=None):
    input_window.event_generate(("<<Cut>>"))

# define function to copy
# the selected text
def copy_text(event=None):
    input_window.event_generate(("<<Copy>>"))

# define function to paste
# the previously copied text
def paste_text(event=None):
    input_window.event_generate(("<<Paste>>"))

# create menus
file_menu = Menu(menu, tearoff=0)
edit_menu = Menu(menu, tearoff=0)
run_menu = Menu(menu, tearoff=0)
view_menu = Menu(menu, tearoff=0)
theme_menu = Menu(menu, tearoff=0)

# add menu labels
menu.add_cascade(label="Archivo", menu=file_menu)
menu.add_cascade(label="Editar", menu=edit_menu)
menu.add_cascade(label="Ejecutar", menu=run_menu)
menu.add_cascade(label="Ver", menu=view_menu)
menu.add_cascade(label="Tema", menu=theme_menu)

# add commands in flie menu
file_menu.add_command(label="Abrir", accelerator="Ctrl+O", command=open_file)
file_menu.add_separator()
file_menu.add_command(label="Guardar", accelerator="Ctrl+S", command=save_file)
file_menu.add_command(label="Guardar como", accelerator="Ctrl+Shift+S", command=save_as)
file_menu.add_separator()
file_menu.add_command(label="Salir", accelerator="Ctrl+Q", command=close)

# add commands in edit menu
edit_menu.add_command(label="Cortar", command=cut_text)
edit_menu.add_command(label="Copiar", command=copy_text)
edit_menu.add_command(label="Pegar", command=paste_text)
run_menu.add_command(label="Ejecutar", accelerator="F5", command=run)

# function to display and hide status bar
show_status_bar = BooleanVar()
show_status_bar.set(True)

def hide_statusbar():
    global show_status_bar
    if show_status_bar:
        status_bars.pack_forget()
        show_status_bar = False
    else:
        status_bars.pack(side=BOTTOM)
        show_status_bar = True


view_menu.add_checkbutton(label="Status Bar", onvalue=True, offvalue=0, variable=show_status_bar,
                          command=hide_statusbar)
# create a label for status bar
status_bars = ttk.Label(window, text=" \t\t\t\t\t\t\t\t  characters: 0 words: 0")
status_bars.pack(side=BOTTOM)

# function to display count and word characters
text_change = False

def change_word(event=None):
    global text_change
    if input_window.edit_modified():
        text_change = True
        word = len(input_window.get(1.0, "end-1c").split())
        chararcter = len(input_window.get(1.0, "end-1c").replace(" ", ""))
        status_bars.config(text=f" \t\t\t\t\t\t characters: {chararcter} words: {word}")
    input_window.edit_modified(False)

input_window.bind("<<Modified>>", change_word)

# function for light mode window
def light():
    window.config(bg="#CFDCE7")
    title_label.config(fg="#2B3239",bg="#CFDCE7")
    input_frame.config(bg="#CFDCE7")
    input_window.config(fg="#2B3239", bg="white")
    #TOKENS
    tokens_label.config(fg="#2B3239", bg="#CFDCE7")
    tokens_window.config(fg="#2B3239", bg="white")
    #OUTPUT
    output_label.config(fg="#2B3239", bg="#CFDCE7")
    output_frame.config( bg="#CFDCE7")
    output_window.config(fg="#2B3239", bg="white")
    status_bars.config(fg="#2B3239",bg="#CFDCE7")

# function for dark mode window
def dark():
    window.config(bg="#183A59")
    title_label.config(fg="white",bg="#183A59")
    input_frame.config(bg="#183A59")
    input_window.config(fg="white", bg="black")
    #TOKENS
    tokens_label.config(fg="white", bg="#183A59")
    tokens_window.config(fg="white", bg="black")
    #OUTPUT
    output_label.config(fg="white", bg="#183A59")
    output_frame.config(bg="#183A59")
    output_window.config(fg="white", bg="black")
    status_bars.config(fg="white", bg="#183A59")

# add commands to change themes
theme_menu.add_command(label="light", command=light)
theme_menu.add_command(label="dark", command=dark)

# create output frames
output_frame = Frame(window)
output_frame.pack(side=RIGHT, padx=15, pady=20)

# create output window to display output of written code
tokens_label = Label(output_frame, text="TOKENS", font=("Arial Bold", 12), fg="#2B3239", justify=RIGHT)
tokens_label.pack(pady=10, expand=1)
tokens_window = ScrolledText(output_frame, height=15)
tokens_window.pack(padx = 10, side=TOP, fill=BOTH, expand=1)


output_label = Label(output_frame, text="OUTPUT", font=("Arial Bold", 12), fg="#2B3239", justify=LEFT)
output_label.pack(pady=10, expand=1)

# create output window to display output of written code
output_window = ScrolledText(output_frame, height=10)
output_window.pack(padx = 10, pady = 10, side=BOTTOM,  fill=BOTH, expand=1)

window.mainloop()

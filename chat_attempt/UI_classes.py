import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText


class UI_window(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.UI_init()

    def UI_init(self): # делегируем оформление
        self.title('chat_attempt')
        self.geometry('{}x{}'.format(300, 400) )
        self.minsize(300,300)
        self.maxsize(600,800)

    def windinfo(self):
        for nm in self.children:
            print(self.children[nm] )



class SettingsFrame(ttk.Frame):
    def __init__(self, parent):

        super().__init__(master = parent, style="fr_style.TFrame")
        self.UI_init()

    def UI_init(self): # делегируем оформление
        
        for i in range(2): self.columnconfigure(i, weight=1)
        for i in range(7): self.rowconfigure(i, weight=1)
        self.configure( 
            width = self.master.winfo_width(),
            height = self.master.winfo_height() 
            )
    
    def display(self): 
        self.pack(expand=True, fill=tk.BOTH)

class ChatFrame(ttk.Frame):
    def __init__(self, parent):

        super().__init__(master = parent, style="fr_style.TFrame")
        self.UI_init()

    def UI_init(self): # делегируем оформление
        
        for i in range(2): self.columnconfigure(i, weight=1)
        self.rowconfigure(0, weight=7)
        self.rowconfigure(1, weight=1)
        self.configure( 
            width = self.master.winfo_width(),
            height = self.master.winfo_height() 
            )
    
    def display(self): 
        self.pack(expand=True, fill=tk.BOTH)



class UI_button(ttk.Button):
    def __init__(self, parent, text, func):
        super().__init__(master = parent, text=text, command = func, style = "btn_style.TButton" )
        self.UI_init()

    def UI_init(self): # делегируем оформление
        #ну хотя бы фон добавить
        #self.bg = "#9999FF"
        pass

    def display(self, coords ): # принимает (row,col,colspan)
        self.grid(row=coords[0], column=coords[1], columnspan=coords[2])


class UI_label(ttk.Label):
    def __init__(self, parent, text, textvar = None):
        super().__init__(master = parent, text=text, style = "lbl_style.TLabel", textvariable = textvar)
        self.UI_init()

    def UI_init(self): # делегируем оформление. а почему не делегируется?..
        #self.bg = "#4000FF",
        #self.fg="#FFFFFF"
        pass # если оно не работает, может удалить кчерту

    def display(self, coords ): # принимает (row,col,colspan)
        self.grid(row=coords[0], column=coords[1], columnspan=coords[2])

class UI_entry(ttk.Entry):
    def __init__(self, parent, store_string):
        super().__init__(master = parent, textvariable=store_string ,style = "entr_style.TEntry" )
        self.UI_init()

    def UI_init(self):
        pass#self.bg = "#580927" #оно же не работает, не? просто чтоб что-то было

    def display(self, coords ): # принимает (row,col,colspan)
        self.grid(row=coords[0], column=coords[1], columnspan=coords[2])

class UI_text(ScrolledText):
    def __init__(self, parent):
        super().__init__(master=parent )
        self.UI_init()
    
    def UI_init(self): #нет стилей, т.к. тк а не ттк, кто понял тот понял
        self.configure(
            wrap = tk.WORD,
            state = tk.DISABLED,
            bg = "#5809F7",
            fg = "#FFFFFF",
            padx= 3,
            pady = 5
            )
        

    def write(self, text_string):
        self.configure(state = tk.NORMAL)
        self.insert(tk.END, text_string.get() + "\n")
        self.see(tk.END)
        text_string.set("")
        self.configure(state = tk.DISABLED)

    def display(self, coords ): # принимает (row,col,colspan)
        self.grid(row=coords[0], column=coords[1], columnspan=coords[2])

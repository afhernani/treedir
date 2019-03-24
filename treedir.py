#!/bin/python3.py
# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os, time


class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Explorador de archivos y carpetas")
        self.geometry("500x600")

        self.back_history = []
        self.forward_history = []

        self.toplayout = tk.LabelFrame(self)

        back_path= os.path.abspath(r'images/back.png')
        print(back_path)
        img = ImageTk.PhotoImage(Image.open(r'images/back.png').resize((16, 16), Image.ANTIALIAS))

        self.back_button = tk.Button(self.toplayout, width=16, height=16,
                                     image=img, state=tk.DISABLED,
                                     compound=tk.TOP, command=self.back_clicked)
        self.back_button.Image = img

        img = ImageTk.PhotoImage(Image.open(r'images/forward.png').resize((16, 16), Image.ANTIALIAS))
        self.forward_button = tk.Button(self.toplayout, width=16, height=16, image=img,
                                        state=tk.DISABLED, command=self.forward_clicked)
        self.forward_button.Image = img

        img = ImageTk.PhotoImage(Image.open(r'images/up.png').resize((16, 16), Image.ANTIALIAS))
        self.up_button = tk.Button(self.toplayout, width=16, height=16,
                                   image=img, command=self.up_button_clicked)
        self.up_button.image = img

        self.address = tk.StringVar()
        self.address_edit = tk.Entry(self.toplayout, text="Entry", textvar=self.address)

        img = ImageTk.PhotoImage(Image.open(r'images/update.png').resize((16, 16), Image.ANTIALIAS))
        self.refresh_button = tk.Button(self.toplayout, width=16, height=16,
                                        image=img, command=self.refresh_button_clicked)
        self.refresh_button.image = img

        self.back_button.pack(side=tk.LEFT)
        self.forward_button.pack(side=tk.LEFT)
        self.up_button.pack(side=tk.LEFT)
        self.address_edit.pack(side=tk.LEFT, fill=tk.X, expand=1)
        self.refresh_button.pack(side=tk.RIGHT)
        self.toplayout.pack(side=tk.TOP, fill=tk.X)
        print(os.getcwd())
        # insertamos el treeview componente
        self.tree = ttk.Treeview(self)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        # self.tree['show'] = 'headings'
        self.tree["columns"] = ("Name", "Date", "Size")
        self.tree.column("Name", width=100)
        self.tree.column("Date", width=100)
        self.tree.column("Size", width=100)
        self.tree.heading("Name", text="Name")
        self.tree.heading("Date", text="Date")
        self.tree.heading("Size", text="Size")
        self.tree.bind('<<TreeviewSelect>>', self.on_selected)
        self.tree.bind("<Double-1>", self.on_double_click)
        self.ysb = ttk.Scrollbar(self.tree, orient='vertical', command=self.tree.yview)
        self.ysb.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscroll=self.ysb.set)
        self.xsb = ttk.Scrollbar(self.tree, orient='horizontal', command=self.tree.xview)
        self.xsb.pack(side=tk.BOTTOM, fill=tk.X)
        self.tree.configure(xscroll=self.xsb.set)

        self.file_image = tk.PhotoImage(file=r"images/file.png")
        self.folder_image = tk.PhotoImage(file=r"images/folder.png")

        self.load_path(os.getcwd())

    def get_icon(self, path):
        """
        Retorna la imagen correspondiente según se especifique
        un archivo o un directorio.
        """
        return self.folder_image if os.path.isdir(path) else self.file_image

    def back_clicked(self):
        print("back_clicked ...")
        if self.back_history and len(self.back_history) > 1:
            # obtener el ultimo elemento
            path = self.back_history[-2]
            self.forward_history.append(self.back_history[-1])
            # remover el directorio actual
            del self.back_history[-1]
            self.load_path(path, False)

    def forward_clicked(self):
        print("forward_clicked ...")
        if self.forward_history:
            path = self.forward_history[-1]
            self.back_history.append(path)
            del self.forward_history[-1]
            self.load_path(path, False)

    def up_button_clicked(self):
        print("up_button_clicked ...")
        parent = os.path.dirname(self.address.get())
        if parent != self.address.get():
            self.load_path(parent)

    def refresh_button_clicked(self):
        print("refresh_button_clicked ...", self.address.get())
        self.load_path(self.address.get())

    def on_selected(self, event):
        print("on_selected ...", event.x, event.y)

    def on_double_click(self, event):
        print("on_double_click ...")
        # item = self.tree.selection()[0]
        item = self.tree.identify('item', event.x, event.y)
        print("you clicked on", self.tree.item(item, "text"), item)
        filepath = os.path.join(self.address.get(), item)
        if os.path.isdir(filepath):
            self.load_path(filepath)
        else:
            # lanch de file
            # startfile(filepath)
            pass

    def load_path(self, path, use_history=True):
        # parent = ' '
        parent = ''
        # Obtener archivos y carpetas
        items = os.listdir(path)
        # Eliminar el contenido anterior
        x = self.tree.get_children()
        for item in x:
            self.tree.delete(item)
        # self.tree.delete(self.tree.get_children())
        # self.tree.delete()
        for i in items:
            # omitir archivos ocultos
            if i.startswith("."):
                continue
            filepath = os.path.join(path, i)
            print("item : ", filepath)
            # obtener informacion del archivos
            stats = os.stat(filepath)
            print("stats: ", stats)
            # import os, time //para esto
            (mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat(filepath)
            tie = time.ctime(mtime)
            print("last modified: %s" % tie)
            tam = self.convert_bytes(size)
            print("Size: %s"% tam)
            datos = [i, tie, tam]
            # crear el control item
            self.tree.insert(parent, tk.END, i, text=i,
                             image=self.get_icon(filepath), values=datos)
            # (str(stats.st_mtime), str(stats.st_size) if os.path.isfile(filepath) else " "),
            # item_widget = (i, strftime("%c", localtime(stats.st_mtime)),
            #                        size(stats.st_size) if isfile(filepath) else " "
            #                        )
            # .decode("utf-8") in localtime
            # Establecer el icono correspondiente
            # añadir el elemento.
            self.address.set(path)
            # añadir al historial
        if use_history:
            self.back_history.append(self.address.get())
        # habilitar / deshabilitar botones de historial.
        if self.back_history and len(self.back_history) > 1:
            if not self.back_button['state'] == tk.NORMAL:
                self.back_button['state'] = tk.NORMAL
        else:
            if self.back_button['state'] == tk.NORMAL:
                self.forward_history = []
                self.back_button['state'] = tk.DISABLED
        if self.forward_history:
            if not self.forward_button['state'] == tk.NORMAL:
                self.forward_button['state'] = tk.NORMAL
        else:
            if self.forward_button['state'] == tk.NORMAL:
                self.forward_button['state'] = tk.DISABLED

    @staticmethod
    def convert_bytes(num):
        """
        this function will convert bytes to MB.... GB... etc
        """
        for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
            if num < 1024.0:
                return "%3.1f %s" % (num, x)
            num /= 1024.0

    def file_size(self, file_path):
        """
        this function will return the file size
        """
        if os.path.isfile(file_path):
            file_info = os.stat(file_path)
            return self.convert_bytes(file_info.st_size)


if __name__ == '__main__':
    win = Window()
    win.mainloop()

from tkinter import *
import utils
from pathlib import Path
from datetime import datetime
import time
import os
import tk_utils
from tkinter import simpledialog
from tkinter import messagebox


class GUI():
    def __init__(self, master, base_path):
        self.base_path = Path(base_path)
        self.master = master
        self.master.title("File Manager")
        self.dirs_label = Label(self.master, text="Directories:")
        self.files_label = Label(self.master, text="Files:")

        self.dirs_label.grid(row=0, column=1, sticky=W, padx=10, pady=5)
        self.files_label.grid(row=0, column=4, sticky=W, padx=10, pady=5)

        self.dirs_listbox = Listbox(self.master, relief=FLAT)
        self.files_listbox = Listbox(self.master, width=40, relief=FLAT)
        self.dirs_listbox.grid(row=1, columnspan=2, column=1, sticky=W + E + N + S, padx=10)
        self.files_listbox.grid(row=1, columnspan=3, column=4, sticky=W + E + N + S, padx=10)

        self.dirs_listbox.bind("<Double-Button-1>", self.dbl_dirs)
        self.files_listbox.bind("<Double-Button-1>", self.dbl_files)

        self.dir_size_label = Label(self.master, text="Total Size: ")
        self.dir_size_label.grid(row=2, column=1, sticky=W, padx=10, pady=10)

        self.total_size = StringVar()
        self.dir_size_label_var = Label(self.master, textvariable=self.total_size)
        self.dir_size_label_var.grid(row=2,column=2)

        self.path_label = Label(self.master, text="Current path: ")
        self.path_label.grid(row=2, column=4, sticky=W, padx=10, pady=10)

        self.current_pathVar = StringVar()
        self.path_label_var = Label(self.master, textvariable=self.current_pathVar)
        self.path_label_var.grid(row=2, column=5)

        self.nd_frame = Frame(self.master)
        self.newdir_button = Button(self.nd_frame, text="+", relief=GROOVE, command=self.new_dir_window)
        self.del_button = Button(self.nd_frame, text="-", relief=GROOVE, command=self.del_file_win)

        self.rs_frame = Frame(self.master)
        self.run_button = Button(self.rs_frame, text="Run", relief=GROOVE, command=self.dbl_files)
        self.search_button = Button(self.rs_frame, text="Search", relief=GROOVE, command=self.search_btn)

        self.filter_global = '*'
        self.feb_frame = Frame(self.master)
        self.filter_entry = Entry(self.feb_frame, width=10, relief=GROOVE)
        self.filter_button = Button(self.feb_frame, text="Filter", relief=GROOVE, command = self.filter_btn)
        self.filter_entry.insert(0, "*.*")

        self.newdir_button.grid(row=0, column=0, sticky=W, ipadx=10)
        self.del_button.grid(row=0, column=1, sticky=E, ipadx=10)
        self.nd_frame.grid(row=3, column=1)

        self.run_button.grid(row=0, column=0, sticky=W, padx=5)
        self.search_button.grid(row=0, column=1, sticky=E, padx=5)
        self.rs_frame.grid(row=3, column=4, sticky=W)

        self.filter_entry.grid(row=0, column=0, padx=5, sticky=N + S)
        self.filter_button.grid(row=0, column=1, padx=5)
        self.feb_frame.grid(row=3, column=6)

        self.master.columnconfigure(0, minsize=30)
        self.master.columnconfigure(1, weight=1)
        self.master.columnconfigure(4, weight=1)
        self.master.rowconfigure(1, weight=1)
        self.master.columnconfigure(3, minsize=30)
        self.master.columnconfigure(7, minsize=30)
        self.master.minsize(500, 300)
        self.master.rowconfigure(4, minsize=30)

        self.updateGui()


    def dbl_dirs(self, event):
        if len(self.dirs_listbox.curselection()) > 0:
            selected_item_index = self.dirs_listbox.curselection()[0]
            selection = self.dirs_listbox.get(selected_item_index)
            self.change_basepath(selection)

    def dbl_files(self, *event):
        if len(self.files_listbox.curselection()) > 0:
            selected_item_index = self.files_listbox.curselection()[0]
            selection = self.files_listbox.get(selected_item_index)
            os.startfile(self.base_path / selection)

    def search_btn(self):
        answer = simpledialog.askstring("Search", "Enter search term:",
                                        parent=self.master)
        if answer is not None:
            a = self.base_path.glob('**/*'+answer+'*')
            a = [object for object in a if object.is_file()]
            if len(a) > 0:
                self.change_basepath(a[0].parent)
            else:
                messagebox.showinfo("File not found","File not found")

    def filter_btn(self):
        filter_entry = str(self.filter_entry.get()).split('.')
        if filter_entry[-1] == self.filter_global:
            self.updateGui()
            self.filter_global = '*'
            self.filter_entry.delete(0,END)
            self.filter_entry.insert(0, "*.*")
            return
        filterd_list = self.base_path.glob('*.'+filter_entry[-1])

        self.files_listbox.delete(0, END)

        for item in filterd_list:
            self.files_listbox.insert(END, item.name)
        self.filter_global = filter_entry[-1]
        self.filter_entry.delete(0, END)
        self.filter_entry.insert(0, "*."+filter_entry[-1])




    def del_file_win(self):
        if len(self.files_listbox.curselection()) > 0:
            selected_item_index = self.files_listbox.curselection()[0]
            selection = self.files_listbox.get(selected_item_index)
            answer = messagebox.askyesno("File Deletion", f"Are you sure you want to delete {selection}?")
            if answer is True:
                try:
                    os.remove(self.base_path / selection)
                    print(selection + ' was deleted')
                    self.updateGui()

                except Exception as e:
                    print(e)

    def change_basepath(self,selection):
        self.base_path = (self.base_path / selection).resolve()
        self.updateGui()

    def __updateListboxes(self):

        self.files_in_basepath = \
            (entry for entry in self.base_path.iterdir() if entry.is_file())
        self.dirs_in_basepath = \
            (entry for entry in self.base_path.iterdir() if entry.is_dir())

        self.dirs_listbox.delete(0,END)
        self.files_listbox.delete(0, END)

        if self.base_path == self.base_path / '/':
            self.total_size.set('Root')
        else:
            self.dirs_listbox.insert(END, "..")

        for item in self.dirs_in_basepath:
            self.dirs_listbox.insert(END, item.name)

        for item in self.files_in_basepath:
            self.files_listbox.insert(END, item.name)


    def __calcSize(self):
        utils.threaded_dir_size(self.base_path, self.total_size)

    def updateGui(self):
        self.__calcSize()
        self.__updateListboxes()
        self.current_pathVar.set(self.base_path)

    def new_dir_window(self):
        answer = simpledialog.askstring("Create New Directory", "Enter new directory name:",
                                        parent=self.master)
        if answer is not None:
            self.make_dir(answer)

    def make_dir(self, dir_name):
        try:
            Path.mkdir(self.base_path / dir_name)
            self.updateGui()
        except Exception as e:
            print(e)


def main():
    base_path = Path("C:/")
    master = Tk()
    gui = GUI(master, base_path)

    mainloop()




if __name__ == "__main__":
    main()

import tkinter as tk
from tkinter.ttk import Treeview 
from koneksi import connect_database, close_database, insert_data, get_data
import tkinter.messagebox as mb
from input_data import create_input_form

class Ui:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Koneksi Database")

        #Colom pada tabel
        self.data_structure = {
            "nama": str,
            "jurusan": str 
        }

        # Label dan entry untuk username
        self.label_username = tk.Label(text="Username:")
        self.entry_username = tk.Entry()

        # Label dan entry untuk password
        self.label_password = tk.Label(text="Password:")
        self.entry_password = tk.Entry(show='*')

        # Tombol untuk koneksi dan tutup
        self.button_connect = tk.Button(text="Koneksi", command=self.connect_database)
        self.button_close = tk.Button(text="Tutup", command=self.close_database)

        self.label_status = tk.Label(text="Database Terputus")

        #tombol masukkan data
        self.button_add = tk.Button(text="Tambah Data", command=self.open_add_form)

        # Tabel
        self.table_frame = tk.Frame(self.window)
    
        # Menata layout
        self.label_username.grid(row=0, column=0)
        self.entry_username.grid(row=0, column=1)

        self.label_password.grid(row=1, column=0)
        self.entry_password.grid(row=1, column=1)

        self.button_connect.grid(row=2, column=0)
        self.button_close.grid(row=2, column=1)
        self.label_status.grid(row=3, column=0, columnspan=2)
        self.button_add.grid(row=4, column=0, columnspan=2)
        self.table_frame = tk.Frame(self.window)
        self.table_frame.grid(row=5, column=0, columnspan=2)

        #layout Tabel
        self.treeview = tk.ttk.Treeview(self.table_frame, columns=["mahasiswa_id", "nama", "jurusan"])
        self.treeview.column("#0", width = 0, stretch = "no")
        self.treeview.heading(0,text="mahasiswa_id")  
        self.treeview.heading(1,text="nama")  
        self.treeview.heading(2,text="jurusan")
        self.treeview.pack()

        # Sesion
        self.connection = None
        self.connection_status = False

        self.window.mainloop()

    def connect_database(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        connection = connect_database(username, password)

        if connection is not None:
            print("Koneksi berhasil!")
            self.connection_status = True
            self.update_connection_status()
            data = get_data(username,password, "jurusan")
            self.display_table_tkinter(data)
            
        else:
            print("Koneksi gagal!")
            self.connection_status = False
            self.update_connection_status()
            

    def close_database(self):
        close_database(self.connection)
        self.connection_status = False
        self.update_connection_status()
        self.treeview.delete(*self.treeview.get_children())
    
    def update_connection_status(self):
        if self.connection_status:
            self.label_status.config(text="Database Terhubung")
        else:
            self.label_status.config(text="Database Terputus")
    
    def display_table_tkinter(self, data):
        self.treeview.delete(*self.treeview.get_children())

        for index, row in data.iterrows():
            values = list(row.values)  
            self.treeview.insert('', 'end', values=values)

    def open_add_form(self):
        if self.connection_status:  
            create_input_form(self, self.data_structure, self.on_submit_add)
        else:
            mb.showerror("Error", "Harap terhubung ke database terlebih dahulu!")

    def on_submit_add(self, data):
        insert_data(self.entry_username.get(), self.entry_password.get(), "jurusan", data)

        self.connect_database()
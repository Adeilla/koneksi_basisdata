import tkinter as tk
from tkinter import messagebox as mb


def create_input_form(parent, data_structure, on_submit):

    form_window = tk.Tk()
    form_window.title("Tambah Data")

    labels = []
    entries = []
    for field_name, field_type in data_structure.items():
        label = tk.Label(form_window, text=f"{field_name}:")
        entry = tk.Entry(form_window) if field_type == str else tk.Spinbox(form_window)  # Handle numeric data (optional)
        labels.append(label)
        entries.append(entry)
        label.pack()
        entry.pack()

    def submit_data():
        try:
            data = {label.cget("text").strip(": "): entry.get() for label, entry in zip(labels, entries)}
            validate_data(data)  # Perform data validation (optional)
            on_submit(data)
            form_window.destroy()  # Close the form after submission
            mb.showinfo("Sukses", "Data berhasil ditambahkan!")
        except (ValueError, Exception) as e:
            mb.showerror("Error", f"Error: {str(e)}")

    submit_button = tk.Button(form_window, text="Submit", command=submit_data)
    submit_button.pack()

    # Optional: Allow cancellation (closes form without submission)
    cancel_button = tk.Button(form_window, text="Cancel", command=form_window.destroy)
    cancel_button.pack()

    form_window.mainloop()
    return form_window

def validate_data(data):
    # Replace this with your specific validation rules
    for field_name, value in data.items():
        if not value:
            raise ValueError(f"Value for '{field_name}' cannot be empty")



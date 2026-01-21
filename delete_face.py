import os
from storage import get_faces_dir

import tkinter as tk
from tkinter import messagebox


def delete_face():
    faces_dir = get_faces_dir()

    # Create root window
    root = tk.Tk()
    root.title("Delete Registered Face")
    root.geometry("300x300")

    # Check faces folder
    if not os.path.exists(faces_dir):
        messagebox.showinfo("Delete Face", "No faces folder found.")
        root.destroy()
        return

    files = [f for f in os.listdir(faces_dir) if f.endswith(".npy")]

    if not files:
        messagebox.showinfo("Delete Face", "No registered faces to delete.")
        root.destroy()
        return

    # Label
    label = tk.Label(root, text="Select a user to delete:")
    label.pack(pady=10)

    # Listbox
    listbox = tk.Listbox(root)
    listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

    for file in files:
        listbox.insert(tk.END, file.replace(".npy", ""))

    # Delete button callback
    def on_delete():
        selection = listbox.curselection()

        if not selection:
            messagebox.showwarning("Delete Face", "Please select a user.")
            return

        index = selection[0]
        name = files[index].replace(".npy", "")
        file_path = os.path.join(faces_dir, files[index])

        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete '{name}'?"
        )

        if not confirm:
            return

        try:
            os.remove(file_path)
            messagebox.showinfo("Delete Face", f"Deleted: {name}")
            root.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete:\n{e}")

    # Delete button
    delete_button = tk.Button(root, text="Delete Selected", command=on_delete)
    delete_button.pack(pady=10)

    # Cancel button
    cancel_button = tk.Button(root, text="Cancel", command=root.destroy)
    cancel_button.pack(pady=5)

    # Start GUI loop
    root.mainloop()

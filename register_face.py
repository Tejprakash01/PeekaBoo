from storage import get_faces_dir
import os
import numpy as np

import tkinter as tk
from tkinter import simpledialog, messagebox


def register_face():
    # Create hidden root window for dialogs
    root = tk.Tk()
    root.withdraw()

    # Ask user name
    name = simpledialog.askstring("Register Face", "Enter person name:")

    if not name:
        messagebox.showinfo("Register Face", "Registration cancelled.")
        root.destroy()
        return

    # Heavy imports only when needed
    try:
        import cv2
        import face_recognition
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load camera modules:\n{e}")
        root.destroy()
        return

    cap = None
    encodings = []
    count = 0

    try:
        cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            messagebox.showerror("Error", "Could not open camera.")
            return

        messagebox.showinfo(
            "Register Face",
            "Look at the camera.\nCapturing 20 samples."
        )

        while count < 20:
            ret, frame = cap.read()
            if not ret:
                continue

            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            faces = face_recognition.face_locations(rgb)

            if len(faces) == 1:
                encoding = face_recognition.face_encodings(rgb, faces)[0]
                encodings.append(encoding)
                count += 1

                top, right, bottom, left = faces[0]
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

            cv2.imshow("Register Face - Peekaboo", frame)

            # ESC to cancel
            if cv2.waitKey(1) & 0xFF == 27:
                messagebox.showinfo("Register Face", "Registration cancelled.")
                return

    finally:
        # Always release camera
        if cap is not None:
            cap.release()

        cv2.destroyAllWindows()

    # Save face data
    faces_dir = get_faces_dir()
    os.makedirs(faces_dir, exist_ok=True)

    file_path = os.path.join(faces_dir, f"{name}.npy")
    np.save(file_path, encodings)

    messagebox.showinfo(
        "Register Face",
        f"Face registered successfully!\nSaved as: {name}"
    )

    root.destroy()

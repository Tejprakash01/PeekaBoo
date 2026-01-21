import os
import time
import numpy as np
import cv2
from datetime import datetime

from storage import get_intruder_dir, get_faces_dir
from notify import send_alert


def load_known_faces():
    known_encodings = []
    known_names = []

    print("[engine] loading known faces...")

    faces_dir = get_faces_dir()

    if not os.path.exists(faces_dir):
        print("[engine] no registered users found")
        return known_encodings, known_names

    for file in os.listdir(faces_dir):
        if file.endswith(".npy"):
            path = os.path.join(faces_dir, file)
            data = np.load(path)
            name = file.replace(".npy", "")

            for enc in data:
                known_encodings.append(enc)
                known_names.append(name)

    print("[engine] loaded users:", list(set(known_names)))
    return known_encodings, known_names


def detection_loop(controller):
    try:
        import face_recognition
        print("[engine] face_recognition imported successfully")
    except Exception as e:
        print("[engine] FATAL: failed to import face_recognition:", e)
        return

    print("[engine] detection loop started, waiting for Start...")

    cap = None
    last_intruder_time = 0
    intruder_frames = 0

    intruder_dir = get_intruder_dir()
    os.makedirs(intruder_dir, exist_ok=True)
    print("[engine] intruder directory:", intruder_dir)

    known_encodings = []
    known_names = []

    last_running_state = False

    while True:

        # If paused, release camera
        if not controller.running:
            if cap is not None:
                print("[engine] paused, releasing camera")
                cap.release()
                cap = None
                cv2.destroyAllWindows()

            last_running_state = False
            time.sleep(0.5)
            continue

        # Detect start or resume
        if not last_running_state:
            print("[engine] detected START / RESUME")
            known_encodings, known_names = load_known_faces()
            intruder_frames = 0
            last_intruder_time = 0
            last_running_state = True

        # Open camera if needed
        if cap is None:
            print("[engine] trying to open camera...")
            cap = cv2.VideoCapture(0)

            if not cap.isOpened():
                print("[engine] ERROR: camera could not be opened")
                controller.running = False
                cap = None
                time.sleep(3)
                continue

            print("[engine] camera opened successfully")

        # Read frame
        ret, frame = cap.read()
        if not ret:
            print("[engine] WARNING: failed to read frame")
            time.sleep(0.05)
            continue

        # Convert to RGB
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Detect faces
        faces = face_recognition.face_locations(
            rgb,
            number_of_times_to_upsample=1,
            model="hog"
        )

        encodings = face_recognition.face_encodings(rgb, faces)

        any_intruder_in_frame = False

        # Process each face
        for (top, right, bottom, left), face_enc in zip(faces, encodings):

            face_width = right - left
            face_height = bottom - top
            face_area = face_width * face_height

            # Ignore very small faces
            if face_area < 5000:
                continue

            is_authorized = False
            label = "Intruder"
            color = (0, 0, 255)   # red

            if len(known_encodings) > 0:
                distances = face_recognition.face_distance(known_encodings, face_enc)
                best_match_index = np.argmin(distances)
                best_distance = distances[best_match_index]

                print("[engine] best distance:", best_distance)

                # Authorized face
                if best_distance < 0.65:
                    is_authorized = True
                    label = known_names[best_match_index]
                    color = (0, 255, 0)   # green
                    print("[engine] authorized user:", label)

            # If not authorized, intruder present
            if not is_authorized:
                any_intruder_in_frame = True

            # Draw box
            cv2.rectangle(frame, (left, top), (right, bottom), color, 2)

            # Draw label
            cv2.putText(
                frame,
                label,
                (left, top - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                color,
                2
            )

        # Update intruder counter
        if any_intruder_in_frame:
            intruder_frames += 1
            print("[engine] intruder frame count:", intruder_frames)
        else:
            intruder_frames = 0

        # Trigger alert and save snapshot
        if intruder_frames >= 1:
            current_time = time.time()

            if current_time - last_intruder_time > 10:
                last_intruder_time = current_time

                time_str = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = os.path.join(
                    intruder_dir,
                    f"intruder_{time_str}.jpg"
                )

                success = cv2.imwrite(filename, frame)

                if success:
                    print("PEEKABOO ALERT: INTRUDER DETECTED")
                    print("Snapshot saved:", filename)
                else:
                    print("[engine] ERROR: failed to save snapshot:", filename)

                try:
                    send_alert(
                        "Peekaboo Alert",
                        "Intruder detected. Snapshot saved."
                    )
                    print("[engine] notification sent successfully")
                except Exception as e:
                    print("[engine] ERROR sending notification:", e)

        # Show preview window
        if controller.preview:
            cv2.imshow("Peekaboo Preview", frame)

            if cv2.waitKey(1) & 0xFF == 27:
                controller.preview = False
                cv2.destroyAllWindows()

        time.sleep(0.01)

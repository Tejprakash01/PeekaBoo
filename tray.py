import os
import sys
import threading

print("[tray] import started")


# PyInstaller safe resource loader
def resource_path(relative_path):
    if getattr(sys, 'frozen', False):
        # In PyInstaller onefile mode, all files are inside _MEIPASS
        base_path = sys._MEIPASS
    else:
        # Normal python run
        base_path = os.path.dirname(os.path.abspath(__file__))

    return os.path.join(base_path, relative_path)


def create_tray(controller):

    print("[tray] create_tray started")

    # Import your modules late (important for PyInstaller)
    from register_face import register_face
    from delete_face import delete_face
    from utils import open_faces_folder, open_intruder_folder

    # Load pystray
    import pystray
    from pystray import MenuItem as item
    from PIL import Image

    print("[tray] pystray imported successfully")

    # Callbacks
    def start(icon, item):
        controller.start()

    def pause(icon, item):
        controller.pause()

    def resume(icon, item):
        controller.resume()

    def toggle_preview(icon, item):
        controller.toggle_preview()

    def register_user(icon, item):
        threading.Thread(target=register_face, daemon=True).start()

    def delete_user(icon, item):
        threading.Thread(target=delete_face, daemon=True).start()

    def open_faces(icon, item):
        open_faces_folder()

    def open_intruders(icon, item):
        open_intruder_folder()

    def exit_app(icon, item):
        controller.pause()
        icon.stop()
        os._exit(0)

    # Load tray icon safely
    icon_path = resource_path("icon.ico")
    print("[tray] loading icon from:", icon_path)

    if not os.path.exists(icon_path):
        print("[tray] ERROR: icon.ico not found, tray will not start")
        return

    image = Image.open(icon_path)

    # Menu
    menu = (
        item("Start Monitoring", start),
        item("Pause Monitoring", pause),
        item("Resume Monitoring", resume),

        item(
            "Preview",
            toggle_preview,
            checked=lambda item: controller.preview
        ),

        item("Register New Face", register_user),
        item("Delete Face", delete_user),

        item("Open Faces Folder", open_faces),
        item("Open Intruders Folder", open_intruders),

        item("Exit", exit_app),
    )

    icon = pystray.Icon(
        "Peekaboo",
        image,
        "Peekaboo - Screen Privacy Guard",
        menu
    )

    print("[tray] starting tray icon now...")

    # This MUST block forever
    icon.run()

    # This line should never be reached
    print("[tray] icon.run() returned - this should not happen")

import sys
import os
import threading

print("MAIN STARTED")

try:
    print("Importing controller...")
    from controller import Controller
    print("Controller imported")

    print("Importing engine...")
    from engine import detection_loop
    print("Engine imported")

    print("Importing tray...")
    from tray import create_tray
    print("Tray imported")

    print("All imports OK")

except Exception as e:
    print("IMPORT FAILED:", e)
    input("Press Enter to exit...")
    sys.exit(1)


def main():
    print("Entered main()")

    controller = Controller()
    print("Controller instance created")

    print("Starting engine thread...")

    engine_thread = threading.Thread(
        target=detection_loop,
        args=(controller,),
        daemon=False   # MUST be False
    )

    engine_thread.start()

    print("Engine thread started")

    print("Starting tray...")
    create_tray(controller)


if __name__ == "__main__":
    main()

import platform
import subprocess
import threading

system = platform.system()

# Try to import plyer safely
try:
    from plyer import notification
    use_plyer = True
    print("[notify] plyer available")
except Exception as e:
    use_plyer = False
    print("[notify] plyer not available:", e)


def _send_windows_toast(title, message):
    try:
        import pythoncom
        pythoncom.CoInitialize()

        from win10toast import ToastNotifier
        toaster = ToastNotifier()

        toaster.show_toast(
            title,
            message,
            duration=5,
            threaded=False   # IMPORTANT: block until shown
        )

        print("[notify] Windows toast shown successfully")

    except Exception as e:
        print("[notify] Windows notifier failed:", e)


def send_alert(title, message):
    print("[notify] send_alert called")

    # FIRST TRY: plyer (if it works)
    if use_plyer:
        try:
            notification.notify(
                title=title,
                message=message,
                timeout=5
            )
            print("[notify] plyer notification sent")
            return
        except Exception as e:
            print("[notify] plyer failed, falling back:", e)

    # WINDOWS
    if system == "Windows":
        print("[notify] using Windows notifier")

        # Run in a NEW thread with proper COM init
        t = threading.Thread(
            target=_send_windows_toast,
            args=(title, message),
            daemon=True
        )
        t.start()
        return

    # macOS
    elif system == "Darwin":
        try:
            safe_title = title.replace('"', '\\"')
            safe_message = message.replace('"', '\\"')

            script = f'display notification "{safe_message}" with title "{safe_title}"'
            subprocess.run(["osascript", "-e", script])
            print("[notify] macOS notification sent")
        except Exception as e:
            print("[notify] macOS notification failed:", e)

    # Linux
    elif system == "Linux":
        try:
            subprocess.run(["notify-send", title, message])
            print("[notify] Linux notification sent")
        except Exception as e:
            print("[notify] Linux notification failed:", e)

    else:
        print("[notify] Unsupported OS for notifications")

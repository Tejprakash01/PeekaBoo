# Peekaboo – Screen Privacy Guard

Peekaboo is a Windows desktop privacy application that runs in the system tray and uses face recognition to detect unauthorized people looking at your screen. When an intruder is detected, it captures a snapshot and sends a desktop notification.

---

## Features

* System tray application (runs in background)
* Register authorized user faces
* Delete registered faces
* Start / Pause / Resume monitoring
* Live preview window (optional)
* Intruder detection with snapshot saving
* Desktop notification alert

---

## System Requirements

* OS: Windows 10 / 11
* Python: 3.9 or 3.10 (recommended)
* Webcam

> Note: `face_recognition` and `dlib` are sensitive to Python version. Avoid Python 3.11+.

---

## Project Structure

```
peakaboo/
│
├── main.py
├── tray.py
├── engine.py
├── controller.py
├── register_face.py
├── delete_face.py
├── notify.py
├── storage.py
├── utils.py
├── icon.ico
├── requirements.txt
├── README.md
└── .gitignore
```

---

## Installation (From Source)

### 1. Clone the repository

```bash
git clone https://github.com/your-username/peekaboo.git
cd peekaboo
```

### 2. Create virtual environment (recommended)

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

If `face_recognition` fails to install:

```bash
pip install cmake
pip install dlib
pip install face-recognition
```

---

## Running the Project (Development Mode)

```bash
python main.py
```

After running:

* Tray icon appears in system tray
* Icon will appear in arrow button near wifi and bluetooth
* Right-click tray icon to access menu

---

## Tray Menu Functions

* **Start Monitoring**
  Starts camera and begins face detection

* **Pause Monitoring**
  Stops camera and pauses detection

* **Resume Monitoring**
  Resumes detection after pause

* **Preview**
  Shows live camera preview window

* **Register New Face**
  Opens camera and registers a new authorized user

* **Delete Face**
  Opens UI to delete an existing registered user

* **Open Faces Folder**
  Opens folder where registered faces are stored

* **Open Intruders Folder**
  Opens folder where intruder snapshots are saved

* **Exit**
  Closes the application

---

## Registering a Face

1. Click **Register New Face** from tray
2. Enter user name in dialog
3. Look at the camera
4. 20 samples are captured
5. Face encoding is saved in:

```
C:\Users\<YourName>\AppData\Local\<User>\Peekaboo\faces
```

---

## Intruder Detection

* When an unknown face appears:

  * After a few frames, it is confirmed as intruder
  * Snapshot is saved in:

```
C:\Users\<YourName>\AppData\Local\<User>\Peekaboo\intruders
```

* Desktop notification is shown

---

## Building Standalone EXE (PyInstaller)

### 1. Install PyInstaller

```bash
pip install pyinstaller
```

### 2. Build Command (No Console, Tray App)

Use this exact command:

```powershell
pyinstaller --onefile --noconsole `
  --hidden-import=face_recognition `
  --hidden-import=face_recognition.api `
  --hidden-import=face_recognition_models `
  --hidden-import=win10toast `
  --hidden-import=pythoncom `
  --hidden-import=plyer `
  --hidden-import=plyer.platforms.win.notification `
  --hidden-import=pystray `
  --hidden-import=pystray._win32 `
  --hidden-import=PIL `
  --hidden-import=PIL.Image `
  --hidden-import=PIL.ImageSequence `
  --hidden-import=PIL.ImageMath `
  --add-data "C:\\Users\\Varun\\anaconda3\\envs\\peekaboo\\lib\\site-packages\\face_recognition_models\\models;face_recognition_models\\models" `
  --add-data "icon.ico;." `
  main.py
```

After build, EXE will be in:

```
dist/main.exe
```

---

## Running the Built EXE

Double-click:

```
dist\main.exe
```

* Tray icon should appear
* No console window will open

---

## Future Scope: Linux & macOS Support

Peekaboo is currently optimized and tested on Windows. Adding full support for Linux and macOS is a planned future enhancement. Below are the key areas that need changes.

### 1. Tray Icon (pystray backend)

* Windows uses pystray win32 backend.
* Linux uses GTK or AppIndicator backend.
* macOS uses Cocoa backend.

Planned change:

* Detect OS using platform.system()
* Let pystray auto-select backend per OS.

### 2. Notifications

Current:

* Uses win10toast and plyer on Windows.

For Linux:

* Use notify-send (libnotify)
* Dependency: libnotify-bin

For macOS:

* Use osascript notifications

Planned change:

* Unified OS-based dispatcher in notify.py

### 3. Camera Backend (OpenCV)

Current:

* Uses default Windows backend.

For Linux:

* Use V4L2 backend
* May require: sudo apt install v4l-utils

For macOS:

* Use AVFoundation backend

Planned change:

* Select VideoCapture backend based on OS.

### 4. Face Recognition Dependencies

Issues:

* dlib is hard to compile on Linux and macOS.
* Apple Silicon needs special wheels.

Planned improvements:

* Provide Docker build
* Optional lighter models (MediaPipe / OpenCV DNN)

### 5. Build System

Current:

* PyInstaller onefile for Windows.

For Linux:

* Build on Linux target OS.

For macOS:

* Use --windowed and code signing.

Planned change:

* Separate build scripts for each OS.

### 6. Settings System

Planned additions:

* settings.json for:

  * Camera index
  * Detection threshold
  * Intruder cooldown
  * Preview default

### 7. Cross-Platform Packaging

Future goals:

* Windows: Inno Setup installer
* Linux: AppImage or .deb
* macOS: .dmg bundle

---

## Common Issues

### 1. Camera not opening

* Close other apps using camera (Zoom, Teams, Browser)
* Restart system

### 2. face_recognition install error

Use:

```bash
pip install cmake
pip install dlib
pip install face-recognition
```

### 3. EXE works on your PC but not on friend's PC

* Friend must install:

  * Microsoft Visual C++ Redistributable
  * Windows 10/11 updates

---

## Author

Developed by Tej Prakash Tak

Peekaboo – Screen Privacy Guard

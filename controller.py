class Controller:
    def __init__(self):
        self.running = False     
        self.preview = False     
        self.alert = False

    def start(self):
        self.running = True
        print("Peekaboo: Monitoring started")

    def pause(self):
        self.running = False
        print("Peekaboo: Monitoring paused")

    def resume(self):
        self.running = True
        print("Peekaboo: Monitoring resumed")

    def toggle_preview(self):
        self.preview = not self.preview
        state = "ON" if self.preview else "OFF"
        print(f"Peekaboo: Preview {state}")

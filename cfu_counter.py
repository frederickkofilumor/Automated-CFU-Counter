"""
Automated CFU Counter
---------------------
This application runs on a Raspberry Pi 4B with a 3.5" touchscreen display (480x320).
It uses a Pi Camera to capture agar plate images in real-time and a YOLOv8n model
to detect and count Colony Forming Units (CFUs). Results are displayed on a
Kivy-based GUI with live video feed and bounding boxes.
"""

from kivy.config import Config

# --- Configure Kivy for Raspberry Pi 3.5" display (480x320, fullscreen, no resize) ---
Config.set('graphics', 'fullscreen', '1')
Config.set('graphics', 'width', '480')
Config.set('graphics', 'height', '320')
Config.set('graphics', 'resizable', '0')

# --- Import libraries ---
import cv2
import time
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from picamera2 import Picamera2
from ultralytics import YOLO

# --- Load YOLO model ---
# Place "best.pt" in the same folder as this script before running
model = YOLO("best.pt")


class CFUApp(App):
    """Main application class for the CFU Counter."""

    def build(self):
        """Builds the Kivy GUI layout."""
        self.layout = BoxLayout(orientation='vertical', spacing=5, padding=5)

        # Camera feed display widget
        self.img_widget = Image()
        self.layout.add_widget(self.img_widget)

        # Label for CFU count
        self.label = Label(text="Number of CFUs: 0", font_size=18, size_hint=(1, 0.1))
        self.layout.add_widget(self.label)

        # Buttons
        self.start_btn = Button(text="Start Camera", size_hint=(1, 0.1))
        self.start_btn.bind(on_press=self.start_camera)
        self.layout.add_widget(self.start_btn)

        self.stop_btn = Button(text="Stop Camera", size_hint=(1, 0.1))
        self.stop_btn.bind(on_press=self.stop_camera)
        self.layout.add_widget(self.stop_btn)

        self.close_btn = Button(text="Close App", size_hint=(1, 0.1))
        self.close_btn.bind(on_press=self.stop_app)
        self.layout.add_widget(self.close_btn)

        # Camera setup
        self.picam2 = Picamera2()
        self.capture = None   # Flag to track if camera is running
        self.event = None     # Clock event for periodic updates

        return self.layout

    def start_camera(self, instance):
        """Starts the Pi Camera and schedules periodic frame updates."""
        if self.capture is None:
            config = self.picam2.create_preview_configuration(main={"size": (640, 480)})
            self.picam2.configure(config)
            self.picam2.start()
            time.sleep(2)  # let camera warm up
            self.capture = True
            # Schedule the update method at ~10 FPS
            self.event = Clock.schedule_interval(self.update, 1.0 / 10.0)

    def stop_camera(self, instance):
        """Stops the camera and cancels the update event."""
        if self.capture:
            self.picam2.stop()
            self.capture = None
        if self.event:
            self.event.cancel()
            self.event = None

    def update(self, dt):
        """Captures frames, runs YOLO detection, and updates the GUI."""
        if self.capture:
            frame = self.picam2.capture_array()
            if frame is not None:

                # Ensure frame has 3 channels (BGR)
                if frame.shape[-1] == 4:
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)

                # Run YOLO detection
                results = model(frame)
                count = len(results[0].boxes)

                # Draw bounding boxes around detected colonies
                for box in results[0].boxes:
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

                # Update label with CFU count
                self.label.text = f"Number of CFUs: {count}"

                # Convert OpenCV frame (BGR) to Kivy texture (RGB)
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                buf = frame_rgb.tobytes()
                texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='rgb')
                texture.blit_buffer(buf, colorfmt='rgb', bufferfmt='ubyte')
                self.img_widget.texture = texture

    def stop_app(self, instance):
        """Stops the camera and closes the app."""
        self.stop_camera(instance)
        App.get_running_app().stop()


# --- Run the app ---
if __name__ == "__main__":
    CFUApp().run()

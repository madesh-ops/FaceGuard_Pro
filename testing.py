import cv2
import mediapipe as mp
import os
import numpy as np
import tkinter as tk
import threading

mp_face_mesh = mp.solutions.face_mesh
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()

NO_FACE_THRESHOLD = 30  # Number of frames with no face before locking
no_face_counter = 0
SLEEP_COMMAND = 'rundll32.exe user32.dll,LockWorkStation'
locked = False  # Move locked to global scope so dashboard can access it



# GUI Dashboard setup
def update_dashboard():
    global locked
    if 'dashboard' in globals():
        dashboard.face_status_var.set(f"Face: {'Detected' if no_face_counter == 0 else 'Not Detected'}")
        dashboard.lock_var.set(f"Locked: {'Yes' if locked else 'No'}")
        dashboard.after(500, update_dashboard)

class Dashboard(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Face/Eye Monitor Dashboard")
        self.geometry("350x180")
        self.resizable(False, False)
        self.configure(bg="#23272f")
        # Header
        header = tk.Label(self, text="Face/Eye Monitor", font=("Segoe UI", 18, "bold"), fg="#00bfff", bg="#23272f")
        header.pack(pady=(15, 10))
        # Status Frame
        status_frame = tk.Frame(self, bg="#23272f")
        status_frame.pack(pady=5, fill=tk.BOTH, expand=True)
        # Face Status
        self.face_status_var = tk.StringVar()
        face_label = tk.Label(status_frame, textvariable=self.face_status_var, font=("Segoe UI", 14, "bold"), fg="#2ecc71", bg="#23272f")
        face_label.pack(pady=5, anchor="w", padx=30)
        # Lock Status
        self.lock_var = tk.StringVar()
        lock_label = tk.Label(status_frame, textvariable=self.lock_var, font=("Segoe UI", 12), fg="#e74c3c", bg="#23272f")
        lock_label.pack(pady=5, anchor="w", padx=30)
        # Footer
        footer = tk.Label(self, text="© 2025 Face/Eye Monitor", font=("Segoe UI", 9), fg="#888", bg="#23272f")
        footer.pack(side=tk.BOTTOM, pady=(0, 8))
        self.protocol("WM_DELETE_WINDOW", self.on_close)
    def on_close(self):
        self.destroy()
        os._exit(0)

def run_dashboard():
    global dashboard
    dashboard = Dashboard()
    dashboard.after(500, update_dashboard)  # Ensure update_dashboard is scheduled after window is created
    dashboard.mainloop()

# Start the dashboard before entering the main loop
threading.Thread(target=run_dashboard, daemon=True).start()

with mp_face_mesh.FaceMesh(
    max_num_faces=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
) as face_mesh:
    while True:
        success, image = cap.read()
        if not success:
            continue
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = face_mesh.process(image)
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        locked = False
        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                # Use float32 for landmarks to reduce memory
                landmarks = np.array([[lm.x, lm.y] for lm in face_landmarks.landmark], dtype=np.float32)
                h, w, _ = image.shape
                landmarks = landmarks * [w, h]
                # Draw face mesh
                mp.solutions.drawing_utils.draw_landmarks(
                    image=image,
                    landmark_list=face_landmarks,
                    connections=mp_face_mesh.FACEMESH_TESSELATION,
                    landmark_drawing_spec=mp.solutions.drawing_utils.DrawingSpec(thickness=1, circle_radius=1),
                    connection_drawing_spec=mp.solutions.drawing_utils.DrawingSpec(thickness=1, circle_radius=1)
                )
            no_face_counter = 0
        else:
            no_face_counter += 1
            if no_face_counter > NO_FACE_THRESHOLD and not locked:
                os.system(SLEEP_COMMAND)
                no_face_counter = 0
                locked = True
        # Only show the window if needed
        cv2.imshow('Face/Eye Detection', image)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
cap.release()
cv2.destroyAllWindows()

# eye_tracker.py
import cv2
import mediapipe as mp
import time

class EyeTracker:
    def __init__(self, ear_threshold=0.15):
        # MediaPipe
        self.mp_face = mp.solutions.face_mesh
        self.face_mesh = self.mp_face.FaceMesh(refine_landmarks=True)
        self.mp_draw = mp.solutions.drawing_utils

        # Eye landmarks
        self.LEFT_EYE = [33, 160, 158, 133, 153, 144]
        self.RIGHT_EYE = [362, 385, 387, 263, 373, 380]

        self.ear_threshold = ear_threshold
        self.eyes_closed_start = None
        self.ear_history = []
        self.fatigue_active = False  # Track if fatigue is currently active

    def eye_openness(self, landmarks, eye_points):
        vertical = abs(landmarks[eye_points[1]].y - landmarks[eye_points[5]].y)
        horizontal = abs(landmarks[eye_points[0]].x - landmarks[eye_points[3]].x)
        return vertical / horizontal

    def process_frame(self, frame):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = self.face_mesh.process(rgb)

        eyes_closed_duration = 0
        left_eye, right_eye = None, None

        if result.multi_face_landmarks:
            face_landmarks = result.multi_face_landmarks[0]  # first face only
            h, w, _ = frame.shape
            landmarks = face_landmarks.landmark

            # Draw eye landmarks
            for idx in self.LEFT_EYE + self.RIGHT_EYE:
                x = int(landmarks[idx].x * w)
                y = int(landmarks[idx].y * h)
                cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)

            left_eye = self.eye_openness(landmarks, self.LEFT_EYE)
            right_eye = self.eye_openness(landmarks, self.RIGHT_EYE)

            # Smooth EAR over last 3 frames
            avg_ear = (left_eye + right_eye) / 2.0
            self.ear_history.append(avg_ear)
            if len(self.ear_history) > 3:
                self.ear_history.pop(0)
            smoothed_ear = sum(self.ear_history) / len(self.ear_history)

            # Check if eyes closed
            if smoothed_ear < self.ear_threshold:
                if self.eyes_closed_start is None:
                    self.eyes_closed_start = time.time()
                eyes_closed_duration = time.time() - self.eyes_closed_start
            else:
                self.eyes_closed_start = None
                eyes_closed_duration = 0

            # Update fatigue active state (only when face is detected)
            if eyes_closed_duration >= 4.0 and not self.fatigue_active:
                self.fatigue_active = True
            elif eyes_closed_duration < 4.0:
                self.fatigue_active = False

        # Set fatigue flag based on active state (persists even without face detection)
        fatigue = "Yes" if self.fatigue_active else "No"

        return left_eye, right_eye, eyes_closed_duration, fatigue, frame
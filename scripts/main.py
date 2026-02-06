# main.py
import cv2
import os
import csv
import time
import platform
from eye_tracker import EyeTracker
from typing_tracker import TypingTracker
from mouse_tracker import MouseTracker

# Beep function
def play_alert():
    system = platform.system()
    if system == "Windows":
        import winsound
        winsound.Beep(1000, 500)
    else:
        print("\a")

# CSV setup
os.makedirs("data", exist_ok=True)
csv_file = os.path.join("data", "fatigue_log.csv")

with open(csv_file, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow([
        "Time(s)", "LeftEAR", "RightEAR", "EyesClosed(s)",
        "TypingCPM", "MouseIdle(s)",
        "EyeFatigue", "BehaviorFatigue"
    ])

# Initialize trackers
eye_tracker = EyeTracker()
typing_tracker = TypingTracker(window=60)
mouse_tracker = MouseTracker()

typing_tracker.start_listener()
mouse_tracker.start_listener()

cap = cv2.VideoCapture(0)
start_time = time.time()

# Alert state trackers
last_eye_fatigue = "No"
last_behavior_fatigue = "No"
fatigue_episodes = []


# Main Loop
while True:

    ret, frame = cap.read()
    if not ret:
        break

    # Mirror webcam
    frame = cv2.flip(frame, 1)

    #Eye Tracking 
    left_eye, right_eye, eyes_closed_duration, eye_fatigue, frame = \
        eye_tracker.process_frame(frame)

    #Typing
    typing_cpm = typing_tracker.get_typing_speed()

    # Mouse
    mouse_idle = mouse_tracker.get_idle_time()

    #  Behaviour Fatigue (Mouse + Keyboard) 
    behavior_fatigue = "No"

    #thresholds values
    if mouse_idle > 90 and typing_cpm < 10:
        behavior_fatigue = "Yes"

    # Alerts 
    now = time.time()

    # only once per event
    if eye_fatigue == "Yes" and last_eye_fatigue == "No":
        play_alert()
        fatigue_episodes.append(now)

    last_eye_fatigue = eye_fatigue

    # Behaviour fatigue beep
    if behavior_fatigue == "Yes" and last_behavior_fatigue == "No":
        play_alert()

    last_behavior_fatigue = behavior_fatigue

    #  Session Rest Reminder (90 min)
    session_duration = now - start_time
    long_session = session_duration > 5400  # 90 minutes

    #  Repeated fatigue logic
    fatigue_episodes = [t for t in fatigue_episodes if t > now - 900]
    repeated_fatigue = len(fatigue_episodes) > 3

    # Display 
    if left_eye is not None:

        cv2.putText(frame, f"Left EAR: {left_eye:.2f}", (30,30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,0), 2)

        cv2.putText(frame, f"Right EAR: {right_eye:.2f}", (30,60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,0), 2)

        cv2.putText(frame, f"Eyes Closed: {eyes_closed_duration:.2f}s", (30,90),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,255), 2)

        cv2.putText(frame, f"Typing CPM: {typing_cpm:.1f}", (30,120),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)

        cv2.putText(frame, f"Mouse Idle: {mouse_idle:.1f}s", (30,150),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)

        # Eye fatigue message
        if eye_fatigue == "Yes":
            cv2.putText(frame, "FATIGUE DETECTED (Eyes)", (30,180),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,255), 2)

        # Behaviour fatigue message
        if behavior_fatigue == "Yes":
            cv2.putText(frame, "LOW ACTIVITY DETECTED", (30,210),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,255), 2)

        # Rest suggestion
        if repeated_fatigue or long_session:
            cv2.putText(frame, "A BREAK IS RECOMMENDED", (30,240),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,0,255), 3)

    #  Log CSV 
    with open(csv_file, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            round(now - start_time, 2),
            round(left_eye,4) if left_eye else None,
            round(right_eye,4) if right_eye else None,
            round(eyes_closed_duration,2),
            round(typing_cpm,2),
            round(mouse_idle,2),
            eye_fatigue,
            behavior_fatigue
        ])

    cv2.imshow("Fatigue Tracker", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break


# Cleanup
cap.release()
cv2.destroyAllWindows()

print(f"Fatigue log saved in {csv_file}")

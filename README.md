# Fatigue Detection System

Real-time fatigue monitoring system that tracks **eye closure**, **typing speed**, and **mouse activity** to detect work fatigue and provide audio alerts.

## Features

- **Eye Fatigue Detection** - Monitors Eye Aspect Ratio (EAR) for prolonged eye closure

- **Behavioral Fatigue Detection** - Tracks typing speed (CPM) and mouse idle time

- **Real-time Audio Alerts** - Beeps on fatigue detection (Windows/Linux compatible)

- **CSV Data Logging** - Records all metrics with timestamps

- **Live Visual Feedback** - On-screen metrics and fatigue status

- **Session Monitoring** - 90-minute break reminders and repeated fatigue detection

**Real-time eye + behavior fatigue detector with alerts & CSV logging**

## 🛠️ Tech Stack

- Python 3.10

- OpenCV - Computer vision

- MediaPipe - Face landmarks

- NumPy - Array processing

- pynput - Keyboard & mouse tracking

## FatigueTracker folder breakdown

```text
FatigueTracker/
│
├── scripts/
│   ├── main.py
│   ├── eye_tracker.py
│   ├── typing_tracker.py
│   └── mouse_tracker.py
│
├── data/
│   ├── fatigue_log.csv
│   └── keyboard_mouse.csv
│
└── requirements.txt
```




## 📊 Metrics Tracked

| Metric | Description | Fatigue Threshold |
|--------|-------------|-------------------|
| Left/Right EAR | Eye Aspect Ratio | Eyes closed > threshold |
| Typing CPM | Characters per minute | < 10 CPM |
| Mouse Idle | Seconds without movement | > 90 seconds |
| Session Time | Total runtime | > 90 minutes |








##  Quick Start

### STEP 1: Create Virtual Environment :-

py -3.10 -m venv myenv



### STEP 2: Activate Environment :-

.\myenv\Scripts\Activate.ps1

&nbsp;- (myenv) appears in console



### STEP 3: Upgrade pip :-

python -m pip install --upgrade pip



### STEP 4: Install Dependencies :-

pip install -r requirements.txt



### STEP 5: Run Project :-

python scripts\\main.py



### STEP 6: Press esc to exit.





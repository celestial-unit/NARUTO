from flask import Flask, Response, render_template, request, redirect, url_for
from ultralytics import YOLO
import cv2
import mediapipe as mp
import time
import random
import os
import json
from collections import deque
import torch

# ---------------- CONFIG -----------------
MODEL_PATH = "best_naruto_signs_7.pt"
CAM_ID = 0
IMG_SIZE = 640
CONF_THRES = 0.25

GESTURE_HOLD_TIME = 2
SELECTION_HOLD_TIME = 2
MAX_SEQUENCE_LENGTH = 20
TIME_ATTACK_DURATION = 60

JUTSU_HAND_SIGNS = {
    "Shadow Clone Jutsu": ["Tiger"],
    "Chidori": ["Ox", "Hare", "Monkey"],
    "Transformation Jutsu": ["Ram", "Serpent", "Tiger"],
    "Body Flicker Jutsu": ["Serpent"],
    "Phoenix Fire Jutsu": ["Tiger", "Serpent", "Dragon"]
}

MASTER_LEVELS = {
    "Novice": 1,
    "Intermediate": 3,
    "Master": 5
}

STATS_FILE = "stats.json"
GESTURE_LOG_FILE = "gestures.json"

# -----------------------------------------

app = Flask(__name__)
model = YOLO(MODEL_PATH)
device = 0 if torch.cuda.is_available() else "cpu"

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.7)

# Global States
phase = "menu"
mode = None
selected_jutsu = None
selection_start_time = None
last_selected_box = None
user_sequence = deque(maxlen=MAX_SEQUENCE_LENGTH)
expected_sequence = []
last_detected_label = None
label_start_time = None
pause_start_time = None
result_message = ""
result_color = (255, 255, 255)
start_time = None
elapsed_time = None
JUTSU_BOXES = {}
time_attack_start = None
time_attack_completed = 0
detected_gestures = deque(maxlen=5)
gesture_display_time = 2
gesture_memory = []
gestures_done = 0  # New for time attack

BOX_WIDTH = 180
BOX_HEIGHT = 45
GAP = 20

if not os.path.exists(STATS_FILE):
    with open(STATS_FILE, "w") as f:
        json.dump({}, f)

if not os.path.exists(GESTURE_LOG_FILE):
    with open(GESTURE_LOG_FILE, "w") as f:
        json.dump([], f)

# --- Helper Functions ---
def clean_gestures_json(file_path='gestures.json'):
    with open(file_path, 'r') as f:
        data = json.load(f)

    cleaned_data = [{"sign": item["gesture"]} for item in data]

    with open(file_path, 'w') as f:
        json.dump(cleaned_data, f, indent=4)
def inside_box(x, y, box):
    x1, y1, x2, y2 = box
    return x1 <= x <= x2 and y1 <= y <= y2

def match_sequence(user_seq, target_seq):
    return list(user_seq) == target_seq

def save_gesture_to_json(label):
    gesture_memory.append({"gesture": label, "timestamp": time.time()})
    with open(GESTURE_LOG_FILE, "w") as f:
        json.dump(gesture_memory, f, indent=4)

def update_stats(jutsu_name, success, completion_time=None):
    with open(STATS_FILE, "r+") as f:
        stats = json.load(f)
        if jutsu_name not in stats:
            stats[jutsu_name] = {"success": 0, "failures": 0, "times": [], "mastery": "Unranked"}
        if success:
            stats[jutsu_name]["success"] += 1
            if completion_time:
                stats[jutsu_name]["times"].append(completion_time)
        else:
            stats[jutsu_name]["failures"] += 1

        success_count = stats[jutsu_name]["success"]
        if success_count >= MASTER_LEVELS["Master"]:
            stats[jutsu_name]["mastery"] = "Master"
        elif success_count >= MASTER_LEVELS["Intermediate"]:
            stats[jutsu_name]["mastery"] = "Intermediate"
        elif success_count >= MASTER_LEVELS["Novice"]:
            stats[jutsu_name]["mastery"] = "Novice"

        f.seek(0)
        json.dump(stats, f, indent=4)
        f.truncate()

# --- Main Camera Streaming ---
def gen_frames():
    global phase, mode, selected_jutsu, selection_start_time, last_selected_box
    global user_sequence, expected_sequence, last_detected_label, label_start_time
    global pause_start_time, result_message, result_color, start_time, elapsed_time
    global JUTSU_BOXES, time_attack_start, time_attack_completed, gestures_done

    cap = cv2.VideoCapture(CAM_ID)
    if not cap.isOpened():
        raise RuntimeError("❌ Cannot open camera.")

    while True:
        success, frame = cap.read()
        if not success:
            break

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        current_time = time.time()

        if phase == "menu":
            continue

        if phase == "paused":
            elapsed = current_time - pause_start_time
            font_scale = min(2.0, 1.0 + 0.1 * (elapsed * 2))

            text_size = cv2.getTextSize(result_message, cv2.FONT_HERSHEY_DUPLEX, font_scale, 2)[0]
            text_x = (frame.shape[1] - text_size[0]) // 2
            text_y = (frame.shape[0] + text_size[1]) // 2

            cv2.putText(frame, result_message, (text_x, text_y),
                        cv2.FONT_HERSHEY_DUPLEX, font_scale, result_color, 3)

            if elapsed_time is not None and mode != "time_attack":
                timer_text = f"Time: {elapsed_time:.2f} sec"
                cv2.putText(frame, timer_text, (text_x, text_y + 60),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 0), 3)

            if elapsed > 2.5:
                phase = "selecting" if mode in ["learn", "mastery"] else "free"

        elif phase == "selecting":
            x = 30
            y = 30
            for jutsu in JUTSU_HAND_SIGNS.keys():
                JUTSU_BOXES[jutsu] = (x, y, x + BOX_WIDTH, y + BOX_HEIGHT)
                y += BOX_HEIGHT + GAP

                # Draw box and label
                cv2.rectangle(frame, (JUTSU_BOXES[jutsu][0], JUTSU_BOXES[jutsu][1]),
                              (JUTSU_BOXES[jutsu][2], JUTSU_BOXES[jutsu][3]),
                              (255, 0, 0), 2)
                cv2.putText(frame, jutsu, (JUTSU_BOXES[jutsu][0] + 5, JUTSU_BOXES[jutsu][1] + 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)

            results = hands.process(frame_rgb)
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    x_list = [lm.x for lm in hand_landmarks.landmark]
                    y_list = [lm.y for lm in hand_landmarks.landmark]
                    cx = int(sum(x_list) / len(x_list) * frame.shape[1])
                    cy = int(sum(y_list) / len(y_list) * frame.shape[0])

                    cv2.circle(frame, (cx, cy), 10, (255, 100, 0), -1)

                    for jutsu_name, box in JUTSU_BOXES.items():
                        if inside_box(cx, cy, box):
                            if last_selected_box != jutsu_name:
                                last_selected_box = jutsu_name
                                selection_start_time = current_time
                            else:
                                if (current_time - selection_start_time) >= SELECTION_HOLD_TIME:
                                    selected_jutsu = jutsu_name
                                    expected_sequence = JUTSU_HAND_SIGNS[selected_jutsu].copy()
                                    phase = "performing"
                                    user_sequence.clear()
                                    start_time = current_time
                                    selection_start_time = current_time + 100

        elif phase in ["free", "performing"]:
            result = model.predict(
                source=frame,
                imgsz=IMG_SIZE,
                conf=CONF_THRES,
                device=device,
                verbose=False
            )[0]

            if result.boxes is not None:
                for xyxy, cls in zip(result.boxes.xyxy, result.boxes.cls):
                    x1, y1, x2, y2 = map(int, xyxy)
                    label = model.names[int(cls)]

                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(frame, label, (x1, y1-10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

                    if phase == "free":
                        save_gesture_to_json(label)

                    if phase == "performing":
                        if label != last_detected_label:
                            last_detected_label = label
                            label_start_time = current_time
                        else:
                            if (current_time - label_start_time) >= GESTURE_HOLD_TIME:
                                if not user_sequence or user_sequence[-1] != label:
                                    user_sequence.append(label)
                                    last_detected_label = None
                                    detected_gestures.append((label, current_time))
                                    save_gesture_to_json(label)

                                if selected_jutsu:
                                    if mode == "time_attack":
                                        gestures_done += 1
                                        selected_jutsu = random.choice(list(JUTSU_HAND_SIGNS.keys()))
                                        expected_sequence = JUTSU_HAND_SIGNS[selected_jutsu].copy()
                                        user_sequence.clear()
                                        start_time = time.time()
                                    elif len(user_sequence) >= len(expected_sequence):
                                        correct = match_sequence(user_sequence, expected_sequence)
                                        result_message = "🎉 CONGRATULATIONS!" if correct else "❌ WRONG!"
                                        result_color = (0, 255, 0) if correct else (0, 0, 255)
                                        phase = "paused"
                                        pause_start_time = current_time
                                        elapsed_time = current_time - start_time
                                        if mode in ["learn", "mastery"]:
                                            update_stats(selected_jutsu, correct, elapsed_time)

        # Draw Detected Gestures Bottom Left
        y_offset = frame.shape[0] - 20
        for gesture, ts in list(detected_gestures):
            if current_time - ts <= gesture_display_time:
                cv2.putText(frame, f"{gesture}", (10, y_offset),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
                y_offset -= 30

        # Draw Required Signs Top Right
        if mode in ["learn", "mastery"] and phase == "performing" and expected_sequence:
            y_offset = 30
            for idx, sign in enumerate(expected_sequence):
                cv2.putText(frame, f"{idx+1}: {sign}", (frame.shape[1]-300, y_offset),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
                y_offset += 30

        # Draw Time Attack Stats
        if mode == "time_attack" and time_attack_start:
            remaining = max(0, TIME_ATTACK_DURATION - (current_time - time_attack_start))
            timer_text = f"Time Left: {remaining:.1f}s | Gestures Done: {gestures_done}"
            cv2.putText(frame, timer_text, (20, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)

        ret, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

    cap.release()

# --- Flask Routes ---

@app.route('/')
def index():
    if mode is None or phase == "menu":
        return redirect(url_for('menu'))
    return render_template('index.html')

@app.route('/menu')
def menu():
    return render_template('menu.html')

@app.route('/set_mode/<new_mode>', methods=['POST'])
def set_mode(new_mode):
    global mode, phase, selected_jutsu, time_attack_start, time_attack_completed, expected_sequence, gestures_done
    mode = new_mode
    if mode == "learn":
        phase = "selecting"
    elif mode == "mastery":
        phase = "selecting"
    elif mode == "free":
        phase = "free"
    elif mode == "time_attack":
        phase = "performing"
        time_attack_start = time.time()
        time_attack_completed = 0
        gestures_done = 0  # Reset gesture counter
        selected_jutsu = random.choice(list(JUTSU_HAND_SIGNS.keys()))
        expected_sequence = JUTSU_HAND_SIGNS[selected_jutsu].copy()
    return "Mode set", 200

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/reset', methods=['POST'])
def reset_sequence():
    global phase, mode, selected_jutsu, user_sequence, expected_sequence
    mode = None
    phase = "menu"
    selected_jutsu = None
    expected_sequence = []
    user_sequence.clear()
    return "Reset done", 200

@app.route('/stats')
def stats():
    if not os.path.exists(STATS_FILE):
        return "No stats available yet."
    with open(STATS_FILE) as f:
        stats_data = json.load(f)
    return render_template('stats.html', stats=stats_data)

if __name__ == '__main__':
    # clean_gestures_json()
    app.run(host='0.0.0.0', port=5000, debug=True)

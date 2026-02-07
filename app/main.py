import streamlit as st
import cv2
import time
from datetime import datetime

# ---------- LOCAL IMPORTS ----------
from emotion_face import EmotionDetector
from emotion_text import detect_text_emotion
from emotion_voice import detect_voice_emotion
from emotion_fusion import fuse_emotions
from stress_monitor import StressMonitor
from task_mapper import map_task
from employee import generate_employee_id
from hr_alert import notify_hr

# ---------- STREAMLIT CONFIG ----------
st.set_page_config(
    page_title="Amdox AI Task Optimizer",
    layout="wide"
)

st.title("Amdox AI – Employee Emotion Intelligence System")

# ---------- SESSION STATE ----------
if "run" not in st.session_state:
    st.session_state.run = False
if "emotion" not in st.session_state:
    st.session_state.emotion = "Neutral"
if "confidence" not in st.session_state:
    st.session_state.confidence = 0.5
if "task" not in st.session_state:
    st.session_state.task = "Routine work"

# ---------- SIDEBAR ----------
st.sidebar.header(" Controls")

if st.sidebar.button("▶ Start Camera"):
    st.session_state.run = True

if st.sidebar.button("⏹ Stop Camera"):
    st.session_state.run = False

st.sidebar.divider()

# ---------- TEXT INPUT ----------
st.sidebar.subheader(" Text Emotion Input")
text_input = st.sidebar.text_area(
    "Employee feedback",
    placeholder="Example: I am feeling very stressed and tired today..."
)
send_text = st.sidebar.button("Analyze Text")

st.sidebar.divider()

# ---------- VOICE INPUT ----------
st.sidebar.subheader("🎙 Voice Emotion Test")
record_voice = st.sidebar.button("Record Voice")

# ---------- OBJECTS ----------
face_detector = EmotionDetector()

if "stress_monitor" not in st.session_state:
    st.session_state.stress_monitor = StressMonitor()

stress_monitor = st.session_state.stress_monitor

# ---------- UI ----------
col1, col2, col3 = st.columns([3, 2, 2])

with col1:
    st.subheader("📷 Live Camera")
    cam_box = st.empty()

with col2:
    st.subheader("😐 Detected Emotion")
    emotion_box = st.empty()

with col3:
    st.subheader("📋 AI Suggested Task")
    task_box = st.empty()

status = st.empty()

# ====================================================
# 📝 TEXT MODE
# ====================================================
if send_text and text_input.strip():
    emp_id = generate_employee_id()   # ✅ FIX

    emotion, confidence = detect_text_emotion(text_input)

    st.session_state.emotion = emotion
    st.session_state.confidence = confidence
    st.session_state.task = map_task(emotion)

    emotion_box.metric("Emotion", emotion, f"{int(confidence*100)}%")
    task_box.success(st.session_state.task)

    if stress_monitor.update(emotion, confidence):
        notify_hr(emp_id, emotion, confidence, source="TEXT")
        st.error("🚨 HR notified due to TEXT stress")

    with open("data/team_mood.csv", "a") as f:
        f.write(f"{emp_id},TEXT,{emotion},{confidence},{datetime.now()}\n")

# ====================================================
# 🎙 VOICE MODE
# ====================================================
if record_voice:
    emp_id = generate_employee_id()   # ✅ FIX

    with st.spinner("🎙 Listening..."):
        voice_emotion, voice_conf = detect_voice_emotion()

    st.session_state.emotion = voice_emotion
    st.session_state.confidence = voice_conf
    st.session_state.task = map_task(voice_emotion)

    emotion_box.metric("Emotion", voice_emotion, f"{int(voice_conf*100)}%")
    task_box.success(st.session_state.task)

    if stress_monitor.update(voice_emotion, voice_conf):
        notify_hr(emp_id, voice_emotion, voice_conf, source="VOICE")
        st.error("🚨 HR notified due to VOICE stress")

    with open("data/team_mood.csv", "a") as f:
        f.write(f"{emp_id},VOICE,{voice_emotion},{voice_conf},{datetime.now()}\n")

# ====================================================
# 📷 CAMERA MODE (FACE)
# ====================================================
cap = cv2.VideoCapture(0)
frame_count = 0

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

while st.session_state.run:
    ret, frame = cap.read()
    if not ret:
        status.error("❌ Camera not accessible")
        break

    frame_count += 1

    if frame_count % 5 == 0:
        emp_id = generate_employee_id()   # ✅ FIX

        face_emotion, face_conf = face_detector.detect(frame)

        st.session_state.emotion = face_emotion
        st.session_state.confidence = face_conf
        st.session_state.task = map_task(face_emotion)

        if stress_monitor.update(face_emotion, face_conf):
            notify_hr(emp_id, face_emotion, face_conf, source="FACE")
            st.error("🚨 HR notified due to FACE stress")

        with open("data/team_mood.csv", "a") as f:
            f.write(f"{emp_id},FACE,{face_emotion},{face_conf},{datetime.now()}\n")

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(
            frame,
            f"{st.session_state.emotion} ({int(st.session_state.confidence*100)}%)",
            (x, y - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2
        )

    cam_box.image(frame, channels="BGR", use_column_width=True)
    emotion_box.metric(
        "Emotion",
        st.session_state.emotion,
        f"{int(st.session_state.confidence*100)}%"
    )
    task_box.success(st.session_state.task)

    time.sleep(0.03)

cap.release()
status.info("⏹ Camera stopped")

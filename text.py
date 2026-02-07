import streamlit as st
import cv2
import time
from datetime import datetime

# -------- LOCAL IMPORTS (APP FOLDER KE ANDAR) --------
from emotion_face import EmotionDetector
from stress_monitor import StressMonitor
from emotion_text import detect_text_emotion
from privacy import anonymize_user
from auth import login, register
from hr_alert import notify_hr
from task_mapper import map_task

# -------- STREAMLIT CONFIG --------
st.set_page_config(page_title="Amdox AI Task Optimizer", layout="wide")
st.title("🎥 Amdox AI – Employee Emotion Intelligence System")

# -------- AUTH --------
if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    st.subheader("🔐 Login / Register")

    u = st.text_input("Username")
    p = st.text_input("Password", type="password")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Login"):
            if login(u, p):
                st.session_state.auth = True
                st.session_state.user = anonymize_user(u)
                st.experimental_rerun()
            else:
                st.error("Invalid credentials")

    with col2:
        if st.button("Register"):
            register(u, p)
            st.success("Registered successfully")

    st.stop()

# -------- SESSION STATE --------
if "run" not in st.session_state:
    st.session_state.run = False

if "emotion" not in st.session_state:
    st.session_state.emotion = "Neutral"

if "task" not in st.session_state:
    st.session_state.task = "Routine work"

# -------- SIDEBAR --------
st.sidebar.header("Controls")

if st.sidebar.button("▶ Start Camera"):
    st.session_state.run = True

if st.sidebar.button("⏹ Stop Camera"):
    st.session_state.run = False

st.sidebar.subheader("📝 Text Emotion Input")
text_input = st.sidebar.text_area("Employee feedback")

# -------- OBJECTS --------
detector = EmotionDetector()
stress = StressMonitor()

# -------- UI GRID --------
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

# -------- CAMERA --------
cap = cv2.VideoCapture(0)
frame_count = 0

while st.session_state.run:
    ret, frame = cap.read()
    if not ret:
        status.error("Camera not accessible")
        break

    frame_count += 1

    # -------- EMOTION FUSION --------
    if frame_count % 5 == 0:
        face_emotion = detector.detect(frame)

        if text_input.strip():
            final_emotion = detect_text_emotion(text_input)
        else:
            final_emotion = face_emotion

        st.session_state.emotion = final_emotion
        st.session_state.task = map_task(final_emotion)

        # -------- STRESS + HR ALERT --------
        if stress.update(final_emotion):
            notify_hr(st.session_state.user)
            st.warning("⚠ High stress detected. HR notified.")

        # -------- LOG TEAM MOOD --------
        with open("../data/team_mood.csv", "a") as f:
            f.write(f"{st.session_state.user},{final_emotion},{datetime.now()}\n")

    cam_box.image(frame, channels="BGR", use_column_width=True)
    emotion_box.metric("Emotion", st.session_state.emotion)
    task_box.success(st.session_state.task)

    time.sleep(0.03)

cap.release()
status.info("Camera stopped")







import smtplib
from email.message import EmailMessage
from datetime import datetime

HR_EMAIL = "abhipatna989@gmail.com"
SENDER_EMAIL = "abcom099786@gmail.com"
APP_PASSWORD = "................"

# "YOUR_16_DIGIT_APP_PASSWORD"

def notify_hr(emp, emotion, conf):
    msg = EmailMessage()
    msg["Subject"] = f"⚠ Prolonged Stress Alert – {emp}"
    msg["From"] = SENDER_EMAIL
    msg["To"] = HR_EMAIL

    msg.set_content(f"""
Employee: {emp}
Emotion: {emotion}
Confidence: {conf*100:.1f}%
Time: {datetime.now()}

Recommendation:
• HR check-in
• Workload review
• Mental health support
""")

    with smtplib.SMTP_SSL("smtp.gmail.com",465) as s:
        s.login(SENDER_EMAIL, APP_PASSWORD)
        s.send_message(msg)

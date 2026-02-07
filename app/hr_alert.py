import smtplib
import ssl
from email.message import EmailMessage
from datetime import datetime

# 🔐 EMAIL CONFIG
EMAIL = "yourgmail@gmail.com"              # sender
APP_PASSWORD = "your_16_digit_app_password" # generated from Google Account settings
RECEIVER = "hrdepartment@gmail.com"        # HR email


def notify_hr(emp, emotion, conf, source):
    """
    emp     : Random Employee ID
    emotion : Stress / Sad / Angry / Fear
    conf    : Confidence (0–1)
    source  : TEXT / FACE / VOICE / FUSION
    """

    msg = EmailMessage()
    msg["From"] = EMAIL
    msg["To"] = RECEIVER
    msg["Subject"] = f"🚨 EMPLOYEE STRESS ALERT | {emp}"

    msg.set_content(f"""
ALERT: EMPLOYEE STRESS DETECTED

Employee ID : {emp}
Source      : {source}
Emotion     : {emotion}
Confidence  : {conf*100:.1f} %
Time        : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Action Required:
• Immediate HR check-in with employee
• Review current workload and deadlines
• Identify stress triggers and pressure points
• Provide mental health / wellness support
• Monitor employee condition for next 7 days
• Escalate to senior HR if stress persists

— Amdox AI Emotion Intelligence System
""")

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(EMAIL, APP_PASSWORD)
        server.send_message(msg)

    print("✅ HR EMAIL SENT")

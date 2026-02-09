# from datetime import datetime

# def notify_hr(employee_id):
#     with open("data/stress_logs.csv", "a") as f:
#         f.write(f"{employee_id},STRESS_ALERT,{datetime.now()}\n")

#     print(f"[HR ALERT] Employee {employee_id} flagged for prolonged stress")


import smtplib
from email.message import EmailMessage
from datetime import datetime

HR_EMAIL = "..........................."
SENDER_EMAIL = "........................"
APP_PASSWORD = "........................"   
# "YOUR_16_DIGIT_APP_PASSWORD" 

def notify_hr(employee_id, emotion, confidence):
    msg = EmailMessage()
    msg["Subject"] = f"⚠ Stress Alert – Employee {employee_id}"
    msg["From"] = SENDER_EMAIL
    msg["To"] = HR_EMAIL

    msg.set_content(f"""
    Employee ID: {employee_id}
    Detected Emotion: {emotion}
    Confidence: {confidence*100:.1f}%
    Time: {datetime.now()}

    Recommendation:
    - HR check-in
    - Workload adjustment
    """)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(SENDER_EMAIL, APP_PASSWORD)
        server.send_message(msg)

    print("✅ HR Email Sent")

import smtplib
from typing import Dict
from email.message import EmailMessage


def send_anomaly_email(sender_email: str, password: str, to_email: str, anomaly: Dict):
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    subject = "🚨 Log Anomaly Detected"
    body = f"""
🚨 Anomaly Detected in System Logs
timestamp   : {anomaly['timestamp']}
error Count : {anomaly['error_count']}
z-Score     : {round(anomaly['z_score'], 2)}
Please investigate immediately.
Regards,
Log Monitoring System
"""
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = to_email
    msg.set_content(body)

    try:
        print("Connecting to SMTP server...")
        server = smtplib.SMTP(smtp_server, smtp_port)

        print("Starting secure connection...")
        server.starttls()

        print("Logging in...")
        server.login(sender_email, password)

        print("Sending email...")
        server.send_message(msg)

        print("Email sent successfully!")

        server.quit()

    except Exception as e:
        print("Error:", e)
        


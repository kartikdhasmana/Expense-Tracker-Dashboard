# Email utility for sending OTP
import smtplib
import random
import string
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv()

# Email configuration - Set these in your .env file
SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
FROM_EMAIL = os.getenv("FROM_EMAIL", SMTP_USER)

def generate_otp(length: int = 6) -> str:
    """Generate a random 6-digit OTP"""
    return ''.join(random.choices(string.digits, k=length))

def send_otp_email(to_email: str, otp: str) -> bool:
    """Send OTP to the specified email address"""
    try:
        # Create message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = 'Your Expense Tracker Verification Code'
        msg['From'] = FROM_EMAIL
        msg['To'] = to_email

        # Plain text version
        text = f"""
Your Expense Tracker Verification Code

Your OTP is: {otp}

This code will expire in 10 minutes.

If you didn't request this code, please ignore this email.
        """

        # HTML version
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: 'Segoe UI', Arial, sans-serif; background-color: #f5f5f5; margin: 0; padding: 20px; }}
        .container {{ max-width: 500px; margin: 0 auto; background: white; border-radius: 16px; padding: 40px; box-shadow: 0 4px 20px rgba(0,0,0,0.1); }}
        .header {{ text-align: center; margin-bottom: 30px; }}
        .logo {{ font-size: 48px; margin-bottom: 10px; }}
        h1 {{ color: #333; margin: 0; font-size: 24px; }}
        .otp-box {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; font-size: 36px; font-weight: bold; letter-spacing: 8px; text-align: center; padding: 20px; border-radius: 12px; margin: 30px 0; }}
        .message {{ color: #666; text-align: center; font-size: 14px; line-height: 1.6; }}
        .footer {{ margin-top: 30px; text-align: center; color: #999; font-size: 12px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="logo">💰</div>
            <h1>Expense Tracker</h1>
        </div>
        <p class="message">Use the following code to verify your email address:</p>
        <div class="otp-box">{otp}</div>
        <p class="message">This code will expire in <strong>10 minutes</strong>.</p>
        <p class="message">If you didn't request this code, you can safely ignore this email.</p>
        <div class="footer">
            &copy; 2025 Expense Tracker. All rights reserved.
        </div>
    </div>
</body>
</html>
        """

        part1 = MIMEText(text, 'plain')
        part2 = MIMEText(html, 'html')
        msg.attach(part1)
        msg.attach(part2)

        # Send email
        if not SMTP_USER or not SMTP_PASSWORD:
            # If no SMTP credentials, just print to console (for development)
            print(f"\n{'='*50}")
            print(f"📧 OTP Email (Development Mode)")
            print(f"{'='*50}")
            print(f"To: {to_email}")
            print(f"OTP: {otp}")
            print(f"{'='*50}\n")
            return True

        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.sendmail(FROM_EMAIL, to_email, msg.as_string())
        
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

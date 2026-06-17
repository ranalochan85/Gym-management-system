"""Email utility functions."""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.config import settings
from typing import List


def send_email(
    recipient: str,
    subject: str,
    body: str,
    html_body: str = None,
    cc: List[str] = None,
    bcc: List[str] = None
) -> bool:
    """Send email."""
    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = settings.SMTP_FROM_EMAIL
        msg["To"] = recipient
        
        if cc:
            msg["Cc"] = ", ".join(cc)
        if bcc:
            msg["Bcc"] = ", ".join(bcc)
        
        # Attach plain text
        msg.attach(MIMEText(body, "plain"))
        
        # Attach HTML if provided
        if html_body:
            msg.attach(MIMEText(html_body, "html"))
        
        # Send email
        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            server.starttls()
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            server.send_message(msg)
        
        return True
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return False


def send_welcome_email(email: str, full_name: str) -> bool:
    """Send welcome email to new user."""
    subject = "Welcome to Gym Management System"
    body = f"""Hello {full_name},

Welcome to our gym! We're excited to have you as a member.

Best regards,
Gym Management Team
"""
    
    return send_email(email, subject, body)


def send_membership_reminder(email: str, member_name: str, expiry_date: str) -> bool:
    """Send membership expiry reminder."""
    subject = "Membership Expiry Reminder"
    body = f"""Hello {member_name},

Your membership will expire on {expiry_date}.

Please renew your membership to continue enjoying our facilities.

Best regards,
Gym Management Team
"""
    
    return send_email(email, subject, body)

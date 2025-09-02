"""
Email service for sending verification codes.
"""
import asyncio
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional
import config


def generate_verification_code() -> str:
    """Generate a random 6-digit verification code."""
    return ''.join([str(random.randint(0, 9)) for _ in range(config.VERIFICATION_CODE_LENGTH)])


def create_verification_email(recipient_email: str, verification_code: str, name: str, event_name: str) -> MIMEMultipart:
    """Create the verification email message."""
    message = MIMEMultipart("alternative")
    message["Subject"] = f"Verify Your Registration for {event_name}"
    message["From"] = config.FROM_EMAIL
    message["To"] = recipient_email
    
    # Create the HTML content
    html = f"""
    <html>
      <body>
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
          <h2 style="color: #333;">Event Registration Verification</h2>
          <p>Hi {name},</p>
          <p>Thank you for registering for <strong>{event_name}</strong>!</p>
          <p>To complete your registration, please use the verification code below:</p>
          <div style="background-color: #f0f0f0; padding: 20px; margin: 20px 0; text-align: center; border-radius: 5px;">
            <h1 style="color: #007bff; margin: 0; font-size: 36px; letter-spacing: 5px;">{verification_code}</h1>
          </div>
          <p>This code will expire in {config.VERIFICATION_CODE_EXPIRY_MINUTES} minutes.</p>
          <p>If you didn't request this registration, please ignore this email.</p>
          <hr style="margin: 30px 0;">
          <p style="color: #666; font-size: 12px;">
            This is an automated message from the Event Registration System.
          </p>
        </div>
      </body>
    </html>
    """
    
    # Create the plain-text content
    text = f"""
    Event Registration Verification
    
    Hi {name},
    
    Thank you for registering for {event_name}!
    
    To complete your registration, please use the verification code below:
    
    {verification_code}
    
    This code will expire in {config.VERIFICATION_CODE_EXPIRY_MINUTES} minutes.
    
    If you didn't request this registration, please ignore this email.
    
    ---
    This is an automated message from the Event Registration System.
    """
    
    # Add text and HTML parts to message
    text_part = MIMEText(text, "plain")
    html_part = MIMEText(html, "html")
    
    message.attach(text_part)
    message.attach(html_part)
    
    return message


async def send_verification_email(recipient_email: str, verification_code: str, name: str, event_name: str) -> bool:
    """
    Send verification email to the recipient.
    
    Returns True if email was sent successfully, False otherwise.
    Note: This is a simplified implementation for demonstration purposes.
    In production, you would use a proper email service like SendGrid, AWS SES, etc.
    """
    try:
        # For demonstration purposes, we'll just print the email content
        # In a real application, you would configure SMTP settings and send the email
        
        print(f"\n=== EMAIL SIMULATION ===")
        print(f"To: {recipient_email}")
        print(f"Subject: Verify Your Registration for {event_name}")
        print(f"Verification Code: {verification_code}")
        print(f"Recipient: {name}")
        print(f"======================\n")
        
        # Simulate email sending delay
        await asyncio.sleep(0.1)
        
        # For now, always return True (successful)
        # In production, implement actual SMTP sending:
        """
        message = create_verification_email(recipient_email, verification_code, name, event_name)
        
        with smtplib.SMTP(config.SMTP_SERVER, config.SMTP_PORT) as server:
            server.starttls()
            server.login(config.SMTP_USERNAME, config.SMTP_PASSWORD)
            server.send_message(message)
        """
        
        return True
        
    except Exception as e:
        print(f"Error sending email: {e}")
        return False


# For production use, uncomment and configure this function:
"""
async def send_verification_email_smtp(recipient_email: str, verification_code: str, name: str, event_name: str) -> bool:
    '''Send verification email using SMTP.'''
    try:
        message = create_verification_email(recipient_email, verification_code, name, event_name)
        
        with smtplib.SMTP(config.SMTP_SERVER, config.SMTP_PORT) as server:
            server.starttls()
            server.login(config.SMTP_USERNAME, config.SMTP_PASSWORD)
            server.send_message(message)
        
        return True
    except Exception as e:
        print(f"Error sending email via SMTP: {e}")
        return False
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional
import os

# Email configuration - update these with your SMTP settings
SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER", "your-email@gmail.com")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "your-app-password")
FROM_EMAIL = os.getenv("FROM_EMAIL", "noreply@eventsync.com")


def send_teacher_credentials_email(
    to_email: str,
    teacher_name: str,
    teacher_id: str,
    password: str,
    login_url: str = "http://localhost:8000/auth/login"
) -> bool:
    """
    Send login credentials to newly created teacher via email.
    
    Args:
        to_email: Teacher's email address
        teacher_name: Teacher's full name
        teacher_id: Generated teacher ID for login
        password: Generated password
        login_url: URL for login page
    
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    
    # Create email content
    subject = "Welcome to EventSync - Your Login Credentials"
    
    html_body = f"""
    <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background-color: #4CAF50; color: white; padding: 20px; text-align: center; }}
                .content {{ background-color: #f9f9f9; padding: 30px; border-radius: 5px; margin-top: 20px; }}
                .credentials {{ background-color: #fff; padding: 15px; border-left: 4px solid #4CAF50; margin: 20px 0; }}
                .credential-item {{ margin: 10px 0; }}
                .label {{ font-weight: bold; color: #555; }}
                .value {{ color: #000; font-family: monospace; background-color: #f0f0f0; padding: 5px 10px; border-radius: 3px; }}
                .button {{ display: inline-block; padding: 12px 30px; background-color: #4CAF50; color: white; text-decoration: none; border-radius: 5px; margin-top: 20px; }}
                .footer {{ text-align: center; margin-top: 30px; color: #777; font-size: 12px; }}
                .warning {{ color: #ff9800; font-weight: bold; margin-top: 15px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🎓 Welcome to EventSync</h1>
                </div>
                <div class="content">
                    <h2>Hello {teacher_name},</h2>
                    <p>Your teacher account has been successfully created by the administrator.</p>
                    <p>Below are your login credentials to access the EventSync platform:</p>
                    
                    <div class="credentials">
                        <div class="credential-item">
                            <span class="label">Teacher ID:</span>
                            <span class="value">{teacher_id}</span>
                        </div>
                        <div class="credential-item">
                            <span class="label">Password:</span>
                            <span class="value">{password}</span>
                        </div>
                        <div class="credential-item">
                            <span class="label">Email:</span>
                            <span class="value">{to_email}</span>
                        </div>
                    </div>
                    
                    <p class="warning">⚠️ Please change your password after your first login for security purposes.</p>
                    
                    <a href="{login_url}" class="button">Login Now</a>
                    
                    <p style="margin-top: 30px;">If you have any questions or need assistance, please contact the administrator.</p>
                </div>
                <div class="footer">
                    <p>This is an automated message from EventSync. Please do not reply to this email.</p>
                    <p>&copy; 2025 EventSync. All rights reserved.</p>
                </div>
            </div>
        </body>
    </html>
    """
    
    text_body = f"""
    Welcome to EventSync, {teacher_name}!
    
    Your teacher account has been successfully created.
    
    Login Credentials:
    ------------------
    Teacher ID: {teacher_id}
    Password: {password}
    Email: {to_email}
    
    Login URL: {login_url}
    
    ⚠️ IMPORTANT: Please change your password after your first login.
    
    If you have any questions, please contact the administrator.
    
    ---
    This is an automated message from EventSync.
    © 2025 EventSync. All rights reserved.
    """
    
    try:
        # Create message
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = FROM_EMAIL
        message["To"] = to_email
        
        # Attach both plain text and HTML versions
        part1 = MIMEText(text_body, "plain")
        part2 = MIMEText(html_body, "html")
        message.attach(part1)
        message.attach(part2)
        
        # Send email
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.send_message(message)
        
        print(f"✅ Credentials email sent successfully to {to_email}")
        return True
        
    except Exception as e:
        print(f"❌ Failed to send email to {to_email}: {str(e)}")
        return False


def send_test_email(to_email: str) -> bool:
    """Test email configuration by sending a test email."""
    try:
        message = MIMEText("This is a test email from EventSync.", "plain")
        message["Subject"] = "Test Email - EventSync"
        message["From"] = FROM_EMAIL
        message["To"] = to_email
        
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.send_message(message)
        
        print(f"✅ Test email sent successfully to {to_email}")
        return True
        
    except Exception as e:
        print(f"❌ Failed to send test email: {str(e)}")
        return False

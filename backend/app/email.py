"""Email service for sending RSVP confirmations."""
import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import date
from typing import List, Optional
from . import config

logger = logging.getLogger(__name__)


def format_date(event_date: date) -> str:
    """Format date for display in emails."""
    return event_date.strftime("%A, %d %B %Y")


def format_guest_list_html(guest_names: List[str]) -> str:
    """Format guest names as HTML list."""
    if len(guest_names) == 1:
        return f"<p><strong>Guest:</strong> {guest_names[0]}</p>"

    guests_html = "<p><strong>Guests:</strong></p><ul style=\"margin: 8px 0; padding-left: 20px;\">"
    for name in guest_names:
        guests_html += f"<li style=\"margin: 4px 0;\">{name}</li>"
    guests_html += "</ul>"
    return guests_html


def format_guest_list_text(guest_names: List[str]) -> str:
    """Format guest names as plain text list."""
    if len(guest_names) == 1:
        return f"Guest: {guest_names[0]}"

    guests_text = "Guests:\n"
    for name in guest_names:
        guests_text += f"  - {name}\n"
    return guests_text


def get_confirmation_email_html(
    guest_name: str,
    event_name: str,
    event_date: date,
    attending: bool,
    guest_names: Optional[List[str]] = None,
    guest_count: int = 1
) -> str:
    """Generate HTML email content for RSVP confirmation."""
    formatted_date = format_date(event_date)

    # Use guest_names if provided, otherwise just the primary guest
    all_guests = guest_names if guest_names else [guest_name]
    guest_list_html = format_guest_list_html(all_guests)

    if attending:
        party_text = f"{guest_count} guest{'s' if guest_count > 1 else ''}" if guest_count > 1 else "you"
        message = f"""
        <p>We're thrilled that {party_text} will be joining us for our <strong>{event_name}</strong>!</p>
        <p><strong>Date:</strong> {formatted_date}</p>
        {guest_list_html}
        <p>We can't wait to celebrate with you. More details will follow closer to the date.</p>
        """
        subject_status = "Confirmed"
    else:
        party_text = f"your party of {guest_count}" if guest_count > 1 else "you"
        message = f"""
        <p>We're sorry {party_text} won't be able to make it to our <strong>{event_name}</strong> on {formatted_date}.</p>
        {guest_list_html}
        <p>We'll miss having you there, but we understand. Thank you for letting us know!</p>
        """
        subject_status = "Received"

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
    </head>
    <body style="font-family: 'Georgia', serif; max-width: 600px; margin: 0 auto; padding: 20px; background-color: #f8fafc;">
        <div style="background-color: #ffffff; border-radius: 12px; padding: 40px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
            <div style="text-align: center; margin-bottom: 30px;">
                <h1 style="color: #4a7a9e; font-size: 28px; margin-bottom: 8px;">Isabella & Joshua</h1>
                <p style="color: #94a3b8; font-size: 14px; text-transform: uppercase; letter-spacing: 2px;">RSVP {subject_status}</p>
            </div>

            <div style="color: #334155; font-size: 16px; line-height: 1.6;">
                <p>Dear {guest_name},</p>
                <p>Thank you for responding to our invitation!</p>
                {message}
                <p>With love,<br>Isabella & Joshua</p>
            </div>

            <div style="margin-top: 40px; padding-top: 20px; border-top: 1px solid #e2e8f0; text-align: center;">
                <p style="color: #94a3b8; font-size: 12px;">
                    If you need to update your RSVP, simply submit the form again with the same email address.
                </p>
            </div>
        </div>
    </body>
    </html>
    """
    return html


def get_confirmation_email_text(
    guest_name: str,
    event_name: str,
    event_date: date,
    attending: bool,
    guest_names: Optional[List[str]] = None,
    guest_count: int = 1
) -> str:
    """Generate plain text email content for RSVP confirmation."""
    formatted_date = format_date(event_date)

    # Use guest_names if provided, otherwise just the primary guest
    all_guests = guest_names if guest_names else [guest_name]
    guest_list_text = format_guest_list_text(all_guests)

    if attending:
        party_text = f"{guest_count} guest{'s' if guest_count > 1 else ''}" if guest_count > 1 else "you"
        message = f"""We're thrilled that {party_text} will be joining us for our {event_name}!

Date: {formatted_date}

{guest_list_text}

We can't wait to celebrate with you. More details will follow closer to the date."""
    else:
        party_text = f"your party of {guest_count}" if guest_count > 1 else "you"
        message = f"""We're sorry {party_text} won't be able to make it to our {event_name} on {formatted_date}.

{guest_list_text}

We'll miss having you there, but we understand. Thank you for letting us know!"""

    text = f"""Dear {guest_name},

Thank you for responding to our invitation!

{message}

With love,
Isabella & Joshua

---
If you need to update your RSVP, simply submit the form again with the same email address.
"""
    return text


def send_rsvp_confirmation(
    to_email: str,
    guest_name: str,
    event_name: str,
    event_date: date,
    attending: bool,
    guest_names: Optional[List[str]] = None,
    guest_count: int = 1
) -> bool:
    """
    Send RSVP confirmation email.

    Returns True if email was sent successfully, False otherwise.
    """
    if not config.EMAIL_ENABLED:
        logger.info(f"Email disabled - would send confirmation to {to_email}")
        return True

    if not all([config.SMTP_HOST, config.SMTP_USER, config.SMTP_PASSWORD, config.SMTP_FROM_EMAIL]):
        logger.warning("Email configuration incomplete - skipping email send")
        return False

    try:
        # Create message
        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"RSVP Confirmation - {event_name}"
        msg["From"] = f"{config.SMTP_FROM_NAME} <{config.SMTP_FROM_EMAIL}>"
        msg["To"] = to_email

        # Create plain text and HTML versions
        text_content = get_confirmation_email_text(
            guest_name, event_name, event_date, attending, guest_names, guest_count
        )
        html_content = get_confirmation_email_html(
            guest_name, event_name, event_date, attending, guest_names, guest_count
        )

        msg.attach(MIMEText(text_content, "plain"))
        msg.attach(MIMEText(html_content, "html"))

        # Send email
        with smtplib.SMTP(config.SMTP_HOST, config.SMTP_PORT) as server:
            server.starttls()
            server.login(config.SMTP_USER, config.SMTP_PASSWORD)
            server.send_message(msg)

        logger.info(f"RSVP confirmation email sent to {to_email}")
        return True

    except smtplib.SMTPException as e:
        logger.error(f"Failed to send email to {to_email}: {e}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error sending email to {to_email}: {e}")
        return False

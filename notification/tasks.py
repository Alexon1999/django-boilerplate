from celery import shared_task

from django.core.mail import send_mail
import environ
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr, make_msgid, formatdate
from notification import services
import smtplib
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

env = environ.Env()


@shared_task
def send_multiple_mails(subject, html_content, mail_receipts):
    def getSMPTConfig():
        return env("smtp_server"), env("smtp_port"), env("username"), env("password")

    def send_one_mail(email, *args):
        msg = MIMEMultipart()
        msg["From"] = formataddr(("DAP", username))
        msg["To"] = email
        msg["Subject"] = Header(subject, "utf-8")
        msg["Message-ID"] = make_msgid(domain="dap.hieraug.fr")
        # Adding the Date header, this is a required header
        msg["Date"] = formatdate(localtime=True)
        # Render the email template with the necessary context data
        msg.attach(MIMEText(html_content, "html", "utf-8"))

        # Send the email via SMTP
        with smtplib.SMTP(smtp_server.strip(), int(smtp_port)) as server:
            server.starttls()  # Comment out if using SSL (port 465)
            server.login(username.strip(), password.strip())
            text = msg.as_string()
            server.sendmail(username, email, text)
            print("Email sent successfully!")

    try:
        smtp_server, smtp_port, username, password = getSMPTConfig()
        smtp_config = {
            "smtp_server": smtp_server,
            "smtp_port": smtp_port,
            "username": username,
            "password": password,
        }

        for mail in mail_receipts:
            send_one_mail(mail, smtp_config)

    except Exception as e:
        print(f"Error: {e}")


@shared_task
def send_mail_test(subject, html_content, mail_receipts):
    send_mail(
        subject=subject,
        message=html_content,
        recipient_list=mail_receipts,
        from_email=None,
        fail_silently=False,
    )


@shared_task
def send_user_notifications():
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "notifications_new_user",
        {
            "type": "number_of_notifications",
        },
    )

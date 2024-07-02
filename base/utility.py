import re
import threading

from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from rest_framework.exceptions import ValidationError
from decouple import config
from twilio.rest import Client

from users.models import VIA_EMAIL, VIA_PHONE

email_regex = re.compile(r'[^@ \t\r\n]+@[^@ \t\r\n]+\.[^@ \t\r\n]+')
phone_regex = re.compile(r'^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$')
username_regex = re.compile(r'^[a-z0-9_-]{3,15}$')


def check_email_or_phone_number(email_or_phone_number):
	if re.fullmatch(email_regex, email_or_phone_number):
		return "email"
	elif re.fullmatch(phone_regex, email_or_phone_number):
		return "phone_number"

	data = {
		"success": False,
		"message": "Email or phone number is not valid"
	}
	raise ValidationError(data)


def check_login_type(login_attempt):
	if re.fullmatch(email_regex, login_attempt):
		return 'email'
	elif re.fullmatch(phone_regex, login_attempt):
		return 'phone_number'
	elif re.fullmatch(username_regex, login_attempt):
		return 'username'
	raise ValidationError({'success': False, "message": "Email or phone number or username isn't valid"})


def check_passwords(password, reset_password):
	return password == reset_password


class EmailThread(threading.Thread):
	def __init__(self, email):
		self.email = email
		threading.Thread.__init__(self)

	def run(self):
		self.email.send()


class Email:
	@staticmethod
	def send_email(data):
		email = EmailMessage(
			subject=data["subject"],
			body=data["body"],
			to=[data['to_email']],

		)
		if data.get("content_type") == "html":
			email.content_subtype = "html"
			EmailThread(email).start()


def send_email(email, code):
	html_content = render_to_string(
		'authentication/activate_account.html',
		{"code": code}

	)
	Email.send_email(
		{
			"subject": "Royhatdan o'tish",
			"to_email": email,
			"body": html_content,
			"content_type": "html"

		}
	)


def send_phone(phone_number, code):
	account_sid = config('ACCOUNT_SID')
	auth_token = config("AUTH_TOKEN")
	client = Client(account_sid, auth_token)
	client.messages.create(
		body=f"Your verification code {code}",
		from_="+16184254756",
		to=f"{phone_number}"
	)

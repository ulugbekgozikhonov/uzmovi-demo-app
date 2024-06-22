import re

from rest_framework.exceptions import ValidationError
from decouple import config
from twilio.rest import Client

from users.models import VIA_EMAIL, VIA_PHONE

email_regex = re.compile(r'[^@ \t\r\n]+@[^@ \t\r\n]+\.[^@ \t\r\n]+')
phone_regex = re.compile(r'^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$')


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


def check_passwords(password, reset_password):
	return password == reset_password


def send_email(email, code):
	pass


def send_phone(phone_number, code):
	account_sid = config('ACCOUNT_SID')
	auth_token = config("AUTH_TOKEN")
	client = Client(account_sid, auth_token)
	client.messages.create(
		body=f"Your verification code {code}",
		from_="+16184254756",
		to=f"{phone_number}"
	)

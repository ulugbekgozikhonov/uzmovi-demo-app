from rest_framework import serializers

from users.models import User


class SignUpSerializer(serializers.ModelSerializer):
	id = serializers.UUIDField(read_only=True)
	auth_type = serializers.CharField(required=False)

	def __init__(self, *args, **kwargs):
		super(SignUpSerializer, self).__init__(*args, **kwargs)
		self.fields["email_or_phone_number"] = serializers.CharField(required=True)

	class Meta:
		model = User
		fields = (id, 'username', 'password', "auth_type")

		extra_kwargs = {
			"auth_type": {"required": False}
		}

	def validate(self, attrs):
		email_or_phone_number = attrs.get("email_or_phone_number")



from django.db import models
import uuid


class BaseModel(models.Model):
	id = models.UUIDField(editable=False, primary_key=True, default=uuid.uuid4)
	created_at = models.DateTimeField(auto_now_add=True)
	update_at = models.DateTimeField(auto_now=True)

	class Meta:
		abstract = True

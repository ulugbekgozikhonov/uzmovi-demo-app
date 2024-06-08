from django.db import models


# Create your models here.


class BaseModel(models.Model):
	id = models.UUIDField(unique=True, editable=False)
	created_at = models.DateTimeField(auto_now_add=True)
	update_at = models.DateTimeField(auto_now=True)

	class Meta:
		abstract = True

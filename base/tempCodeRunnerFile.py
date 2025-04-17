from django.db import models
import uuid

class BaseModel(models.Model):
    uid=models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)      #editable=false means adminbata developersharule field modeify garna namilne gari
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    class Meta:
        abstract=True     
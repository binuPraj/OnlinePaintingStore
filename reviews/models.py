from django.db import models
from django.contrib.auth.models import User
from base.models import BaseModel  # Assuming BaseModel is a custom model you're extending

class ContactMessage(BaseModel):
    # ForeignKey to User model for associating messages with a user
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="contact_messages")
    phone = models.CharField(max_length=15, blank=True, null=True)  # Phone number field
    message = models.TextField()  # Message content
    submitted_at = models.DateTimeField(auto_now_add=True)  # Timestamp for when the message is submitted

    def __str__(self):
        # Returns a string representation of the message (user's name and the first 50 characters of the message)
        return f"{self.user.first_name} {self.user.last_name}: {self.message[:50]}..."

    class Meta:
        # Optional: Define any meta options, such as ordering or verbose name
        ordering = ['-submitted_at']  # Order by the most recent submission first


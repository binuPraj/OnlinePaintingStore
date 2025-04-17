from django.contrib import admin
from .models import ContactMessage

class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'message', 'submitted_at']  # Display user and message in admin
    search_fields = ['user__first_name', 'user__last_name', 'user__email', 'message']  # Allow search by user's name, email, and message
    list_filter = ['submitted_at']  # Filter by submission date

admin.site.register(ContactMessage, ContactMessageAdmin)

from django.urls import path,include
from reviews import views

urlpatterns=[    
    path('contactus/',views.contactus,name='contactus'), 
    path('contact/',views.contact,name='contact'),
    path('aboutus/',views.aboutus,name="aboutus"),
    path('Feedback/',views.feedback,name="feedback"),
]
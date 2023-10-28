from django.urls import path
from . import views

urlpatterns = [

    path('register/', views.RegisterView.as_view()),
    path('sendMessages/', views.SendMessages.as_view(), name='send_messages'),
    
]


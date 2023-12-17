from django.urls import path
from . import views

urlpatterns = [

    path('register/', views.RegisterView.as_view()),

    path("myMessages/<user_id>/", views.MyInbox.as_view()),
    path("filterMessages/", views.filterMessages.as_view()),
    path("getMessages/<sender_id>/<reciever_id>/", views.GetMessages.as_view()),
    path('sendMessages/', views.SendMessages.as_view(), name='send_messages'),
    path('deleteMessages/<sender_id>/<reciever_id>/', views.DeleteMessages.as_view(), name='delete_messages'),
    path('view/', views.get_id_receiver.as_view(), name='id'),
    
]


from django.urls import path
from . import views

urlpatterns = [
    path("personal_chatbot", views.index),
    path("api/data", views.api_data)
]
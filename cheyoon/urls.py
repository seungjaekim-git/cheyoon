from django.urls import path
from cheyoon.views import HomeView

urlpatterns = [
    path('/<int:board_pk>',HomeView.as_view()),
]


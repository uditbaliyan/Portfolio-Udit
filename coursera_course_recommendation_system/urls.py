# recommend/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='coursera_course_recommendation_system'),
]

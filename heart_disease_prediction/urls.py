from django.urls import path
from . import views

urlpatterns = [
    path('', views.heart, name='heart'),
    path('predict_heart/', views.predict_heart, name='predict_heart'),
]

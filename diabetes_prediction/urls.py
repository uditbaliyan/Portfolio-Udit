from django.urls import path
from . import views

urlpatterns = [
    path('', views.diabetes, name='diabetes'),
    path('predict/', views.predict, name='predict'),
]

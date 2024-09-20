from django.urls import path
from . import views

urlpatterns = [
    path('predict/', views.predict, name='predict'),
    path('teams/', views.get_teams, name='get_teams'),
]




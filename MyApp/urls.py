from django.urls import path
from . import views

urlpatterns = [
    path('', views.python_ide_view, name='python_ide'),
]
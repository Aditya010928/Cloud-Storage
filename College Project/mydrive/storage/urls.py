from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('upload/', views.upload_file, name='upload'),
    path('decrypt/<int:file_id>/', views.decrypt_file, name='decrypt'),
]

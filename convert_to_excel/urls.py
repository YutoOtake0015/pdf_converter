from django.contrib import admin
from django.urls import path
from . import views

app_name = "convert_to_excel"

urlpatterns = [
    path('top/', views.top, name='top'),
    path('upload/', views.UploadView.as_view(), name='upload'),
    path('list/', views.ListView.as_view(), name='list'),
    path('del_file/', views.del_file, name='del_file'),
    path('', views.top)
]
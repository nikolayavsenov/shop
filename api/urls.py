from . import views
from django.urls import path, include

urlpatterns = [
    path('test/', views.PostList.as_view()),
]
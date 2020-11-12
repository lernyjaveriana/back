from django.urls import path
from user import views

urlpatterns = [
    path('user/<int:user_id>', views.UserManageGet.as_view()),
    path('user/', views.UserManagePost.as_view()),
    path('user/login/', views.ApiManager.as_view()),
]
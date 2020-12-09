from django.urls import path
from user import views

urlpatterns = [
    path('user/<int:user_id>', views.UserManageGet.as_view()),
    path('user/', views.UserManagePost.as_view()),
    path('user/login/', views.ApiManager.as_view()),
    path('user/pay/<str:tipoDocumento>/<str:numeroDocumento>', views.GetPayInformation.as_view()),
]
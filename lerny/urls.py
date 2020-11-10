from django.urls import path
from lerny import views

urlpatterns = [
    path('lerny/<int:cellphone_number>', views.LernyManageGet.as_view()),
    path('microlerny/<int:microlerny_id>', views.MicroLernyDadAndSon.as_view()),
]
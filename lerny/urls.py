from django.urls import path
from lerny import views

urlpatterns = [
    path('lerny/<int:cellphone_number>', views.LernyManageGet.as_view()),
    path('microlerny/<int:microlerny_id>', views.MicroLernyDadAndSon.as_view()),
    path('detail/', views.UserStateResource, name='detail'),
    path('apiresources/', views.ApiStateResource, name='apiresources'),
    path('editresource/', views.editStateResource, name='editresource'),
    path('lernydetail/', views.lernyDetail.as_view()),
    path('charts/', views.charts, name = 'charts'),
    path('lernyapi/', views.getLernyList, name = 'lernyapi'),
    path('microlernyapi/', views.getMicrolernyList, name = 'microlernyapi'),
]
from django.urls import path

from fractals import views

urlpatterns = [
    path('', views.ConfigurationList.as_view(), name='configuration-list'),
    path('add', views.ConfigurationCreate.as_view(), name='configuration-create'),
    path('<int:pk>', views.ConfigurationUpdate.as_view(), name='configuration-update'),
]

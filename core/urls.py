from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token

from . import views


urlpatterns = [



    path('manufacturers/', views.ManufacturerList.as_view(), name='manufacturer_list'),
    path('manufacturers/<str:pk>/', views.ManufacturerDetail.as_view()),

    path('modules/', views.ModuleList.as_view(), name='Module_list'),
    path('modules/<str:pk>/', views.ModuleDetail.as_view()),

    path('inverters/', views.InverterList.as_view(), name='Inverter_list'),
    path('inverters/<str:pk>/', views.InverterDetail.as_view()),

    path('batteries/', views.BatteryList.as_view(), name='Battery_list'),
    path('batteries/<str:pk>/', views.BatteryDetail.as_view()),

    path('submission/', views.FileUploadViewGenericProduct.as_view(), name="submission"),

    path('products/', views.ProductList.as_view(), name="products"),




    path('login/', obtain_auth_token, name='api-token-auth'),

]

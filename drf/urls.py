from django.urls import path, include
from . import views
from rest_framework import routers

routor = routers.DefaultRouter()
routor.register(r"api", views.AllProductsViewSet, basename='allproduct')
routor.register(r"product", views.ProductInventoryVievSet, basename='productinventory')


app_name = 'drf'

urlpatterns = [
    path('', include(routor.urls))
    # path('', views.productmodelall, name='productmodel'),
    # path('<int:pk>/', views.productmodeldetail, name='productdetail'),
]



from django.urls import path
from . import views


app_name = 'demo'

urlpatterns = [
    path('', views.home, name='home'),
    path('category/', views.category, name='category'),
    path('product_by_category/<slug:category>/', views.product_by_category, name='product_by_category'),
    path('<str:slug>/', views.product_detail, name='product_detail'),
]



from django.contrib import admin
from django.urls import path, include
from search.views import SearchProductInventory

urlpatterns = [
    path('admin/', admin.site.urls),
    path('demo/', include('demo.urls', namespace='demo')),
    path('', include('drf.urls', namespace='drf')),
    path('search/<str:query>/', SearchProductInventory.as_view()),
    path('ninja/', include('dninja.urls')),
]

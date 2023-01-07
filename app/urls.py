from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('classify/', views.welcome),
    path('nearstAddress/',views.getNearestAddress)
]

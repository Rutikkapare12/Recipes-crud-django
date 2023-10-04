from django.contrib import admin
from django.urls import path
from base import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.receipes, name="receipe" ),
    path('delete-receipe/<id>/', views.delete_receipe, name="delete_receipe"),
    path('update-receipe/<id>/', views.update_receipe, name="update_receipe")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
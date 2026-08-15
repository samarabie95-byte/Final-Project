from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.admin_url if hasattr(admin, 'admin_url') else admin.site.urls), # أو مسار الأذمن العادي بتاعك
    path('', include('tasks.urls')),
]
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # normal site
    path('', include('store.urls')),

    # API
    path('api/', include('store.urls')),
]

from django.contrib import admin
from django.urls import path, include
from rest_framework.documentation import include_docs_urls
from django.urls import path, re_path
from rest_framework import permissions

urlpatterns = [
    path('', include('acc_auth.urls')),
    path('accounts/', include('allauth.urls')), 
    path('admin/', admin.site.urls),
    path('arb/', include('arb.urls')),
    path('api/', include('api.urls')),
    path('docs/', include_docs_urls(title='ArbyAPI')),        
]

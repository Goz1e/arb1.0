"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.documentation import include_docs_urls


urlpatterns = [
    path('', include('acc_auth.urls')),
    path('accounts/', include('allauth.urls')), 
    path('admin/', admin.site.urls),
    path('arb/', include('arb.urls')),
    path('api/', include('api.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('docs/', include_docs_urls(title='ArbyAPI')),
    
    
]

# curl.exe  -X POST -H 'Content-Type: application/json' -d '{"email":"a@django.com", "password": "password"}' http://127.0.0.1:8000/api/token/
# curl.exe -X POST -H "Content-Type: application/json" -d "{'email':'a@django.com', 'password':'password'}" http://127.0.0.1:8000/api/token/

# curl.exe -X POST -H "Content-Type: application/json" -d '{"email": "a@django.com", "password": "password"}' http://127.0.0.1:8000/api/token/


# http http://127.0.0.1:8000/api/binance/ "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjgyNjU4NjQzLCJpYXQiOjE2ODI2NTgzNDMsImp0aSI6IjFmNTUxYjI1OGYzMTQ5NzU4YTQ4NmYwN2UxZGRkMDk1IiwidXNlcl9pZCI6M30.aS6k_24-qjw-c0YBBlY5v2XU-tEynBnCHAbvGdX-Nsg"
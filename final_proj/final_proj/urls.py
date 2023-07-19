"""
URL configuration for final_proj project.

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
from django.urls import path

from web_app.views import index_view, page1_view, test_page1_view, loading_page1_view, temp_page_view

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", index_view, name='index'),
    path("index/", index_view, name='index'),
    path("page1/<path:url>/", page1_view, name='page1'),
    path("test_page1/<path:url>/", test_page1_view, name='test_page1'),
    path("temp_page/<path:url>/", temp_page_view, name='temp_page'),
    path("loading_page1/<path:url>/", loading_page1_view, name='loading_page1'),
]

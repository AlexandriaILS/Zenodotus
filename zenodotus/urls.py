"""zenodotus URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from api import views


router = DefaultRouter()

router.register(r"record", views.RecordViewSet, basename="record")
router.register(r"itemtype", views.ItemTypeViewSet, basename="itemtype")
router.register(r"subject", views.SubjectViewSet, basename="subject")
router.register(r"itemtypebase", views.ItemTypeBaseViewSet, basename="itemtypebase")
router.register(
    r"bibliographiclevel", views.BibliographicLevelViewSet, basename="bibliographiclevel"
)

urlpatterns = [
    path("", views.index),
    url(r"^api/", include(router.urls)),
    path('admin/', admin.site.urls),
]

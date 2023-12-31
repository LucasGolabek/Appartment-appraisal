"""apartment_appraisal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import include, path

import debug_toolbar
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

from apartments import views

router = routers.SimpleRouter()

#router.register(r"apartment", views.UserApartmentView, basename="apartment")
router.register(r"apartments", views.UserApartmentsGetView, basename="apartments")
router.register(r"register", views.RegisterUserView, basename="register")

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),
    path("login/", obtain_auth_token, name="obtain-auth-token"),
    path("__debug__/", include(debug_toolbar.urls)),
    path("apartment/", views.UserApartmentView.as_view())
] + router.urls

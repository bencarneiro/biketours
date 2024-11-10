"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path, re_path
from backend.views import home, stripe_webhook, checkout, cancel, monitor, success, create_checkout_session, calendar, barton, report, favicon_view, homepage_image_1, homepage_image_2, homepage_image_3, homepage_image_4, homepage_image_5, gallery
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home, name="home"),
    path("stripe_webhook/", stripe_webhook, name="stripe_webhook"),
    path("checkout/", checkout, name="checkout"),
    path("cancel/", cancel, name="cancel"),
    path("success/", success, name="success"),
    path("calendar/", calendar, name="calendar"),
    path("barton/", barton, name="barton"),
    path("report/", report, name="report"),
    path("create_checkout_session/", create_checkout_session, name="create_checkout_session"),
    path("homepage_image_1", homepage_image_1, name="homepage_image_1"),
    path("homepage_image_2", homepage_image_2, name="homepage_image_2"),
    path("homepage_image_3", homepage_image_3, name="homepage_image_3"),
    path("homepage_image_4", homepage_image_4, name="homepage_image_4"),
    path("homepage_image_5", homepage_image_5, name="homepage_image_5"),
    path("gallery", gallery, name="gallery"),
    path("monitor", monitor, name="monitor"),
    re_path(r'^favicon\.ico$', favicon_view),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

"""SalmaFit URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from SalmaFit_api import views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import gettext_lazy as _


urlpatterns = i18n_patterns(
    path(_('admin/'), admin.site.urls),
    path('api/', include('SalmaFit_api.urls')),
    path('aboutus/', views.AboutUsView.as_view(), name='aboutus'),
    path('termsandconditions/', views.TermsAndConditionsView.as_view(), name='termsandconditions'),
    path('farsi/aboutus/', views.FarsiAboutUsView.as_view(), name='faaboutus'),
    path('farsi/termsandconditions/', views.FarsiTermsAndConditionsView.as_view(), name='fatermsandconditions'),
    path('privacypolicy/', views.PrivacyPolicyView.as_view(), name='privacypolicy'),
    prefix_default_language=True
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
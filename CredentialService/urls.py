"""CredentialService URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from Service_App import views

urlpatterns = [
    url('admin/', admin.site.urls),
 	url(r'^$', views.home, name='home'),
 	url(r'^issue_credential/$', views.issue_credential, name='issue_credential'),
    url(r'^issuer.json', views.issuer, name = 'issuer'),
    url(r'^download_issueFile/(?P<filename>.+)$', views.download_issueFile, name='download_issueFile'),
    url(r'^upload_credential', views.upload_credential, name='upload_credential'),
    url(r'^select_credential', views.select_credential, name='select_credential'),
    url(r'^download_selectFile/(?P<filename>.+)$', views.download_selectFile, name='download_selectFile'),
    url(r'^verify_credential', views.verify_credential, name='verify_credential'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


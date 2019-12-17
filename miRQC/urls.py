"""miRQC URL Configuration

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
from django.urls import path
from newJob.views import startNew, testMulti, launchJob, checkStatus
from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path('admin/', admin.site.urls),
    url(r'^/*$', startNew.as_view(), name='home'),
    url(r'^check', checkStatus.as_view(), name="check_status"),
    url(r'^testqc', testMulti.as_view()),
    url(r'^launch', launchJob.as_view(), name="launch"),
    url(r'^result', include('results.urls')),
    url(r'^upload/[A-za-z0-9]+', startNew.as_view()),
]


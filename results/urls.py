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
from .views import testMulti, loadResults, ajax_heatmap, ajax_percentiles
from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    url(r'testqc', testMulti.as_view()),
    url(r'^ajax_hm$', ajax_heatmap, name='ajax_hm'),
    url(r'^ajax_perc$', ajax_percentiles, name='ajax_perc'),

    url(r'[A-za-z0-9]+', loadResults.as_view()),
    url(r'', loadResults.as_view(), name="result_page"),

]


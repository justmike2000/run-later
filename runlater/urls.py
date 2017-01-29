"""runlater URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from . import views
from jobs import views as job_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^$', views.index),

    url(r'^login_user/', views.login_user),
    url(r'^verify_login/', views.verify_login),
    url(r'^logout_user/', views.logout_user),

    url(r'^dashboard/$', views.dashboard),
    url(r'^dashboard/runs/$', views.runs),
    url(r'^dashboard/jobs/$', views.jobs),
    url(r'^dashboard/jobs/add/', views.add_job),
    url(r'^dashboard/jobs/(\d+)/', views.job),

    url(r'^api/jobs/', job_views.jobs),
    url(r'^api/runs/', job_views.runs),
]

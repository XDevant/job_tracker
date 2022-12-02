"""jobtracker URL Configuration

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
from django.urls import path
from django.conf import settings
from jobtable import views as table_views
from authentication import views as auth_views
from django.conf.urls.static import static


urlpatterns = [
    path("admin/", admin.site.urls),
    path('jobs/', table_views.jobs, name='jobs'),
    path('jobs/prospects/add/', table_views.create_prospect, name='create-prospect'),
    path('jobs/prospects/', table_views.create_prospect, name='list-prospects'),
    path('signup/', auth_views.signup_page, name='signup'),
    path('', auth_views.login_page, name='login'),
    path('logout/', auth_views.logout_user, name='logout'),
]
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

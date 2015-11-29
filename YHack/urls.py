from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^submit/', include('submit.urls', namespace="submit")),
    url(r'^admin/', include(admin.site.urls)),
]
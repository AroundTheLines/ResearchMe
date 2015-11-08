from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^apply$', views.apply, name='apply'),
    url(r'^review$', views.review, name='review'),
    url(r'^process$', views.process, name='process'),
    url(r'^view_resume/(?P<resume_id>[0-9]+)/$', views.view_resume, name='view_resume'),
]
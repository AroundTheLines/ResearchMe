from django.conf.urls import url

from . import views

urlpatterns = [
	# /polls/
    url(r'^$', views.index, name='index'),
    # /polls/__some_number__/
    url(r'^(?P<question_id>[0-9]+)/$', views.detail, name='detail'),
    # /polls/__some_number__/results/
    url(r'^(?P<question_id>[0-9]+)/results/$', views.results, name='results'),
    # /polls/__some_number__/vote/
    url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
]
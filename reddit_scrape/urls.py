from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^scrape/$', views.scrape_reddit),
	url(r'^view_titles/$', views.view_titles),
]
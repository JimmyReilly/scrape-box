from django.shortcuts import render
from django.http import HttpResponse
from reddit_scrape.scrape import scrape_page

from .models import Link

def index(request):
	return HttpResponse("this is just a test")

def scrape_reddit(request):
	titles = scrape_page(6)

	insert_list = []
	for link_title in titles:
		insert_list.append(Link(title=link_title))

	Link.objects.bulk_create(insert_list) 

	return HttpResponse("saved")
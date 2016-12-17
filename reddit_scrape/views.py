from django.shortcuts import render
from django.http import HttpResponse
from reddit_scrape.scrape import scrape_page

def index(request):
	return HttpResponse("this is just a test")

def scrape_reddit(request):
	titles = scrape_page(6)
	return HttpResponse("saved")


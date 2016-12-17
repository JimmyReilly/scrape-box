import requests
from bs4 import BeautifulSoup

def scrape_page(pages_deep):
	url = "http://reddit.com"

	session = requests.Session()
	header = {
		"Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
		"Accept-Encoding" : "gzip, deflate, sdch, br",
		"Accept-Language" : "en-US,en;q=0.8,pt;q=0.6",
		"Cache-Control" : "max-age=0",
		"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"
		}

	r = session.get(url, headers=header)
	soup = BeautifulSoup(r.text, 'html.parser')

	link_titles = []

	for tag in soup.find_all('p', {"class" : "title"}):
		if tag.text:
			link_titles.append(tag.text)

	for _ in range(pages_deep):
		url = soup.find('span', {"class" : "next-button"}).a['href']

		r = session.get(url, headers=header)
		soup = BeautifulSoup(r.text, 'html.parser')

		for tag in soup.find_all('p', {"class" : "title"}):
			if tag.text:
				link_titles.append(tag.text)

	return link_titles
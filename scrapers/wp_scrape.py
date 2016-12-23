import requests
import os
from bs4 import BeautifulSoup

full_output = False

username = os.environ['WPUSERNAME']
password = os.environ['WPPASSWORD']

login_url = "https://warriorplus.com/login/login.php"
data_url = "https://warriorplus.com/wsopro/affiliate/get-offers.php?o=7"
keywords_url = "https://warriorplus.com/include/ajax/offer-tags-info.php?id="

header = {
	"Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
	"Accept-Encoding" : "gzip, deflate, sdch, br",
	"Accept-Language" : "en-US,en;q=0.8,pt;q=0.6",
	"Cache-Control" : "max-age=0",
	"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"
}

params = {
	"j_username" : username,
	"j_password" : password,
	"autologin" : 1,
	"returnto" : data_url,
}

#get new session
session = requests.Session()

#log into w+
s = session.post(login_url, params)

# get page data
s = session.get(data_url)
soup = BeautifulSoup(s.text, 'html.parser')

# Iterate each row on the page
for tag in soup.find_all('tr', {'class' : ''}):
	keywords = []

	#Get Product Name
	product_name_tag = tag.find('a', {'class' : 'offer-tags-info'})
	if (product_name_tag):
		product_name = product_name_tag.contents[0]

		# Get Keywords
		oid = product_name_tag['oid']
		offer_ajax = session.get(keywords_url + oid)
		ajax_soup = BeautifulSoup(offer_ajax.text, 'html.parser')
		
		for span in ajax_soup.find_all('span'):
			keywords.append(span.contents[0])

	#Get vendor
	vendor = tag.find('a', {'class' : 'seller_link_link'})
	if vendor:
		vendor = vendor.contents[0]

		# Get contest bool
		contest = bool(tag.find('i', {'class' : 'icon-gift'}))

		# Get rebill bool
		rebill = bool(tag.find('i', {'class' : 'icon-repeat'}))

		# Get POTD Bool
		potd = bool(tag.find('span', {'class' : 'badge-featured'}))

		# Get Launch date
		launch_date = tag.find('td', {'nowrap' : 'nowrap'})
		if launch_date:
			launch_date = launch_date.contents[0]

		num_class = tag.findAll('td', {'class' : 'num'})
		currency_class = tag.findAll('td', {'class' : 'currency'})
		
		if num_class:	
			sales = num_class[0].contents[0]
			conversion = num_class[1].contents[0]
			refund_rate = num_class[3].contents[0]
		
		if currency_class:
			visitor_value = currency_class[0].contents[0]
			avg_sale = currency_class[1].contents[0]

		if full_output:
			print("VENDOR: " + vendor)
			print("CONTEST: " + str(contest))
			print("POTD: " + str(potd))
			print("VENDOR: " + vendor)
			print("LAUNCH DATE: " + launch_date)
			print("SALES: " + sales)
			print("CONVERSION: " + conversion)
			print("REFUND RATE: " + refund_rate)
			print("VISITOR VALUE: " + visitor_value)
			print("AVG SALE: " + avg_sale)
			print("*******************")
		else:
			print(vendor)

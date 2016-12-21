# offer
# 	*name
# 	*vendor
# 	*contest bool
# 	*recur bool
# 	*featured bool
# 	*launch date
# 	*sales
# 	*conversion rate
# 	*visitor value
# 	*refund rate
# 	*keywords

# vendor
# 	*name
# 	*location
# 	*sales total
# 	has many offers
# 	followers
# 	number of potd
# 	member since
# 	contact links

# product
# 	price
# Enter user credentials in commandline or ENV


import requests
import os
from bs4 import BeautifulSoup

username = os.environ['WPUSERNAME']
password = os.environ['WPPASSWORD']

login_url = "https://warriorplus.com/login/login.php"
data_url = "https://warriorplus.com/wsopro/affiliate/get-offers.php?o=7"
keywords_url = "https://warriorplus.com/include/ajax/offer-tags-info.php?id="
member_url = "https://warriorplus.com/member/"

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

# geet page data
s = session.get(data_url)

soup = BeautifulSoup(s.text, 'html.parser')

for tag in soup.find_all('tr', {'class' : ''}):
	product_name = tag.find('a', {'class' : 'offer-tags-info'})

	keywords = []

	# GET KEYWORDS
	if (product_name):
		oid = product_name['oid']
		offer_ajax = session.get(keywords_url + oid)
		ajax_soup = BeautifulSoup(offer_ajax.text, 'html.parser')
		
		for span in ajax_soup.find_all('span'):
			keywords.append(span.contents[0])

	if (product_name):
		product_name = product_name.contents[0]
		# print(product_name + ":")
		# for key in keywords:
		# 	print(key)
		# print("********")

	vendor = tag.find('a', {'class' : 'seller_link_link'})
	if vendor:
		#vendor 
		vendor = vendor.contents[0]

		vendor_page = session.get(member_url + vendor)
		vendor_soup = BeautifulSoup(vendor_page.text, 'html.parser')
		
		#	name
		vendor_name = vendor_soup.find('div', {'class' : 'overview-text-large overview-text'})
		if vendor_name:
			vendor_name = vendor_name.text.strip()
		#	print(vendor + ": " + vendor_name)
		# 	location
		location = vendor_soup.find('i', {'class' : 'icon-map-marker'})
		if location:
			location = location.parent.text.strip()
		
####### Need to rework, logic fails on missing item

		#	followers
		followers = vendor_soup.find('span', {'class' : 'cnt-large'})
		if followers:
			followers = followers.text.strip()
			#print(vendor + ": " + followers)
		# 	sales total
		sales = vendor_soup.find_all('span', {'class' : 'cnt-large'})
		if sales:
			sales = sales[1].text.strip()
			#print(vendor + ": " + sales)
		# 	products
		products = vendor_soup.find_all('span', {'class' : 'cnt-large'})

		print(vendor)
		for item in products:
			print(item.text)
		print('********')
		# if products:
		# 	products = products[2].text.strip()
			#print(vendor + ": " + sales)
		



		# 	number of potd
		# 	member since
		# 	contact links

	contest = bool(tag.find('i', {'class' : 'icon-gift'}))

	# if vendor:
	# 	if contest:
	# 		print(vendor + "  yes")
	# 	else:
	# 		print(vendor + "  NO")

	rebill = tag.find('i', {'class' : 'icon-repeat'})

	# if vendor:
	# 	if rebill:
	# 		print(vendor.contents[0] + "  yes")
	# 	else:
	# 		print(vendor.contents[0] + "  NO")

	potd = tag.find('span', {'class' : 'badge-featured'})

	# if vendor:
	# 	if potd:
	# 		print(vendor.contents[0] + "  yes")
	# 	else:
	# 		print(vendor.contents[0] + "  NO")

	launch_date = tag.find('td', {'nowrap' : 'nowrap'})
	# if launch_date:
	# 	print(launch_date.contents[0])

	num_class = tag.findAll('td', {'class' : 'num'})
	currency_class = tag.findAll('td', {'class' : 'currency'})
	
	if num_class:	
		sales = num_class[0]
		conversion = num_class[1]
		refund_rate = num_class[3]
	
	if currency_class:
		visitor_value = currency_class[0]
		avg_sale = currency_class[1]

	# if vendor:
	# 	print("Vendor: " + vendor.contents[0])
	# 	print("Product Name:" product_name.contents[0])
	# 	if contest:
	# 		print("Has Contest: " + "  yes")
	# 	else:
	# 		print("Has Contest: " + "  NO")
	# 	if potd:
	# 		print("Was POTD: " +  "  yes")
	# 	else:
	# 		print("Was POTD: " +  "  NO")
	# 	print("Sales: " + sales.contents[0])
	# 	print("Conversion: " + conversion.contents[0])
	# 	print("Visitor Value: " + visitor_value.contents[0])
	# 	print("Avg Sale: " + avg_sale.contents[0])
	# 	print("Refund Rate: " + refund_rate.contents[0])
	# print("*************")


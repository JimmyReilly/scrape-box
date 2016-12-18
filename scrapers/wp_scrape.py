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
# 	keywords

# vendor
# 	name
# 	location
# 	sales total
# 	has many offers
# 	followers
# 	number of potd
# 	member since
# 	contact links

# product
# 	price
# Enter user credentials in commandline or ENV


import requests
from bs4 import BeautifulSoup

username = ""
password = ""
login_url = "https://warriorplus.com/login/login.php"
data_url = "https://warriorplus.com/wsopro/affiliate/get-offers.php?o=7"

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

session = requests.Session()

s = session.post(login_url, params)

s = session.get(data_url)

soup = BeautifulSoup(s.text, 'html.parser')

for tag in soup.find_all('tr', {'class' : ''}):
	product_name = tag.find('a', {'class' : 'offer-tags-info'})
	# if product_name:
	# 	print(product_name.contents[0])

	vendor = tag.find('a', {'class' : 'seller_link_link'})
	# if vendor:
	# 	print(vendor.contents[0]).

	contest = tag.find('i', {'class' : 'icon-gift'})

	# if vendor:
	# 	if contest:
	# 		print(vendor.contents[0] + "  yes")
	# 	else:
	# 		print(vendor.contents[0] + "  NO")

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

	if vendor:
		print("Vendor: " + vendor.contents[0])
		print("Sales: " + sales.contents[0])
		print("Conversion: " + conversion.contents[0])
		print("Visitor Value: " + visitor_value.contents[0])
		print("Avg Sale: " + avg_sale.contents[0])
		print("Refund Rate: " + refund_rate.contents[0])
	print("*************")


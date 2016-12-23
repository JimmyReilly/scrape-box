import requests
import os
import sys
from urllib import parse
from bs4 import BeautifulSoup

username = os.environ['WPUSERNAME']
password = os.environ['WPPASSWORD']

login_url = "https://warriorplus.com/login/login.php"
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
	"returnto" : 'https://warriorplus.com/',
}

#get new session
session = requests.Session()

#log into w+
s = session.post(login_url, params)

#Pause on connection errors, log the error and set to retry at a later time

for line in sys.stdin:
	line = line.rstrip().strip()

	profile_url = member_url + parse.quote_plus(line)

	vendor_page = session.get(profile_url)
	vendor_soup = BeautifulSoup(vendor_page.text, 'html.parser')

	print(profile_url)

	# Get the vendor's real name
	vendor_name = vendor_soup.find('div', {'class' : 'overview-text-large overview-text'})
	if vendor_name:
		vendor_name = vendor_name.text.strip()

		# Get the location
		location = vendor_soup.find('i', {'class' : 'icon-map-marker'})
		if location:
			location = location.parent.text.strip()

		# Get the followers count
		followers = vendor_soup.find('div', {'class' : 'subscriber-count'}).find('span', {'class' : 'cnt-large'})
		if followers:
			followers = followers.text.strip()

		cnt_tags = vendor_soup.find_all('span', {'class' : 'cnt-normal'})

		sales = None
		products = None

		for tag in cnt_tags:
			if 'Sales' in tag.text:
				sales = tag
			if 'Products' in tag.contents[0]:
				products = tag

		# Get sale count
		if sales:
			sales = sales.parent.find('span', {'class' : 'cnt-large'}).text
		else:
			sales = '0'

		#Get product count
		if products:
			products = products.parent.find('span', {'class' : 'cnt-large'}).text
		else:
			products = '0'

		# Get POTD count
		potd_count = vendor_soup.find('span', {'class' : 'badge-dotd-count'})
		if potd_count:
			potd_count = potd_count.text
		else:
			potd_count = "0"


		th_tags = vendor_soup.find_all('th')

		member_since = None

		wf_url = None
		linkedIn_url = None
		facebook_url = None
		google_url = None
		twitter_url = None

		# Member since and contact links
		for tag in th_tags:
			if 'Member Since' in tag.contents[0]:
				member_since = tag.parent.find('td').contents[0]
			if 'Connected Accounts' in tag.contents[0]:
				connected_accounts = tag.parent.parent.parent
				account_links = connected_accounts.find_all('a')
				for link in account_links:
					href = link['href']
					if "warriorforum" in href:
						wf_url = href
					elif "linked" in href:
						linkedIn_url = href
					elif "facebook" in href:
						facebook_url = href
					elif "google" in href:
						google_url = href
					elif "twitter" in href:
						twitter_url = href

		if not member_since:
			member_since = "0"

		print("VENDOR: " + str(line))
		if vendor_name:
			print("VENDOR NAME: " + vendor_name)
		if location:
			print("LOCATION: " + location)
		if followers:
			print("FOLLOWERS: " + followers)
		if sales:
			print("SALES: " + sales)
		if products:
			print("PRODUCTS: " + products)
		if potd_count:
			print("POTD COUNT: " + potd_count)
		if member_since:
			print("MEMBER SINCE: " + member_since)
		if wf_url:
			print("WF URL: " + wf_url)
		if linkedIn_url:
			print("LINKEDIN URL: " + linkedIn_url)
		if facebook_url:
			print("FACEBOOK URL: " + facebook_url)
		if google_url:
			print("GOOGLE URL: " + google_url)
		if twitter_url:
			print("TWITTER URL: " + twitter_url)
		print('*********')
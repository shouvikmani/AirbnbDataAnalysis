import requests
import sys
import csv
import time

class AirbnbClient:
	def __init__(self):

		CLIENT_ID = "3092nxybyb0otqw18e8nh5nty"
		self.REQUEST_INTERVAL = .1
		self.DEBUG = True
		self.MAX_LIMIT = 50
		self.search_url = "https://api.airbnb.com/v2/search_results?client_id=" + CLIENT_ID
		self.listing_url = "https://api.airbnb.com/v2/listings/%d?client_id="+CLIENT_ID+"&_format=v1_legacy_for_p3"
		

	def scrape(self, location, num_listings):
		num_loops = (num_listings / self.MAX_LIMIT) + 1

		offset = 0
		listings = []
		while num_listings > 0:
			listings += self.search(location, limit=min(num_listings, self.MAX_LIMIT), offset=offset)
			num_listings -= self.MAX_LIMIT
			offset += self.MAX_LIMIT

		listings = map(lambda l: l["listing"]["id"], listings)
		print "Got %d total listings in %s" % (len(listings), location)

		return listings


	def search(self, location, limit, offset, locale="USD"):

		params = {
			"locale": locale,
			"_limit": limit,
			"_offset": offset,
			"location": location
		}
		resp = requests.get(self.search_url, params=params)
		if resp.status_code != 200:
			print "Error occured in request to %s" % self.search_url
			return []	
		results = resp.json()
		
		if self.DEBUG:
			print "Made request to %s" % resp.url


		return results["search_results"]

	def cleanse_str(self, s):
		s = s.replace(u"\u2018", "'").replace(u"\u2019", "'")
		s = s.replace('\n', ' ').replace('\r', '').replace(',','')
		return s.encode('utf-8')

	def parse_listings(self, listings, params_filename="params.csv", output_filename="airbnb-results.csv"):
		
		with open(params_filename, 'r') as f:
			params = f.readlines()
			f.close()

		params = map(lambda s: s.rstrip('\n'), params)
		
		pf = open(output_filename, 'w')
		writer = csv.writer(pf, delimiter=',', quotechar='', quoting=csv.QUOTE_NONE, escapechar='\\')
		writer.writerow(params)

		for i,lid in enumerate(listings):
			url = self.listing_url % lid
			resp = requests.get(url)
			l = resp.json()["listing"]
			vals = []
			for key in params:
				if type(l[key]) is unicode:
					s = self.cleanse_str(l[key])					
					vals.append(s)
				else:
					vals.append(l[key])

			writer.writerow(vals)
			time.sleep(self.REQUEST_INTERVAL)



if __name__ == "__main__":
	print sys.argv
	if len(sys.argv) < 3:
		print >> sys.stderr, "%s: usage: <location>" % sys.argv[0]
		sys.exit(1)

	ac = AirbnbClient()
	listings = ac.scrape(sys.argv[1], int(sys.argv[2]))
	print sys.argv
	if len(sys.argv) == 4:
		ac.parse_listings(listings, sys.argv[3])
	else:	
		ac.parse_listings(listings)





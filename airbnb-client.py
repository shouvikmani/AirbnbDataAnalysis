import requests
import sys
import csv
import time

class AirbnbClient:
	def __init__(self):
		# Public Airbnb Client Key (NOT SECRET)
		CLIENT_ID = "3092nxybyb0otqw18e8nh5nty"
		# Ensure we don't overload API with requests
		self.REQUEST_INTERVAL = .2
		# Debugging flag
		self.DEBUG = False
		# Max Number of results returned by each API search query
		self.MAX_LIMIT = 50
		# Base Search URL 
		self.search_url = "https://api.airbnb.com/v2/search_results?client_id=" + CLIENT_ID
		# Base Listing Info URL
		self.listing_url = "https://api.airbnb.com/v2/listings/%d?client_id="+CLIENT_ID+"&_format=v1_legacy_for_p3"
		

	def scrape(self, locations, num_listings_per_loc):

		listings = []
		# Loop through desired locations
		for location in locations:
			if self.DEBUG:
				print "Start scraping %s..." % location

			num_listings = num_listings_per_loc
			offset = 0
			# Since we are limited by pagination, calculate offset and obtain results incrementally
			while num_listings > 0:
				listings += self.search(location, limit=min(num_listings, self.MAX_LIMIT), offset=offset)
				num_listings -= self.MAX_LIMIT
				offset += self.MAX_LIMIT

		# Contruct listings id list
		listings = map(lambda l: l["listing"]["id"], listings)

		return listings


	def search(self, location, limit, offset, locale="USD"):
		# Build request
		params = {
			"locale": locale,
			"_limit": limit,
			"_offset": offset,
			"location": location
		}
		resp = requests.get(self.search_url, params=params)
		# Error checking
		if resp.status_code != 200:
			print "Error occured in request to %s: %s" % (resp.url, resp.content)
			return []	
		results = resp.json()
		
		if self.DEBUG:
			print "Made request to %s" % resp.url
		
		# Return results 
		return results["search_results"]

	def cleanse_str(self, s):
		s = s.replace(u"\u2018", "'").replace(u"\u2019", "'")
		s = s.replace('\n', ' ').replace('\r', '').replace(',','')
		return s.encode('utf-8')


	def parse_listings(self, listings, params_filename="params.txt", output_filename="airbnb-results.csv"):
		
		if self.DEBUG:
			print "Parsing %d listings..." % len(listings)

		# Read parameters file
		with open(params_filename, 'r') as f:
			params = f.readlines()
			params = map(lambda s: s.rstrip('\n'), params)	
			f.close()

		# Open results file for writing and write params	
		pf = open(output_filename, 'w')
		writer = csv.writer(pf, delimiter=',', quotechar='', quoting=csv.QUOTE_NONE, escapechar='\\')
		writer.writerow(params)

		# Enumerate listing ids and obtain information on each one
		for i,lid in enumerate(listings):
			url = self.listing_url % lid
			if self.DEBUG:
				print "Obtained %d listings so far..." % (i)

			# Call Airbnb API to get more information about the listing
			resp = requests.get(url)
			resp_json = resp.json()
			vals = []

			# Parse all desired params from results
			for key in params:
				l = resp_json["listing"]
				# Check if param is a host param
				if key.startswith("host_"):
					key = key.replace("host_", "")
					l = l["primary_host"]
				
				# Cleanup string if it's unicode (i.e. description)
				if type(l[key]) is unicode:
					s = self.cleanse_str(l[key])					
					vals.append(s)
				else:
					vals.append(l[key])

			writer.writerow(vals)
			# Sleep for a small interval to not rate limit API 
			time.sleep(self.REQUEST_INTERVAL)



if __name__ == "__main__":
	print sys.argv
	if len(sys.argv) < 3:
		print >> sys.stderr, "%s: usage: <locations seperated by ':'> <num_results>" % sys.argv[0]
		sys.exit(1)

	ac = AirbnbClient()
	locations = sys.argv[1].split(":")

	# Scrape API Search Results for all locations
	listings = ac.scrape(locations, int(sys.argv[2]))

	# Parse results
	print "Parsing the following locations: " + ", ".join(locations)
	if len(sys.argv) == 4:
		ac.parse_listings(listings, output_filename=sys.argv[3])
	else:	
		ac.parse_listings(listings)





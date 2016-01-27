import requests, os

# arg parse! need lat, lon for each point.

def setup_dictionary():
	""" create our dictionary to hold the distances between points. using Google maps routing API
	Input: 4 latitude, longitude points
	Output: dictionary
	"""
	google_key = os.environ.get("Google_API_Key")
	origin = '43.6533103,-79.3827675'
	destination = '45.5017123,-73.5672184'
	query_params = {'key': google_key,
					'origin': origin,
					'destination': destination
					}
	
	endpoint = 'https://maps.googleapis.com/maps/api/directions/json?'
	response = requests.get(endpoint, params=query_params).json()
	print response['routes'][0]['legs'][0]['distance']['value']

setup_dictionary()


"""store hte routes you need in a dictionary with "AB", etc. as key and value is {'lat/long pairs': (lat, long)}
loop over to calculate distance between pairs and store as another item in value dict.
calculate from A to B, A to C, C to D, D to B, C to A, B to D
find which is shorter - A to B - (AC, CD, DB)
or CD - (CA, AB, BD)

response['routes'][0]['legs'][0]['distance']['value']
"""
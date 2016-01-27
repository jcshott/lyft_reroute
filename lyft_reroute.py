import requests, os

# arg parse! need lat, lon for each point.

def get_leg_distance(x, y):
	""" make call to Google Distance API to get the distance between two lat/lon pairs
	Input: 2 strings that are comma seperated lat,lon
	i.e.  '43.6533103,-79.3827675', '45.5017123,-73.5672184'
	Output: distance in meters (int)
	"""

	query_params = {'key': os.environ.get("Google_API_Key"),
					'origin': x,
					'destination': y
					}
	
	endpoint = 'https://maps.googleapis.com/maps/api/directions/json?'
	response = requests.get(endpoint, params=query_params).json()
	
	return response['routes'][0]['legs'][0]['distance']['value']

def setup_dictionary(a, b, c, d):
	""" create our dictionary to hold the distances between points.
	"""
	route_legs = [(a,b), (a, c), (c, d), (d, b), (c, a), (b, d)]
	distance_dict =  {"ab": {"coord_pair": route_legs[0]},
						"ac": {"coord_pair": route_legs[1]},
						"cd": {"coord_pair": route_legs[2]},
						"db": {"coord_pair": route_legs[3]},
						"ca": {"coord_pair": route_legs[4]},
						"bd": {"coord_pair": route_legs[5]}
						}
	
	for key, value in distance_dict.iteritems():
		coord_tuple = value["coord_pair"]
		lat, lon = coord_tuple
		# coordinates = coord_tuple[0] + ", " + coord_tuple[1]
		distance = get_leg_distance(lat, lon)
		distance_dict[key]['distance'] = distance
	
	return distance_dict

# testing home to antonia's and personalis to tacolicious

setup_dictionary("37.4770169, -122.237806", "37.416566 -122.122387", "37.4759487, -122.1458561", "37.4433459, -122.1611703")

def find_smallest_reroute(A, B, C, D):
	"""calculate the shortest reroute distance for drivers starting at points A & C, travelling to B & D if one were to pick up/drop off the other
	"""

	# get our dictionary of distances between the 4 points
	distance_dict = setup_dictionary(A, B, C, D)


"""
calculate from A to B, A to C, C to D, D to B, C to A, B to D
find which is shorter - A to B - (AC, CD, DB)
or CD - (CA, AB, BD)

response['routes'][0]['legs'][0]['distance']['value']
"""
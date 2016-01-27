import requests, os, argparse

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



def find_shorter_reroute(A, B, C, D):
	"""calculate the shortest reroute distance for 2 drivers starting at points A & C, travelling to B & D (respectively) if one were to pick up/drop off the other

	shortest of:
	driver 1 re-route: AB - (AC, CD, DB)
	driver 2 re-route: CD - (CA, AB, BD)
	
	"""
	# get our dictionary of distances between the 4 points
	distance_dict = setup_dictionary(A, B, C, D)

	a_pickup_c = (distance_dict["ac"]["distance"] + distance_dict["cd"]["distance"] + distance_dict["db"]["distance"]) - distance_dict["ab"]["distance"]
	print a_pickup_c
	c_pickup_a = (distance_dict["ca"]["distance"] + distance_dict["ab"]["distance"] + distance_dict["bd"]["distance"]) - distance_dict["cd"]["distance"] 
	print c_pickup_a

	if a_pickup_c == c_pickup_a:
		return "It's the same distance for both re-routes!"
	elif a_pickup_c < c_pickup_a:
		return "The distance for driver 1 to re-route is shortest with a distance of %d meters" % (a_pickup_c)
	elif c_pickup_a < a_pickup_c:
		return "The distance for driver 2 to re-route is shortest with a distance of %d meters" % (c_pickup_a)


def main():
	"""parse command line arguments to get user's lat/lon combinations"""
	# TODO: argeparse to get a,b,c,d
	parser = argparse.ArgumentParser(description="Find shortest re-route for 2 drivers")
	# parser.add_argument('-h', '--help', help='enter 4 latitude,longitue pairs for the 4 points to be evaluated. no space after comma in pair')
	parser.add_argument('-a', '--a', action='store', dest='A', help='enter the lat,lon of point A, start point of driver 1', required=True)
	parser.add_argument('-b', '--b', action='store', dest='B', help='lat,lon of point B, end point of driver 1', required=True)
	parser.add_argument('-c', '--c', action='store', dest='C', help='lat,lon of point C, start point of driver 2', required=True)
	parser.add_argument('-d', '--d', action='store', dest='D', help='lat,lon of point D, end point of driver 2', required=True)
	
	parse_results = parser.parse_args()
	
	A = parse_results.A
	B = parse_results.B
	C = parse_results.C
	D = parse_results.D

	return find_shorter_reroute(A, B, C, D)
	# testing home to antonia's and personalis to tacolicious
	# return find_shorter_reroute("37.4770169, -122.237806", "37.416566 -122.122387", "37.4759487, -122.1458561", "37.4433459, -122.1611703")



if __name__ == '__main__':
	print main()


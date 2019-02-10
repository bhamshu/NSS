#this module takes as input a list of addresses and a given address and returns a list of tuples (index, dist) sorted by distance.
#https://delhimetrorail.info/-sarojini-nagar-delhi-metro-station-to-rajiv-chowk-delhi-metro-station

def nearest(arr, add):
	
	arrset = list(set(arr))
	arrset.insert(0, add)
	arrset = [str(x)+", "+str(y) for x, y in arrset]
	
	params = {
  			 "locations": arrset,
   			"options": {
     		"manyToOne": True
 			}
	 	}
	
	import requests, json
	url = "http://www.mapquestapi.com/directions/v2/routematrix?key=Q6O6RIYtJ8TDQeJmBbdsrN0P9q7JQoGb"
	resp = requests.post(url=url, json=params)
	#print("BBB", resp, "AAA", resp.text)
	json_data = json.loads(resp.text)
	#print(json_data)
	dist = json_data["distance"][1:]
	time = json_data["time"][1:]
	arrset = arrset[1:]
	d = []

	for i in range(len(arr)):
		ind = arrset.index( str(arr[i][0])+", "+str(arr[i][1]) ) 
		d.append( (i, arr[i], dist[ind] ) )


	sortbyd = lambda tup: tup[2]
	d.sort(key = sortbyd)
	
	return d
	

if __name__ == "__main__":
	#nearest([0, 1],2)
	pass
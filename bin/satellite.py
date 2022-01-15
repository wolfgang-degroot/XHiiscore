import urllib3
import os.path
import time
import requests
import json
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def gatherer(dimension="world", map="map.knockoutmc.com"):
	path = "/up/world/"

	url = "https://" + map + path + dimension + "/"
	frame = requests.get(url, verify=False).json()
	players = frame["players"]
	timestamp = frame["timestamp"]

	return {"timestamp": timestamp, "players": players, "dimension": dimension}


def hunter(data):
	frame = dict()
	for player in data["players"]:
		if player["world"] != data["dimension"]:
			continue
		frame[player["account"]] = [
			int(player["x"]),
			int(player["y"]),
			int(player["z"])
		]
	return [data["timestamp"], frame]

def sun(dimension, interval=30):
	address = dimension+".json"
	if not os.path.exists(address):
		print("No log found. Generating new...")
		open(address, 'w').close()
	while 1 == 1:
		with open(address, "r+") as chest:
			bounty = hunter(gatherer(dimension))
			try:
				storage = dict(json.load(chest))
			except:
				storage = dict()
			storage[bounty[0]] = bounty[1]
			chest.write(json.dumps(storage, indent=2))
			print(".", end="")
		time.sleep(interval)


if __name__ == "__main__":
	interval = 3  # Update rate in seconds
	dimension = "world"
	# Dimension Guide:
	# Overworld	= 'world'
	# Nether	= 'world_nether'
	# The End	= '???'

	print("Updating every " + str(interval) + " seconds.")
	sun(dimension, interval)

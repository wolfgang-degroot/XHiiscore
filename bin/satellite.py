import sys
import time
import requests
import json


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

def sun(dimension, interval=5):
	while 1 == 1:
		with open(dimension+".json", "r") as chest:
			bounty = hunter(gatherer(dimension))
			try:
				storage = json.load(chest)
			except:
				storage = dict()
			storage[bounty[0]] = bounty[1]

		with open(dimension+".json", "w") as f:
	   		f.write(json.dumps(storage))
		time.sleep(interval)


if __name__ == "__main__":
	interval = 30  # Update rate in seconds
	dimension = "world"
	# Dimension Guide:
	# Overworld	= 'world'
	# Nether	= 'world_nether'
	# The End	= '???'

	print("Updating every " + str(interval) + " seconds.")
	sun(dimension, interval)

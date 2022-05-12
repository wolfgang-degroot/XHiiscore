import urllib3
import time
import requests
import os.path
import json
import gzip
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def gatherer(dimension="world", map="map.knockoutmc.com"):
    url = "https://{}/up/world/{}/".format(map, dimension)
    try:
        frame = requests.get(url, verify=False).json()
    except:
        return False
    players = frame["players"]
    timestamp = frame["timestamp"]

    return {"timestamp": timestamp, "players": players, "dimension": dimension}


def hunter(data):
    if data == False:
        return False
    else:
        frame = dict()
        for player in data["players"]:
            if player["world"] != data["dimension"]:
                continue
            frame[player["account"]] = [
                int(player["x"]),
                int(player["y"]),
                int(player["z"])
            ]
        return {data["timestamp"]: frame}


def inventory(address):
    if not os.path.exists(address):
        print("No log found. Generating new...")
        open(address, 'w').close()
        storage = {}
    else:
        bounty = hunter(gatherer(dimension))
        if bounty == False:
            return False
        try:
            with open(address) as chest:
                storage = json.load(chest)
        except:
            storage = {}
    with open(address, "w") as chest:
        storage.update(bounty)
        json.dump(storage, chest, separators=(',', ':'),)
    return True


def sun(dimension="world", interval=30):
    counter = missed = 0  # Weird as hell but it works
    while 1 == 1:
        if inventory(dimension+".json"):
            if counter % 32 == 0:
                print("[", end="")
            elif counter % 32 == 31:
                print("]", end="")
                print(" " + str(missed) + " missed." if missed > 0 else "\n")
                missed = 0
            else:
                print(".", end="")
            counter += 1
        else:
            missed += 1
        time.sleep(interval)


if __name__ == "__main__":
    interval = 15  # Update rate in seconds
    dimension = "world"
    # Dimension Guide:
    # Overworld	= 'world'
    # Nether	= 'world_nether'
    # The End	= '???'

    print("Updating every " + str(interval) + " seconds.")
    sun(dimension, interval)

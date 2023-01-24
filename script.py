import requests
import os
import base64
import urllib3
from time import sleep
import json

CONFIG = {
    'Ascent': "Jett",
    'Pearl': "Jett",
    'Haven': "Cypher",
    'Split': "Jett",
    'Icebox': "Reyna",
    'Fracture': "Harbor",
    'Lotus': "Breach",
}

REGION = "na"
SHARD = "na"

# get account lockfile
lockfile_path = os.path.join(os.getenv("LOCALAPPDATA"), R"Riot Games\Riot Client\Config\lockfile")

with open(lockfile_path) as lockfile:
    data = lockfile.read().split(":")
    keys = ["name", "PID", "port", "password", "protocol"]
    lockfile = dict(zip(keys, data))

# get current version
data = requests.get("https://valorant-api.com/v1/version")
data = data.json()["data"]
current_version = f"{data['branch']}-shipping-{data['buildVersion']}-{data['version'].split('.')[3]}"  # return formatted version string

# get local headers
local_headers = {
    "Authorization": (
        "Basic "
        + base64.b64encode(
            ("riot:" + lockfile["password"]).encode()
        ).decode()
    )
}

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# get entitlements, this will be used for headers
entitlements = requests.get(
    f'https://127.0.0.1:{lockfile["port"]}/entitlements/v1/token',
    headers=local_headers,
    verify=False,
).json()

# set up the headers for the rest of the requests
headers = {
    "Authorization": f"Bearer {entitlements['accessToken']}",
    "X-Riot-Entitlements-JWT": entitlements["token"],
    "X-Riot-ClientPlatform": "ew0KCSJwbGF0Zm9ybVR5cGUiOiAiUEMiLA0KCSJwbGF0Zm9ybU9TIjogIldpbmRvd3MiLA0KCSJwbGF0Zm9ybU9TVmVyc2lvbiI6ICIxMC4wLjE5MDQyLjEuMjU2LjY0Yml0IiwNCgkicGxhdGZvcm1DaGlwc2V0IjogIlVua25vd24iDQp9",
    "X-Riot-ClientVersion": current_version,
}

# get rnet chat session
session = requests.get(
    f'https://127.0.0.1:{lockfile["port"]}/chat/v1/session',
    headers=local_headers,
    verify=False
).json()

game_data = eval(requests.get("https://pastebin.com/raw/4nRP6XwW").text) # i will be updating this every time it changes

while True:

    sleep(1)    # it will still instalock, don't worry :P

    # get the current presence of your game, this can be MENUS, PREGAME, or COREGAME
    data = requests.get(
        f'https://127.0.0.1:{lockfile["port"]}/chat/v4/presences',
        headers=local_headers,
        verify=False
    ).json()

    for presence in data["presences"]:
        if presence["puuid"] == session["puuid"]:
            presence = json.loads(base64.b64decode(presence["private"]))["sessionLoopState"]
            break
    
    if presence == "MENUS": continue # dont do anything if you're in the menus

    if presence == "PREGAME": # this is set to pregame right as you hear "MATCH FOUND!!", which is why sleeping every second 
        while True:
            
            try:
                match_id = requests.get(
                    f"https://glz-{REGION}-1.{SHARD}.a.pvp.net/pregame/v1/players/{session['puuid']}",
                    headers=headers
                ).json()["MatchID"]
            except: # this except is here because sometimes it will run after loading into the coregame, so it will throw an error
                break

            match_data = requests.get(
                f"https://glz-{REGION}-1.{SHARD}.a.pvp.net/pregame/v1/matches/{match_id}",
                headers=headers
            ).json()

            map_id = match_data["MapID"]

            for map_name, map_value in game_data["maps"].items():
                if map_value == map_id:
                    map_name = map_name
                    break

            agent_id = game_data["agents"][CONFIG[map_name]]

            response = requests.post(
                f"https://glz-{REGION}-1.{SHARD}.a.pvp.net/pregame/v1/matches/{match_id}/lock/{agent_id}",
                headers=headers
            ).json()

            break # go back to scanning for pregame so you dont need to run the program again
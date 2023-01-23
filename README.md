# VALORANT-Instalocker
Locks agents before the game even starts to load, made in less than an hour

To use this with your own agents, edit the CONFIG and REGION near the top of the code
```py
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
```

This is only for educational purposes, please do not use it online!

## How does it work?
Whenever you attempt to lock an agent ingame, you are just sending a network request.
All I am doing here is sending that same request before the game loads in.

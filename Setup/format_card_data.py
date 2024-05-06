import json

items_to_remove = ["Island", "Swamp", "Mountain", "Forest", "Plains"]
THE_LIST = [
    'Smuggler\'s Copter', 
    'Bishop of the Bloodstained', 
    'Burden of Guilt', 
    'Evolutionary Leap', 
    'Combine Chrysalis', 
    'Consign // Oblivion', 
    'Crashing Footfalls',
    'Possibility Storm', 
    'Drown in the Loch',
    'Duskmantle, House of Shadow', 
    'Enlisted Wurm', 
    'Fabricate',
    'Field of the Dead',
    'Gamble',
    'Ghost Quarter', 
    'Ghostly Prison',
    'Gnaw to the Bone', 
    'Goblin Warchief', 
    'Hard Evidence', 
    'High Alert', 
    'Ixidor, Reality Sculptor', 
    'Jace, Wielder of Mysteries', 
    'Krosan Tusker', 
    'Kuldotha Rebirth', 
    'Laid to Rest', 
    'Leonin Relic-Warder', 
    'Magmaw', 
    'Mass Hysteria', 
    'Maverick Thopterist', 
    'Mentor of the Meek', 
    "Metalspinner's Puzzleknot", 
    'Millstone', 
    'Mistveil Plains', 
    'Molten Psyche', 
    'Monologue Tax', 
    'Mystery Key', 
    'Nyx Weaver', 
    'Putrid Warrior', 
    'Quintorius, Field Historian', 
    'Ranger-Captain of Eos', 
    'Shard of Broken Glass', 
    'Show and Tell',
    'Spell Snare', 
    'Stromkirk Captain', 
    'Syr Konrad, the Grim', 
    'Tireless Tracker',
    'Tragic Slip',
    'Treacherous Terrain', 
    'Victimize',
    'Worldspine Wurm',
]
ARENA_EXC = ['Smuggler\'s Copter', 'Evolutionary Leap', 'Possibility Storm']
#The list is a collection of cards that can appear in booster packs even though the cards technically do not belong to that set.
#Arena exclusive list cards are list cards that only appear in the arena online platform because of course they do.
print(len(THE_LIST))

MKM_file_path = 'data/json/MKM.json'
list_file_path = 'data/json/PLST.json'
rm_file_path = 'data/json/MKM_filtered.json'

with open(MKM_file_path, 'r', encoding='utf-8') as file:
    MKM_data = json.load(file)
    
with open(list_file_path, 'r', encoding='utf-8') as file:
    list_data = json.load(file)

filtered_data = []   
    
for card in list_data["data"]["cards"]:
    if any(card["name"] == item["name"] for item in filtered_data):
        existing_card = next(item for item in filtered_data if item["name"] == card["name"])
        existing_card["types"] += card["types"]
    elif card["name"] in THE_LIST:
        object = {"colorIdentity": card["colorIdentity"],
                  "convertedManaCost": card["convertedManaCost"],
                  "name": card["name"],
                  "types": card["types"],
                  "rarity": "list"}
        filtered_data.append(object)
    
for card in MKM_data["data"]["cards"]:
    if any(card["name"] == item["name"] for item in filtered_data):
        existing_card = next(item for item in filtered_data if item["name"] == card["name"])
        existing_card["types"] += card["types"]
    elif "promoTypes" in card and "prerelease" in card["promoTypes"]:
        pass
    elif card["name"] not in items_to_remove :
        object = {"colorIdentity": card["colorIdentity"],
                  "convertedManaCost": card["convertedManaCost"],
                  "name": card["name"],
                  "types": card["types"],
                  "rarity": card["rarity"]}
        filtered_data.append(object)

for card in THE_LIST:
    print(card)
    print(any(card == item["name"] for item in filtered_data))
    if any(card == item["name"] for item in filtered_data):
        pass
    else:
        object = {"colorIdentity": None,
                "convertedManaCost": None,
                "name": card,
                "types": None,
                "rarity": "list"}
        filtered_data.append(object)

print(len(filtered_data))
sorted_data = sorted(filtered_data, key=lambda x: x["name"])
with open(rm_file_path, 'w') as file:
    json.dump(sorted_data, file, indent=4)


import json

colors = "WUBRG"
color_pairs = ["WU", "WB", "WR", "WG", "UB", "UR", "UG", "BR", "BG", "RG"]
rarity_boost = {
    'common': 0.0,
    'uncommon': 0.2,
    'list': 0.25,
    'rare': 0.3,
    'mythic': 0.4
}

cards_file_path = 'data/json/MKM_filtered.json'
weights_file_path = 'data/json/MKM_weights.json'
with open(cards_file_path, 'rb') as f:
    card_set = json.load(f)


def card_weight(color_identity, color_pair, rarity):
    overlap = set(color_identity) & set(color_pair)
    if len(overlap) != 0:
        return ( 0.5*len(overlap) / len(color_identity) + rarity_boost[rarity])
    else: #wrong colors
        return 0


card_ratings = {}
for card in card_set:
    color_identity = card['colorIdentity']
    rarity = card['rarity']
    if not color_identity: #colorless
        card_weights = {
            color_pair[0] + color_pair[1]: 0.25 + rarity_boost.get(rarity, 0.0)
            for color_pair in color_pairs
        }
    else:
        card_weights = {
            color_pair[0] + color_pair[1]: card_weight(color_identity, color_pair, rarity)
            for color_pair in color_pairs
        }
    card_ratings[card['name']] = card_weights


with open(weights_file_path, 'w') as f:
    json.dump(card_ratings, f)
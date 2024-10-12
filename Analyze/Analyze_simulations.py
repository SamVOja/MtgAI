import matplotlib.pyplot as plt
import json

class Plotter:
    def __init__(self):
        self.archetype_names = ["WU", "WB", "WR", "WG", "UB", "UR", "UG", "BR", "BG", "RG"]
    
    def plot_card_types(self, drafters, drafts): #not used
        card_types = ["Artifact", "Battle", "Creature", "Enchantment", "Instant", "Land", "Planeswalker", "Sorcery"]
        card_counters = {card_type: 0 for card_type in card_types}
        for i, draft in enumerate(drafts):
            card_types_mapping = {card['name']: card['types'] for card in draft.packs.cards}
            for drafter in range(drafters):
                cards_pick = self.cards_in_archetype(drafter-1, draft)
                for card_name in cards_pick:
                    if card_name in card_types_mapping:
                        types = set(card_types_mapping[card_name])
                        for card_type in types:
                            if card_type in card_counters:
                                card_counters[card_type] += 1
        card_counters = {key: value / (drafters) / (i+1) for key, value in card_counters.items()}
        sorted_counters = dict(sorted(card_counters.items(), key=lambda item: item[1], reverse=True))
        plt.bar(sorted_counters.keys(), sorted_counters.values())
        plt.xlabel('Card Type')
        plt.ylabel('Count')
        plt.title('Number of Each Card Type in Owned Cards')
        plt.tick_params(axis='x', rotation=45)
        plt.tight_layout()  
        plt.show()

    def plot_arch_preference(self, drafts):
        """Plot average preference for each of the two color archetypes"""
        drafter = 0
        arch_counters = {arch: 0 for arch in self.archetype_names}
        for i, draft in enumerate(drafts, start=1):
            picks = self.cards_picked(drafter, draft)
            arch_pref = self.calc_archetype_preference(drafter, draft, picks)
            arch_counters[arch_pref] += 1
        values_list = list(arch_counters.values())
        values_sum = sum(values_list)
        normalized_values = [value / values_sum for value in values_list]
        plt.bar(arch_counters.keys(), normalized_values)
        plt.xlabel('Archetype Names')
        plt.ylabel('Ratio of Archetype preference')
        plt.title('')
        plt.tick_params(axis='x', rotation=45)
        plt.tight_layout()  
        plt.show() 
    
    def calc_win_rates(self, drafters, drafts, json_file_path):
        """Calculate average winrates for the best 23 cards in archetype """
        with open(json_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            
            full_list = []
            best_list = []
            land_list = []
            for i, draft in enumerate(drafts, start=1):
                for drafter in range(1, drafters+1):
                    cards = []
                    lands = []

                    picks = self.cards_in_archetype(drafter-1, draft)
                    for card in picks:
                        cards.append(data[card])

                    sorted_list = sorted(cards, reverse=True)
                    full_list += sorted_list
                    best_list += sorted_list[:min(23, len(sorted_list))]
            print("Average cards on color")
            print(len(full_list)/((drafter)*(i)))
            print("Average card winrate of 23 best cards (on color)")
            print(sum(best_list)/(drafter)/(i)/(23)) #penalize if less than 23
        
    def plot_mana_curve(self, drafters, drafts):
        """Print the average distribution of different costed cards drafted"""
        mana_costs = ["0", "1", "2", "3", "4", "5", "6+"]
        mana_counters = {mana_cost: 0 for mana_cost in mana_costs}
        for i, draft in enumerate(drafts):
            card_mana_mapping = {card['name']: card['convertedManaCost'] for card in draft.packs.cards}
            for drafter in range(drafters):
                
                cards_pick = self.cards_in_archetype(drafter-1, draft)
                for card_name in cards_pick:
                    if card_name in card_mana_mapping:
                        if int(card_mana_mapping[card_name]) > 5:
                            mana_counters["6+"] += 1
                        elif int(card_mana_mapping[card_name]) > 0: 
                            mana_counters[str(int(card_mana_mapping[card_name]))] += 1
                        else:
                            mana_counters["0"] += 1
        mana_counters = {key: value / (drafters) / (i+1) for key, value in mana_counters.items()}
        plt.bar(mana_counters.keys(), mana_counters.values())
        plt.xlabel('Mana cost')
        plt.ylabel('Amount of cards')
        plt.title('Mana Curve')
        plt.tick_params(axis='x', rotation=45)
        plt.tight_layout()  
        plt.show() 
        
    def cards_picked(self, drafter, draft):
        """"Return cards picked by a player"""
        cards_picked = []
        picks = [pick[drafter] for pick in draft.picks]
        for pick in picks:
            cards_picked.append(pick["name"])
        return cards_picked
    
    def cards_in_archetype(self, drafter, draft):
        """Return cards picked by a player that are in their strongest archetype""" 
        cards_in_archetype = []
        cards_pick = self.cards_picked(drafter, draft)
        archetype = self.calc_archetype_preference(drafter, draft, cards_pick)
        archetype_mapping = {card['name']: card['colorIdentity'] for card in draft.packs.cards}
        for card_name in cards_pick:
            if card_name in archetype_mapping:
                colors = archetype_mapping[card_name] 
                if len(colors)==0:
                    cards_in_archetype.append(card_name)
                elif set(colors) & set(archetype):
                    cards_in_archetype.append(card_name)
        return cards_in_archetype
        
    def calc_archetype_preference(self, drafter, draft, picks): 
        """Determine the archetype of cards picked by a player"""
        vals = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for card in picks:
            card_weights = draft.weights[card]
            i = 0
            for arch in card_weights:
                vals[i] += card_weights[arch]
                i += 1
        max_value = max(vals)
        arch_index = vals.index(max_value)
        max_arch = draft.archetype_names[arch_index] 
        return max_arch


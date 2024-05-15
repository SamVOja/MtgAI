import random

class Picker:
    def __init__(self, picker, n_drafters, n_cards, weights):
        self.archetype_names = ["WU", "WB", "WR", "WG", "UB", "UR", "UG", "BR", "BG", "RG"]  
        self.n_drafters = n_drafters
        self.n_cards = n_cards
        self.weights = weights
        self.pref = [None, None, None, None, None, None, None, None, None, None]

        self.picks = []
        
        if picker == "WeightedvsWeighted":
            self.picker = self.WeightedvsWeighted
        elif picker == "Rare":
            self.picker = self.Rare
        elif picker == "Random":
            self.picker = self.Random
        elif picker == "WeightedvsRare":
            self.picker = self.WeightedvsRare
        else:
            self.picker = self.Random
    
    def Random(self, packs, arch_weights):
        """"Make random choices"""
        picks = []
        for pack in packs:
            pick = random.choice(pack)
            picks.append(pick)
            pack.remove(pick)
        return packs, picks
    
    def Rare(self, packs, arch_weights):
        """"Choose the rarest card for the player's archetype"""
        picks = []
        for i, pack in enumerate(packs):
            pref = self.pref[i]
            if pref == None and self.picks:
                pref = self.calc_archetype_pref(i)
                self.pref[i] = pref
                #pref = self.calc_archetype_pref(i) #change
            #print(pref, i)
            if pref == None:
                pick = None
                for card in pack:
                    if pick == None or self.compare_rarity(pick, card):
                        pick = card
                #print(i) #0-7
                picks.append(pick)
                #print(len(picks[i]))
                pack.remove(pick)
                #i += 1
            else: 
                pick = None
                best_overlap = -1
                for card in pack:
                    card_color = card["colorIdentity"]
                    overlap = set(card_color) & set(pref)
                    #if i == 0:
                    #    print(len(overlap), pref)
                    if len(card_color) == 0 or len(overlap)/len(pref) == 1: #change
                        if best_overlap < 1:
                            pick = card
                            best_overlap = 1
                        elif pick == None or self.compare_rarity(pick, card):
                            pick = card
                            best_overlap = 1
                    else:
                        if pick == None:
                            pick = card
                            best_overlap = len(overlap)/len(card_color)
                        elif len(overlap)/len(card_color) > best_overlap:
                            pick = card
                            best_overlap = len(overlap)/len(card_color)
                        elif len(overlap)/len(card_color) == best_overlap:
                            if self.compare_rarity(pick, card):
                                pick = card
                #print(i)
                #print(picks[i])
                picks.append(pick)
                pack.remove(pick)
                #if i == 0:
                #    print(pick["name"])
                #i += 1
        #self.update_arch_weights(picks)
        #print("RARES:", end= " ")
        #print([card['name'] for card in picks])
        self.picks.append(picks)
        return packs, picks
    
    def WeightedvsRare(self, packs, arch_weights):
        """Make weighted pick for 1 player and use rare picker for the rest"""
        picks = []
        for i, pack in enumerate(packs):
            if i == 0:
                picks.append(self.Weighted(pack))
            else:
                pref = self.pref[i]
                if pref == None and self.picks:
                    pref = self.calc_archetype_pref(i)
                    self.pref[i] = pref
                    #pref = self.calc_archetype_pref(i) #change
                #print(pref, i)
                if pref == None:
                    pick = None
                    for card in pack:
                        if pick == None or self.compare_rarity(pick, card):
                            pick = card
                    #print(i) #0-7
                    picks.append(pick)
                    #print(len(picks[i]))
                    pack.remove(pick)
                    #i += 1
                else: 
                    pick = None
                    best_overlap = -1
                    for card in pack:
                        card_color = card["colorIdentity"]
                        overlap = set(card_color) & set(pref)
                        #if i == 0:
                        #    print(len(overlap), pref)
                        if len(card_color) == 0 or len(overlap)/len(pref) == 1: #change
                            if best_overlap < 1:
                                pick = card
                                best_overlap = 1
                            elif pick == None or self.compare_rarity(pick, card):
                                pick = card
                                best_overlap = 1
                        else:
                            if pick == None:
                                pick = card
                                best_overlap = len(overlap)/len(card_color)
                            elif len(overlap)/len(card_color) > best_overlap:
                                pick = card
                                best_overlap = len(overlap)/len(card_color)
                            elif len(overlap)/len(card_color) == best_overlap:
                                if self.compare_rarity(pick, card):
                                    pick = card
                    #print(i)
                    #print(picks[i])
                    picks.append(pick)
                    pack.remove(pick)
                    #if i == 0:
                    #    print(pick["name"])
                    #i += 1
            #self.update_arch_weights(picks)
            #print("RARES:", end= " ")
            #print([card['name'] for card in picks])
        self.picks.append(picks)
        return packs, picks
    
    def WeightedvsWeighted(self, packs, arch_weights): 
        """Make weighted pick for all players"""
        picks = []
        for i, pack in enumerate(packs):
            picks.append(self.Weighted(pack))
        self.picks.append(picks)
        return packs, picks

    def Weighted(self, pack):
        """Make a weighted pick for 1 player""" 
        picks = []
        max_card = None
        arch_vals = {arch: 0 for arch in self.archetype_names}

        #calc pool weights (archetype preference)
        for k, row in enumerate(self.picks):
            #print(k)
            #print(len(self.picks))
            pick = row[0]
            #print(pick)
            arch_weight = self.weights[pick["name"]]
            for arch in self.archetype_names:
                arch_vals[arch] += arch_weight[arch]
        
        #print(arch_vals)
        
        #calc option weights
        
        max_val = 0
        for k, card in enumerate(pack):
            option_weights = [self.weights["bias"][key] * 
                              self.weights[card["name"]][key] * 
                              (1+arch_vals[key]) 
                              for key in self.weights[card["name"]]]
            #print(option_weights) #max_card = max in rows

            if max(option_weights) > max_val:
                max_card = card
                max_val = max(option_weights)
                #max_indices = [j for j, v in enumerate(option_weights) if v == max_val]  # Collect indices of all occurrences of max_value
                #max_val = self.archetype_names[random.choice(max_indices)]
                      
        pick = max_card 
        pack.remove(pick)
        return pick

    def calc_archetype_pref(self, drafter): 
        """"Determine archetype preference for Rare picker"""
        first_pick = self.picks[0][drafter]
        
        name = first_pick["name"]
        #print(name)
        arch_weight = self.weights[name]
        color = first_pick["colorIdentity"]
        if len(color) == 0:
            pref = random.choice(self.archetype_names)
            return pref
        list = []
        for arch in self.archetype_names:
            overlap = set(arch) & set(color)
            #print(overlap)
            #print(color)
            if len(overlap)/len(arch) == 1:
                pref = arch
                return pref
            elif len(overlap)/len(arch) == 0.5:
                list.append(arch)
        if list:
            pref = random.choice(list)  
            return pref
        pref = random.choice(self.archetype_names) 
        return pref
 
    
    def compare_rarity(self, previous_best, new_card):
        """Return true if new_card has better rarity than a previous card"""
        Rarities = {"common": 1, "uncommon": 2, "list": 3, "rare": 4, "mythic": 5}
        return Rarities.get(new_card["rarity"], 0) > Rarities.get(previous_best["rarity"], 0) 
    
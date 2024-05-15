import random

class Pack:
    def __init__(self, cards):
        self.cards = cards
        self.card_names = [card['name'] for card in cards]
        self.C, self.U, self.R, self.M, self.L = self.rarities(cards)
        self.n_cards = len(self.card_names)
      
    def rarities(self, cards):  
        """Sort all cards by their rarity"""
        rarities = {'common': [], 'uncommon': [], 'rare': [], 'mythic': [], 'list': []}
        for card in cards:
            rarity = card['rarity']
            if rarity in rarities:
                rarities[rarity].append(card)
            else:
                print("Rarity missing")
        return rarities['common'], rarities['uncommon'], rarities['rare'], rarities['mythic'], rarities['list']  
    
    def wildCard(self): 
        """can be anything but a list card"""
        wildcards_pool = ['common', 'uncommon', 'raremythic']
        wildcards = random.choices(wildcards_pool, k=2)
        return wildcards
    
    def listCard(self): 
        """87.5% chance to be common, otherwise a list card"""
        if random.random() < 0.875:
            listcard = 0
        else:
            listcard = 1
        return listcard

    def random_pack(self):
        """Create a pack of cards (play booster)."""
        n_commons = 6 
        n_uncommons = 3
        n_raremythics = 1
        wildcards = self.wildCard()
        listcard = self.listCard()
        if listcard == 0:
            n_commons = 7
        pack_unopened = {'common': n_commons, 'uncommon': n_uncommons, 'raremythic': n_raremythics, 'list': listcard}
        for card in wildcards:
            pack_unopened[card] += 1
            
        pack_opened = []
        for _ in range(pack_unopened["common"]):
            pack_opened.append(random.choice(self.C))
        for _ in range(pack_unopened["uncommon"]):
            pack_opened.append(random.choice(self.U))
        for _ in range(pack_unopened["raremythic"]):
            if random.random() < 1/7:
                pack_opened.append(random.choice(self.M))
            else:
                pack_opened.append(random.choice(self.R))
        for _ in range(pack_unopened["list"]):
            pack_opened.append(random.choice(self.L))
        return pack_opened

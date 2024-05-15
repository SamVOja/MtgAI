
class Draft:
    def __init__(self, card_values, picker, packs):
        self.archetype_names = ["WU", "WB", "WR", "WG", "UB", "UR", "UG", "BR", "BG", "RG"]  
        self.weights = card_values
        self.picker = picker
        self.packs = packs

        self.n_drafters = 8
        self.n_rounds = 3
        self.n_cards_in_pack = 13
        
        self.arch_weights = self.create_arch_weights()
        self.picks = []

    def pick(self, packs):
        """Each player makes a pick using the chosen picker method"""
        packs, picks = self.picker.picker(packs, self.arch_weights)
        self.picks.append(picks)
        self.update_arch_weights(picks)
        packs = self.pass_packs(packs)
        return packs
    
    def pass_packs(self, packs):
        """Each player gives the current pack they have to the next player"""
        last_element = packs[-1]
        for i in range(len(packs)-1, 0, -1):
            packs[i] = packs[i-1]
        packs[0] = last_element
        return packs
    
    def draft(self):
        """Operate the draft"""
        for _ in range(self.n_rounds): #3 pack
            packs = [self.packs.random_pack() for _ in range(self.n_drafters)]
            for _ in range(self.n_cards_in_pack): #13 picks (1 per call)
                packs = self.pick(packs)
        self.picker.picks.clear()
        #clear picks for next draft
        #self.picker.arch_weights.clear()
        
    def create_arch_weights(self):
        """Initialize archetype weights"""
        result_dict = {}
        for i in range(0, self.n_drafters):
            inner_dict = {}
            for arch in self.archetype_names:
                inner_dict[arch] = 0
            result_dict[i] = inner_dict
        return result_dict 
        
    def update_arch_weights(self, picks):
        """Update archetype weights based on the cards the players have selected"""
        for i in range(self.n_drafters): 
            drafter_pick = picks[i]["name"]
            pick_weights = self.weights[drafter_pick]
            #print(drafter_pick)
            for archetype, weight in pick_weights.items():
                #print(self.arch_weights[i].get(archetype, 0)* weight, i)
                current_weight = self.arch_weights[i].get(archetype, 0)
                updated_weight = current_weight * weight + 0.1
                self.arch_weights[i][archetype] = updated_weight
        



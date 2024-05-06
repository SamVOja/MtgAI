import json
import torch
    
class Model(torch.nn.Module): 
    def __init__(self, n_cards, random_initial):
        super().__init__() 
        self.colors = ["WU", "WB", "WR", "WG", "UB", "UR", "UG", "BR", "BG", "RG"]
        self.n_cards = n_cards
        self.n_archetypes = 10 
        self.relu = torch.nn.ReLU()
        self.linear = torch.nn.Linear(321, 10)
        self.linear.bias = torch.nn.Parameter(torch.tensor(1.0))
        
        if random_initial:
            self.weights = self.Random_Weights()
        else:
            self.weights = self.Initial_Weights()

    def Random_Weights(self): #Uniform distribution
        initial_weights = torch.nn.Parameter(torch.rand(self.n_cards, self.n_archetypes))
        return initial_weights  

    def Initial_Weights(self): #Weights defined by simple heuristics
        json_file_path = 'data/json/MKM_weights.json'
        with open(json_file_path, 'r') as file:
            data = json.load(file)
            archetype_names = list(data.keys())
            weights_list = []
            for archetype_name in archetype_names:
                archetype_weights = []
                for color_combination in self.colors:
                    weight = data[archetype_name][color_combination]
                    archetype_weights.append(weight)
                weights_list.append(archetype_weights)
            initial_weights = torch.FloatTensor(weights_list)
            initial_weights = torch.nn.Parameter(initial_weights)
            return initial_weights
    
    def forward(self, X):
        batch_size = X.shape[0]
        cards = X[:, :self.n_cards]
        pool = X[:, self.n_cards:self.n_cards*2]
        mana = X[:, self.n_cards*2:]
        
        Avg_Cost = torch.sum(pool * mana, dim=1)
        index = torch.arange(1, batch_size + 1, device=Avg_Cost.device).float()
        Avg_Cost /= index #avg mana of pool at every pick

        self.linear.weight = torch.nn.Parameter(self.weights.T)
        arch_bias = self.linear(pool)
        card_weights = (cards.view((batch_size, self.n_cards, 1)) * self.weights.reshape((1, self.n_cards, self.n_archetypes)))
        
        arch_bias_expanded = arch_bias.unsqueeze(1) # Shape [39, 1, 10]

        current_choice = torch.mul(arch_bias_expanded, card_weights).sum(dim=-1)
        current_choice = self.relu(current_choice)
        return current_choice
import json
import torch
import numpy as np
import torch.nn.functional as F
    
class Model(torch.nn.Module): 
    def __init__(self, n_cards, random_initial):
        super().__init__() 
        self.colors = ["WU", "WB", "WR", "WG", "UB", "UR", "UG", "BR", "BG", "RG"]
        self.n_cards = n_cards
        self.n_archetypes = 10 
        self.relu = torch.nn.ReLU()
        self.dropout = torch.nn.Dropout(p=0.3)
        self.linear = torch.nn.Linear(321, 10)

        self.linear.bias.data.fill_(0.5)
        
        if random_initial:
            self.weights = self.Random_Weights()
        else:
            self.weights = self.Initial_Weights()
            
        self.linear.weight = torch.nn.Parameter(self.weights.T) 
        
    def Random_Weights(self): 
        """Weights initialized as a Uniform distribution"""
        initial_weights = torch.nn.Parameter(torch.rand(self.n_cards, self.n_archetypes))
        return initial_weights  

    def Initial_Weights(self): 
        """Weights initialized by simple heuristics"""
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

        arch_bias = self.relu(self.linear(pool))
        
        card_weights = (cards.view((batch_size, self.n_cards, 1)) * self.weights.reshape((1, self.n_cards, self.n_archetypes)))
        #shape[39, 321, 10]
        
        arch_bias_expanded = arch_bias.unsqueeze(1) # Shape [39, 1, 10]

        current_choice = torch.mul(arch_bias_expanded, card_weights).sum(dim=-1)

        return F.relu(current_choice)
    
    def stable_non_zero_log_softmax(self, x):
        b = x.max(dim=1).values.view(-1, 1)
        stabalized_x = (x - b * x.sign())
        log_sum_exps = torch.log(torch.sum(x.sign() * torch.exp(stabalized_x), dim=1))
        log_probs = x.sign() * (stabalized_x - log_sum_exps.view(-1, 1))
        return log_probs

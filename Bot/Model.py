import json
import torch
import numpy as np
import torch.nn.functional as F
    
class Model(torch.nn.Module): 
    def __init__(self, n_cards, random_initial):
        super().__init__() 
        self.colors = ["WU", "WB", "WR", "WG", "UB", "UR", "UG", "BR", "BG", "RG"]
        self.n_cards = n_cards #321
        self.n_archetypes = 10 
        self.n_neurons = 128
        
        self.relu = torch.nn.ReLU()
        self.dropout = torch.nn.Dropout(p=0.3)

        self.hidden = torch.nn.Linear(self.n_cards, self.n_neurons)  
        self.output = torch.nn.Linear(self.n_neurons, self.n_archetypes)  

        if random_initial:
            self.weights = self.Random_Weights()
        else:
            self.weights = self.Initial_Weights()
            
        self.output.bias.data.fill_(0.5)
        
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
        Avg_Cost /= index #avg mana of pool at every pick, unused

        hidden_output = self.hidden(pool) 
        hidden_output = self.relu(hidden_output)
        hidden_output = self.dropout(hidden_output)
        
        arch_bias = self.output(hidden_output)
        arch_bias = self.relu(arch_bias)
        
        card_weights = (cards.view((batch_size, self.n_cards, 1)) * self.weights.reshape((1, self.n_cards, self.n_archetypes)))
        #shape[39, 321, 10]
        
        arch_bias_expanded = arch_bias.unsqueeze(1) # Shape [39, 1, 10]

        current_choice = torch.mul(arch_bias_expanded, card_weights).sum(dim=-1)

        return F.relu(current_choice)


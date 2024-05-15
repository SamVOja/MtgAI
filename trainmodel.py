import numpy as np
import pandas as pd
import json
import torch
import sqlite3
from torch.utils.data import TensorDataset, DataLoader
from Analyze.Analyze_training import TrainingPlotter
from Bot.Model import Model
from Bot.Trainer import Trainer


# FETCH DATA
db_path="data/sqlite/training.sqlite" 
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

packs = pd.read_sql_query("SELECT * FROM packs;", conn, index_col=['draft', 'drafter', 'pick_number'])
picks = pd.read_sql_query("SELECT * FROM picks;", conn, index_col=['draft', 'drafter', 'pick_number'])
pool = pd.read_sql_query("SELECT * FROM pool;", conn, index_col=['draft', 'drafter', 'pick_number'])
mana = pd.read_sql_query("SELECT * FROM mana;", conn) 

N_Cards = int(packs.shape[1]) 
N_Training= int(packs.shape[0] * 0.85)
N_Validation = int(packs.shape[0] * 0.15)
N_Testing = int(packs.shape[0] * 0.15)

#print(packs.shape[1])
#print(picks.shape[1])
#print(pool.shape[1])
#print(mana.shape[1])

X = pd.merge(packs, pool, left_index=True, right_index=True)
X = X.assign(cross_index=0)  
X = pd.merge(X, mana, how='cross') 
X = X.drop(columns=['cross_index'])
X.iloc[:, 0:N_Cards] = np.sign(X.iloc[:, 0:N_Cards])

#column_names = X.columns.tolist()
#cards_column_names = column_names[:N_Cards]
#pool_column_names = column_names[N_Cards:N_Cards*2]
#mana_column_names = column_names[N_Cards*2:]
#print("Column names for cards:", len(cards_column_names))
#print("Column names for pool:", len(pool_column_names))
#print("Column names for mana:", len(mana_column_names))

y = pd.Series(np.argmax(picks.values, axis=1), index=picks.index)
y_names = picks.columns

nb_samples = 50000 #10000
features = torch.randn(nb_samples, 10)
labels = torch.empty(nb_samples, dtype=torch.long).random_(10)
adjacency = torch.randn(nb_samples, 5)
laplacian = torch.randn(nb_samples, 7)

dataset = TensorDataset(features, labels, adjacency, laplacian)
loader = DataLoader(
    dataset,
    batch_size=39
)

train = TensorDataset(
    torch.from_numpy(X[:N_Training].values.astype(np.float32)),
    torch.from_numpy(y[:N_Training].values.astype(np.int64)))  
test = TensorDataset(
    torch.from_numpy(X[N_Training:].values.astype(np.float32)),
    torch.from_numpy(y[N_Training:].values.astype(np.int64)))  

train_batcher = DataLoader(train, batch_size=39) 
test_batcher = DataLoader(test, batch_size=39) 

#bot = Model(n_cards=N_Cards, random_initial=True)
bot = Model(n_cards=N_Cards, random_initial=False)

trainer = Trainer(n_epochs=100, learn_rate=0.005)
trainer.fit(bot, train_batcher, test_batcher)
  
print(bot.linear.bias)
print("TRAINING DONE")

file_path = 'data/json/MKM_learned_weights.json'
with open(file_path, 'w') as file:
    bias = bot.linear.bias.detach().numpy().tolist()
    sum_bias = sum(bias) 

    normalized_bias = [10*b / sum_bias for b in bias]
    weights = bot.weights.detach().numpy().tolist()
    colors = ["WU", "WB", "WR", "WG", "UB", "UR", "UG", "BR", "BG", "RG"]
    d = {
        "bias": {
            colors[i]: x for i, x in enumerate(normalized_bias)
        },
        **{cardnm: {
            colors[i]: x for i, x in enumerate(row)}
        for cardnm, row in zip(y_names, weights)}
        }
    json.dump(d, file, indent=4)

plotter = TrainingPlotter()
plotter.plot_loss(trainer)


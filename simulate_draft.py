from Simulate.Drafter import Draft 
from Simulate.Picker import Picker
from Simulate.Packs import Pack
from Analyze.Analyze_simulations import Plotter
import json

#n_drafts = 100000
n_drafts = int(input("Enter amount of drafts to simulate: ") or 1)
print("Simulating " + str(n_drafts) + " draft(s):")

cards_path='data/json/MKM_filtered.json'
winrates_path='data/json/MKM_winrate.json'

heuristic_values_path='data/json/MKM_weights.json'
learned_values_path='data/json/MKM_learned_weights.json'

cards = json.load(open(cards_path))
heuristic_values = json.load(open(heuristic_values_path))
#learned_values = json.load(open(learned_values_path))

pickerAi = Picker("WeightedvsRare", n_drafters=8, n_cards=len(cards), weights=heuristic_values)
#pickerAi = Picker("Weighted", n_drafters=8, n_cards=len(cards), weights=learned_values)
pickerRare = Picker("Rare", n_drafters=8, n_cards=len(cards), weights=heuristic_values)
pickerRandom = Picker("Random", n_drafters=8, n_cards=len(cards), weights=heuristic_values)

Randomdrafts = []
Raredrafts = []
Aidrafts = []
for i in range(n_drafts):
    pack = Pack(cards=cards) #use same packs with different pickers to compare
    draftRandom = Draft(card_values=heuristic_values, picker=pickerRandom, packs=pack)
    draftRare = Draft(card_values=heuristic_values, picker=pickerRare, packs=pack)
    draftAi = Draft(card_values=heuristic_values, picker=pickerAi, packs=pack)

    draftRandom.draft()
    draftRare.draft()
    draftAi.draft()
    
    Randomdrafts.append(draftRandom)
    Raredrafts.append(draftRare)
    Aidrafts.append(draftAi)  
print(str(n_drafts) + " Draft(s) complete.")

# PLOTTING
plotter = Plotter()

#plotter.plot_card_types(7, Randomdrafts) 
#plotter.plot_card_types(7, Raredrafts) 
#plotter.plot_card_types(7, Aidrafts) #drafters (0-7)=8, drafts

#plotter.plot_mana_curve(7, Randomdrafts)
#plotter.plot_mana_curve(7, Raredrafts)
#plotter.plot_mana_curve(7, Aidrafts)

plotter.plot_win_rates(8, Randomdrafts, winrates_path)
plotter.plot_win_rates(8, Raredrafts, winrates_path) 
plotter.plot_win_rates(1, Aidrafts, winrates_path) 

plotter.plot_arch_preference(Aidrafts) 
#print([row[0]["name"] for row in Aidrafts[0].picks])

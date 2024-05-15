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
learned_values = json.load(open(learned_values_path))

pickerAivsAi = Picker("WeightedvsWeighted", n_drafters=8, n_cards=len(cards), weights=learned_values)
pickerAi = Picker("WeightedvsRare", n_drafters=8, n_cards=len(cards), weights=learned_values)
pickerRare = Picker("Rare", n_drafters=8, n_cards=len(cards), weights=heuristic_values)
pickerRandom = Picker("Random", n_drafters=8, n_cards=len(cards), weights=None)

Randomdrafts = []
Raredrafts = []
Aidrafts = []
AivsAidrafts = []
for i in range(n_drafts):
    pack = Pack(cards=cards) #use same packs with different pickers to compare
    draftRandom = Draft(card_values=heuristic_values, picker=pickerRandom, packs=pack)
    draftRare = Draft(card_values=heuristic_values, picker=pickerRare, packs=pack)
    draftAi = Draft(card_values=learned_values, picker=pickerAi, packs=pack)
    draftAivsAi = Draft(card_values=learned_values, picker=pickerAi, packs=pack)

    draftRandom.draft()
    draftRare.draft()
    draftAi.draft()
    draftAivsAi.draft()
    
    Randomdrafts.append(draftRandom)
    Raredrafts.append(draftRare)
    Aidrafts.append(draftAi) 
    AivsAidrafts.append(draftAivsAi)  
print(str(n_drafts) + " Draft(s) complete.")

# PLOTTING
plotter = Plotter()

#plotter.plot_mana_curve(8, Randomdrafts)
#plotter.plot_mana_curve(8, Raredrafts)
#plotter.plot_mana_curve(8, Aidrafts)

plotter.calc_win_rates(8, Randomdrafts, winrates_path)
plotter.calc_win_rates(8, Raredrafts, winrates_path) 
plotter.calc_win_rates(8, AivsAidrafts, winrates_path) 
plotter.calc_win_rates(1, Aidrafts, winrates_path) 

plotter.plot_arch_preference(Aidrafts) 
plotter.plot_arch_preference(AivsAidrafts) 

#print([row[0]["name"] for row in Aidrafts[0].picks])

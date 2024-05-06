import matplotlib.pyplot as plt
import csv
import json

def calculate_card_playrate(csv_file_path):
    column_sums = {}
    with open(csv_file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        deck_columns = [col for col in reader.fieldnames if col.startswith("deck_")]

        for row in reader:
            for col in deck_columns:
                value = int(row[col]) if row[col].isdigit() else 0
                if value > 0:
                    column_sums[col.replace("deck_", "")] = column_sums.get(col.replace("deck_", ""), 0) + value
        
        column_sums = dict(sorted(column_sums.items(), key=lambda item: item[1], reverse=True))
    return column_sums

def calculate_player_winrate(csv_file_path):

    with open(csv_file_path, 'r') as csvfile:
        data = csv.DictReader(csvfile)
        col = data.fieldnames[17]
        wins = 0
        total_games = 0
        
        for row in data:
            total_games += 1
            wins += 1 if row[col] == "True" else 0

        winrate = wins / total_games * 100

    return total_games, wins, winrate

def calculate_card_winrate(csv_file_path):
    played_sums = {}
    win_sums = {}
    winrate = {}
    with open(csv_file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        
        drawn_columns = [col for col in reader.fieldnames if col.startswith("drawn_")]
        opening_columns = [col for col in reader.fieldnames if col.startswith("opening_hand_")]
        tutored_columns = [col for col in reader.fieldnames if col.startswith("tutored_")]
        
        for row in reader:
            for drawn_col, opening_col, tutored_col in zip(drawn_columns, opening_columns, tutored_columns):
                drawn_value = int(row[drawn_col]) if row[drawn_col] else 0
                opening_value = int(row[opening_col]) if row[opening_col] else 0
                tutored_value = int(row[tutored_col]) if row[tutored_col] else 0
                
                sum_value = drawn_value + opening_value + tutored_value
                played_sums.setdefault(drawn_col, 0)
                played_sums[drawn_col] += sum_value  
                
                win_sums.setdefault(drawn_col, 0)
                if str(row["won"]) == "True":
                    win_sums[drawn_col] += sum_value
        for drawn_col in drawn_columns:
            print(win_sums[drawn_col])
            print(played_sums[drawn_col])
            winrate.setdefault(drawn_col.replace("drawn_", ""), 0)
            if played_sums[drawn_col] != 0:
                winrate[drawn_col.replace("drawn_", "")]  = win_sums[drawn_col]/played_sums[drawn_col]        
    return winrate

def plot_cards(column_sums):
    first_five = dict(list(column_sums.items())[:5])
    remaining = dict(list(column_sums.items())[5:105])

    # Plot Basic Lands separately
    plt.figure(figsize=(20, 8))
    plt.bar(first_five.keys(), first_five.values(), color='skyblue')
    plt.xlabel('Basic land name')
    plt.ylabel('Amount of the card in decks')
    plt.title('')
    plt.xticks(rotation=45, fontsize=10)
    plt.tight_layout()
    plt.show()

    # Plot the remaining cards
    plt.figure(figsize=(50, 8))
    plt.bar(remaining.keys(), remaining.values(), color='skyblue', width=0.8)
    plt.xlabel('Card')
    plt.ylabel('Amount of the card in decks')
    plt.title('')
    plt.xlim(-0.5, len(remaining.keys()) - 0.5)  
    plt.xticks(rotation=45, fontsize=6, ha='right')
    plt.xticks(range(len(remaining.keys())), remaining.keys())  
    plt.gca().xaxis.set_major_locator(plt.MultipleLocator(1))
    plt.tight_layout()
    plt.show()
    
def save_winrate_to_json(winrate, json_file_path):
    with open(json_file_path, 'w') as jsonfile:
        json.dump(winrate, jsonfile)
        
def plot_winrate(winrate):
    plt.figure(figsize=(20, 8))
    plt.bar(winrate.keys(), winrate.values(), color='skyblue')
    plt.xlabel('Card name')
    plt.ylabel('Winrate if in hand')
    plt.title('')
    plt.xticks(rotation=45, fontsize=10)
    plt.tight_layout()
    plt.show()


csv_file_path = 'data/csv/game_data_public.MKM.PremierDraft.csv'
winrate = calculate_card_winrate(csv_file_path)
json_file_path = 'data/json/MKM_winrate.json'
save_winrate_to_json(winrate, json_file_path) 
total_games, value, winrate = calculate_player_winrate(csv_file_path)

print("Total Games:", total_games)
print("Wins:", value)
print("Victory Rate: {:.2f}%".format(winrate))

#playrate = calculate_card_playrate(csv_file_path)
#plot_cards(playrate) 











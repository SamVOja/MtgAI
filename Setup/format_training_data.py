import csv
import sqlite3
import json

color_pairs = ["WU", "WB", "WR", "WG", "UB", "UR", "UG", "BR", "BG", "RG"]
items_to_remove = ["Island", "Swamp", "Mountain", "Forest", "Plains"]

def create_table(cursor, csv_file, json_file): 
    tables = ['packs', 'picks', 'pool']
    with open(json_file, 'rb') as f:
        cards = json.load(f)
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        fieldnames = reader.fieldnames
        for table in tables:
            sql_create_tables = f'CREATE TABLE IF NOT EXISTS {table} (' + \
                            'draft TEXT, ' + \
                            'drafter TEXT, ' + \
                            'pick_number INTEGER, ' + \
                            ', '.join([f'"{key.replace("pack_card_", "")}" INTEGER' for key in fieldnames if key.startswith('pack_card_') and key[10:] not in items_to_remove]) + \
                            ')'
            cursor.execute(sql_create_tables)
        sql_create_mana = f'CREATE TABLE IF NOT EXISTS mana (' + \
                ', '.join([f'"{key.replace("pack_card_", "")}" INTEGER' for key in fieldnames if key.startswith('pack_card_') and key[10:] not in items_to_remove]) + \
                ')'
        cursor.execute(sql_create_mana)
        column_names = [f'"{card["name"]}"' for card in cards]
        converted_mana_costs = [card['convertedManaCost'] for card in cards]
        insert_query = f'INSERT INTO mana ({", ".join(column_names)}) VALUES ({", ".join("?" for _ in column_names)})'
        cursor.execute(insert_query, converted_mana_costs)
        
def insert_data_row(i, row, drafter, pack_columns, pool_columns):
    #i // 39
    pack_number = int(row['pack_number']) #pack_number #0-2
    pick_number = int(row['pick_number'])+(pack_number*13) #0-38

    pack_values = [int(row[col]) for col in pack_columns]
    pool_values = [int(row[col]) for col in pool_columns]

    pick = row['pick']
    pick_values = [0] * len(pack_columns)
    pick_index = pool_columns.index("pool_" + pick)
    pick_values[pick_index] = 1
         
    draft = row['draft_id']

    placeholders = ','.join(['?' for _ in range(len(pack_columns) + 3)])
    insert_query = f"INSERT INTO packs VALUES ({placeholders});"
    cursor.execute(insert_query, tuple([draft, drafter, pick_number] + pack_values))
    
    insert_query = f"INSERT INTO picks VALUES ({placeholders});"
    cursor.execute(insert_query, tuple([draft, drafter, pick_number] + pick_values))
                
    insert_query = f"INSERT INTO pool VALUES ({placeholders});"
    cursor.execute(insert_query, tuple([draft, drafter, pick_number] + pool_values))
                
    return i + 1

def validate_data(reader, skipped_lines): 
    dict = []
    for i in range(1, 40):
        row = next(reader)
        if int(row["pick_number"])+13*int(row["pack_number"]) != i-1:
            dict.clear
            skipped_lines += i
            if i > 1:
                skipped_lines += 1
            return validate_data(reader, skipped_lines)
        else:
            dict.append(row)
    return dict, skipped_lines

def insert_n_data(csv_file, n_drafter):
    print("INSERTING DATA FROM " + str(n_drafter) + " PLAYERS")
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        pack_columns = [col for col in reader.fieldnames if col.startswith("pack_card_") and col[10:] not in items_to_remove]
        pool_columns = [col for col in reader.fieldnames if col.startswith("pool_") and col[5:] not in items_to_remove]
        total_skipped_lines = 0
        for drafter in range(n_drafter):
            skipped_lines = 0
            dict, skipped_lines = validate_data(reader, skipped_lines)
            total_skipped_lines += skipped_lines
            i = 39*drafter+total_skipped_lines
            for row in dict:
                i = insert_data_row(i, row, drafter, pack_columns, pool_columns)
    print(total_skipped_lines)

n_drafters = int(input("Enter amount of played drafts to use for training: ") or 20000)
csv_file = "data/csv/draft_data_public.MKM.PremierDraft.csv"
db_file = "data/sqlite/training.sqlite"
json_file = "data/json/MKM_filtered.json"
conn = sqlite3.connect(db_file)
cursor = conn.cursor()

create_table(cursor, csv_file, json_file)

insert_n_data(csv_file, n_drafters) 

conn.commit()
conn.close()
print("DATA INSERTED.")

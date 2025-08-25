import json

def read_taboo_words():
    try:
        with open('taboo_words.json', 'r', encoding='utf-8') as file:
            taboo_cards = json.load(file)
        return taboo_cards
    except FileNotFoundError:
        raise FileNotFoundError("Error: taboo_words.json not found.")
    except json.JSONDecodeError:
        raise ValueError("Error: Could not decode taboo_words.json. Please check the file format.")
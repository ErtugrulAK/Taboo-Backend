def read_taboo_words():
    taboo_cards = {}
    try:
        with open('taboo_words.txt', 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                words = line.split()
                main_word = words[0]
                taboos = words[1:6]
                taboo_cards[main_word] = taboos
        return taboo_cards
    except FileNotFoundError:
        exit()

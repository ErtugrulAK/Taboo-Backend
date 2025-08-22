import json
import re
from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()

def normalize_word(word):
    word = word.lower()
    lemma_noun = lemmatizer.lemmatize(word, pos='n')
    lemma_verb = lemmatizer.lemmatize(word, pos='v')
    return set([lemma_noun, lemma_verb])

def check_description(taboo_dict: dict, target_word: str, description: str) -> str:
    taboo_words = taboo_dict.get(target_word, [])
    description_words = re.findall(r'\b\w+\b', description.lower())

    description_lemmas = set()
    for w in description_words:
        description_lemmas.update(normalize_word(w))

    used_taboo_words = []

    for taboo_word in taboo_words:
        taboo_lemmas = normalize_word(taboo_word)
        if taboo_lemmas.intersection(description_lemmas):
            used_taboo_words.append(taboo_word)

    isvalid = len(used_taboo_words) == 0

    result = {
        "isvalid": isvalid,
        "used_taboo_words": used_taboo_words
    }

    return json.dumps(result, ensure_ascii=False, indent=2)

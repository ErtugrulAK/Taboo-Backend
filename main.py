import random
import json
from read_file import read_taboo_words
from ai_guesser import guess_object
from ai_moderator import check_description

def main():
    taboo_dict = read_taboo_words()
    temp_taboo_dict = {k: v.copy() for k, v in taboo_dict.items()}

    print("=== TABOO ===")

    while True:
        target_word = random.choice(list(temp_taboo_dict.keys()))
        print(f"\nYour word is: {target_word}")

        description = input("Enter your description: ").strip()
        if description.lower() == "quit":
            break

        result_json = check_description(temp_taboo_dict, target_word, description)
        result = json.loads(result_json)
        if not result["isvalid"]:
            print(f"Warning! You used taboo words: {', '.join(result['used_taboo_words'])}")
            continue

        combined_description = description

        while True:
            guess = guess_object(combined_description)
            print(f"Guess: {guess}")

            guesses = [g.strip().lower() for g in guess.split(",")]
            for g in guesses:
                if g in temp_taboo_dict[target_word]:
                    temp_taboo_dict[target_word].remove(g)

            correct = input("Is the guess correct? (true/false): ").strip().lower()
            if correct == "true":
                break
            elif correct == "false":
                extra_desc = input("Enter additional description: ").strip()
                combined_description += " " + extra_desc

if __name__ == "__main__":
    main()

import sqlite3
from random import choice

def main():
    connection = sqlite3.connect("database.db")
    cur = connection.cursor()

    while True:
        length_input = input("Gib die Länge des gesuchten Wortes ein oder 'EXIT' zum Beenden: ")

        if length_input.lower() == 'exit':
            print("Machs gut! Das Spiel wird beendet.")
            break

        try:
            length = int(length_input)
        except ValueError:
            print("Ungültige Eingabe. Bitte gib eine ganze Zahl ein oder 'EXIT' zum Beenden.")
            continue

        cur.execute("SELECT word FROM words WHERE letters = ?", (length,))
        words_of_length = cur.fetchall()

        if not words_of_length:
            print(f"Keine Wörter mit der Länge {length} gefunden. Versuche es erneut.")
            continue

        selected_word = choice(words_of_length)
        guessed_part = ['_'] * length
        attempts = 5

        while attempts > 0:
            guess = input("Gib einen Buchstaben ein: ").upper()

            if guess in selected_word[0]:
                print("Richtig!")
                for i, letter in enumerate(selected_word[0]):
                    if letter == guess:
                        guessed_part[i] = guess
                print("Aktueller Fortschritt:", ' '.join(guessed_part))
            else:
                attempts -= 1
                print(f"Das war leider falsch! Streng dich mehr an! Du hast nur noch {attempts} Versuche übrig.")

            if ''.join(guessed_part) == selected_word[0]:
                print("Na also! Du hast das Wort erraten.")
                break

        if attempts == 0:
            print(f"OK, lassen wir das... Das richtige Wort wäre '{selected_word[0]}' gewesen.")

if __name__ == "__main__":
    main()

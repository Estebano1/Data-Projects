import sqlite3

def add_word_to_database(word):
    connection = sqlite3.connect("database.db")
    cur = connection.cursor()

    word = word.upper()

    letters_count = len(word)

    cur.execute("INSERT INTO words (word, letters) VALUES (?, ?)", (word, letters_count))

    connection.commit()
    connection.close()

def main():
    while True:
        new_word = input("Gib das neue Wort ein oder 'exit' zum Beenden: ")

        if new_word.lower() == 'exit':
            print("Auf Wiedersehen! Das Programm wird beendet.")
            break

        add_word_to_database(new_word)

        print(f"Das Wort '{new_word.upper()}' wurde hinzugefügt.")

if __name__ == "__main__":
    main()

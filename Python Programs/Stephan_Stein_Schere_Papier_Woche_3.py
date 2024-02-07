#!/usr/bin/env python
# coding: utf-8

# In[68]:


from random import randint

punkte_human = 0  
punkte_comp = 0
    

while True:
    print("""
    Ich möchte wählen:
    1. Stein   (1)
    2. Schere  (2)
    3. Papier  (3)
    4. Beenden (4)
    """)

    human = int(input("Bitte gib die Nummer deiner Auswahl ein: "))

    computer = randint(1,3)

    ausgabe = (human,computer)

    

    if human == 4:
        print("Das Spiel wurde beendet")
        break
        
    if ausgabe == (1,1):
        print()
        print("Du und der Computer habt Stein gewählt!")
        print()
        print("Unentschieden")
        print()
    if ausgabe == (1,2):
        print()
        punkte_human = punkte_human + 1  
        punkte_comp = punkte_comp + 0
        print()
        print("Du hast Stein gewählt!")
        print("Der Computer hat Schere gewählt!")
        print()
        print("Stein macht die Schere stumpf!")
        print()
        print("Du gewinnst!")
        print()
    if ausgabe == (1,3):
        print()
        punkte_human = punkte_human + 0  
        punkte_comp = punkte_comp + 1
        print()
        print("Du hast Stein gewählt!")
        print("Der Computer hat Papier gewählt!")
        print()
        print("Papier wickelt den Stein ein!")
        print()
        print("Der Computer gewinnt!")
        print()
    if ausgabe == (2,2):
        print()
        print("Du und der Computer habt Schere gewählt!")
        print()
        print("Unentschieden")
        print()
    if ausgabe == (2,1):
        print()
        punkte_human = punkte_human + 0  
        punkte_comp = punkte_comp + 1
        print()
        print("Du hast Schere gewählt!")
        print("Der Computer hat Stein gewählt!")
        print()
        print("Stein macht die Schere stumpf!")
        print()
        print("Der Computer gewinnt!")
        print()
    if ausgabe == (2,3):
        print()
        punkte_human = punkte_human + 1  
        punkte_comp = punkte_comp + 0
        print()
        print("Du hast Schere gewählt!")
        print("Der Computer hat Papier gewählt!")
        print()
        print("Schere schneidet das Papier!")
        print()
        print("Du gewinnst!")
        print()
    if ausgabe == (3,3):
        print()
        print("Du und der Computer habt Papier gewählt!")
        print()
        print("Unentschieden")
        print()
    if ausgabe == (3,1):
        print()
        punkte_human = punkte_human + 1  
        punkte_comp = punkte_comp + 0
        print()
        print("Du hast Papier gewählt!")
        print("Der Computer hat Stein gewählt!")
        print()
        print("Papier wickelt den Stein ein!")
        print()
        print("Du gewinnst!")
        print()
    if ausgabe == (3,2):
        print()
        punkte_human = punkte_human + 0  
        punkte_comp = punkte_comp + 1
        print()
        print("Du hast Papier gewählt!")
        print("Der Computer hat Schere gewählt!")
        print()
        print("Schere schneidet das Papier!")
        print()
        print("Der Computer gewinnt!")
        print()


 
    print("---------------------------------------")
    print()
    print("Zwischenstand:")
    print("Punkte (Du) ",(punkte_human))
    print("Punkte (Comp) ",(punkte_comp))
    print()
    print("---------------------------------------")






# In[ ]:





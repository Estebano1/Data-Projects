#!/usr/bin/env python
# coding: utf-8

# In[94]:


def verschiebung(textfeld, anzahl_verschiebung):
    for jeder_buchstabe in textfeld:
        buchstabe_zahl = ord(jeder_buchstabe) 
        if buchstabe_zahl in range(97,123):
            verschobene_buchstabe_zahl = buchstabe_zahl + anzahl_verschiebung
            if verschobene_buchstabe_zahl > 122:
                verschobene_buchstabe_zahl = verschobene_buchstabe_zahl - 26
            ausgabe = chr(verschobene_buchstabe_zahl)
            
            
        else:
            ausgabe = chr(buchstabe_zahl)
        print(ausgabe, end="")
            
            


# In[ ]:


textfeld = input("Bitte gib einen Text ein ")

anzahl_verschiebung = int(input("Um welche Anzahl Buchstaben soll der Text verschoben werden? "))

textfeld = textfeld.lower()

verschiebung(textfeld, anzahl_verschiebung)


# In[ ]:





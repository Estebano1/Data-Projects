#!/usr/bin/env python
# coding: utf-8

# In[ ]:


while True:

#Begrüßung


    print("Servus, i bins, dei Taschenrechner")
    print("Wollen mia beide ned moi wos zam rechnen? ")
    print("ich ko scho mid +, -, *, /, **, //, % rechnen.")
    print("Kommen mia probieren es moi aus..")
    print()
    print()
    print()
    print()
# Eingaben

    zahl_1=int(input("Tippe a Zoi a "))
    operator=input("Wos wuist du damit doa? ")
    zahl_2=int(input("Tippe a zwoate Zoi a "))

# Berechnungen
   
        
    if operator == "+":
        result = f"Des Eagbnis da Addition vo {zahl_1} und {zahl_2} is {zahl_1 + zahl_2}"
    elif operator == "-":
        result = f"Des Eagbnis da Subtraktion vo {zahl_1} und {zahl_2} is {zahl_1 - zahl_2}"
    elif operator == "*":
        result = f"Des Eagbnis da Multipikation vo {zahl_1} und {zahl_2} is {zahl_1 * zahl_2}"
    elif operator == "/":
        if zahl_2 == 0:
            result = "Division duach Nui is ned ealaubt."
        else:
            result = f"Des Eagbnis da Division vo {zahl_1} und {zahl_2} is {zahl_1 / zahl_2}"
    elif operator == "//":
        if zahl_2 == 0:
            result = "Division duach Nui is ned ealaubt."
        else:
            result = f"Des Eagbnis da ganzzählign Division vo {zahl_1} und {zahl_2} is {zahl_1 // zahl_2}"
    elif operator == "**":
        result = f"Des Eagbnis da Potenzierung vo {zahl_1} mid {zahl_2} is {zahl_1 ** zahl_2}"
    elif operator == "%":
        result = f"Des Eagbnis da Modulodivision vo {zahl_1} und {zahl_2} is {zahl_1 % zahl_2}"
    else:
        result = "Ungültiga Operatoa."
        
        
  
    print("----------------------------------------------")
    print()
    print()
    print(result)
    print()
    print()
    print("==============================================")
    print("==============================================")
    print("==============================================")
    print()
    print()


# In[ ]:





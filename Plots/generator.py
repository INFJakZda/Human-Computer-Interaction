#!/usr/bin/python3

import statistics
import matplotlib.pyplot as plt
import csv

def main():
    names = ['rsel.csv','cel-rs.csv', '2cel-rs.csv', 'cel.csv', '2cel.csv']     #pomocnicza lista nazw plikow z danymi
    plots = plt.figure(figsize=(9, 6.7))                                        #ustawienie rozmiaru obrazka
    lower = plots.add_subplot(121)                                              #ustawienie dwoch obrazkow obok siebie
    #PLOT
    for name in names:                  #dla każdej nazwy pliku
        flag = 0                        #pomijanie pierwszej linijki w csv
        osX = []                        #wartosci na osi X
        osY = []                        #wartosci na osi Y
        suma = []                       #pomocnicza lista dla osY     
        with open("data/" + name, 'r') as plik:           #otwieranie kazdego pliku z danymi
            dane = csv.reader(plik)             #czytanie konkretnego pliku
            for row in dane:                    #rozkladanie danych wiersz po wierszu
                if flag == 0:                   #pomijanie pierwszej linijki w csv - niepotrzebne nazwy kolumn
                    flag = 1                    #otwarcie bramy po minięciu pierwszego wiersza w pliku
                    continue                    #przejscie do drugiego wiersza 
                osX.append(int(row[1]) / 1000)  #druga kolumna( [1] ) to os X, odpowiednio przeskalowana
                for i in range(2,34):           #odczytanie wszytskich wartosci w wierszu
                    suma.append(float(row[i]))  #do pomocniczej listy dodajemy kolejne wartosci  
                osY.append(statistics.mean(suma) * 100)     #aby teraz policzyc jej srednia i wpisac do osi Y
                suma = []                       #czyszczenie pomocniczej listy
            #dodanie osi X, Y,   nazwy lini,        koloru        znacznikow  rozmiaru      
        if name == 'rsel.csv':
            lower.plot(osX, osY, label="1-Evol-RS", color='blue', marker='o', markersize=7, markevery=25)
        if name == 'cel-rs.csv':
            lower.plot(osX, osY, label="1-Coev-RS", color='green', marker='v', markersize=7, markevery=25)      
        if name == '2cel-rs.csv':  
            lower.plot(osX, osY, label="2-Coev-RS", color='red', marker='D', markersize=7, markevery=25)  
        if name == 'cel.csv':      
            lower.plot(osX, osY, label="1-Coev", color='black',marker='s', markersize=7, markevery=25)        
        if name == '2cel.csv':
            lower.plot(osX, osY, label="2-Coev", color='magenta', marker='d', markersize=7, markevery=25)  
    #ustawienie parametrow              
    lower.set_xlabel("Rozegranych gier (x1000)")
    lower.set_ylabel("Odsetek wygranych gier [%]")
    lower.set_xlim(0, 500)

    top = plt.twiny()
    top.set_xlim(0, 200)
    top.set_xticks([0, 100, 200, 300, 400, 500])
    top.set_xticklabels(["0", "40", "80", "120", "160", "200"])
    top.set_xlabel("Pokolenie")

    lower.legend(loc=4)
    lower.grid()
    
    #BOX PLOT
    
        
    
    plt.savefig('out/myplot_5.0.pdf')
    plt.close()

if __name__ == '__main__':
    main()

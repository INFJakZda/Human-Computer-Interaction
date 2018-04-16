#!/usr/bin/python3

import statistics
import matplotlib.pyplot as plt
import csv

def main():
    names = ['rsel.csv','cel-rs.csv', '2cel-rs.csv', 'cel.csv', '2cel.csv'] 
    plt.figure(figsize=(6.7, 6.7)) 
    for name in names:          #dla każdej nazwy pliku
        flag = 0                #pomijanie pierwszej linijki w csv
        osX = []
        osY = []
        suma = []               #pomocnicza lista dla osY     
        with open("data/" + name, 'r') as plik:
            dane = csv.reader(plik)
            for row in dane:
                if flag == 0:   #pomijanie pierwszej linijki w csv
                    flag = 1
                    continue
                osX.append(int(row[1]))  #druga kolumna to os X
                for i in range(2,34):   
                    suma.append(float(row[i]))            
                osY.append(statistics.mean(suma))
                suma = []    
        plt.plot(osX, osY)   
        plt.legend(names)   
    plt.xlabel("Rozegranych gier")
    plt.ylabel("Odsetek wygranych gier")
    plt.savefig('out/myplot_3.0.pdf')
    plt.close()

if __name__ == '__main__':
    main()

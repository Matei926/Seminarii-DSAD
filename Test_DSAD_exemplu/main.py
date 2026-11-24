import numpy as np
import pandas as pd #biblioteca de tabele

def calcul_medie_ponderata(t:pd.DataFrame):
    x=t.values
    mp = np.average(x[:,:-1],axis=0,weights=x[:,-1])
    return pd.Series(mp,t.columns[:-1])


firme = pd.read_csv("data_in/I2014.csv",index_col=0) #index_col=0 face
#ca prima coloana sa fie "numele" tabelelor
indicatori = list(firme.columns)[1:] #salveaza listele coloanelor
# fara prima - index=0 e deja numele randurilor

#print(indicatori)
#print(firme)

#Cerinta 1
firme_sal=firme[firme["NrSal"]>0] #filtrare dupa coloana "NrSal"
raport=firme_sal.apply(func=lambda x: x["TotalCifraAfaceri"]/x["NrSal"],axis=1)
#aplica o formula pe fiecare rand -> axis=1 == pe randuri
#x e randul curent
#lambda x == o functie de o linie pe randul x
cerinta1=pd.DataFrame({"DenLocalitate":firme_sal["DenLocalitate"],"Raport CA/NrSal":raport})
cerinta1.sort_values(by="Raport CA/NrSal",ascending=False).round(3).to_csv("data_out/Output1.csv")


# Să se calculeze rata ocupării populației ca număr de salariați la 1000 locuitori pentru 
# fiecare județ. Datele vor fi salvate în ordinea descrescătoare a ratei, în fișierul Output2.csv. 
# Pentru fiecare județ se va afișa indicativul de județ și rata ocupării. 

#Cerinta 2
populatie = pd.read_csv("data_in/PopulatieLocalitati.csv",index_col=0)
#lipeste tabelele unul langa altul, potrivind randurile cu aceeasi Siruta
#left_index si right_index potriveste tabelele dupa index
firme_loc=firme.merge(populatie,left_index=True,right_index=True)
#lipeste doua liste, cea care contine indicatorii + Pop + Jud
#se grupeaza dupa Judet si se face suma tuturor valorilor
firme_judet=firme_loc[indicatori+["Populatie","Judet"]].groupby(by="Judet").sum()
cerinta2=firme_judet.apply(func=lambda x: x["NrSal"]*1000/x["Populatie"],axis=1)
#print(firme_judet)
#Rezultatul are o singura coloana, o serie, deci ii dam numele cerut in subiect
cerinta2.name = "Rata Ocuparii"
cerinta2.sort_values(ascending=False).to_csv("data_out/Output2.csv")


# Să se determine pentru fiecare județ localitatea cu cel mai mare profit pe locuitor și 
# să se salveze în fișierul Output3.csv. Pentru fiecare județ se va salva indicativul 
# de județ și denumirea localității cerute.

#Cerinta 3 
firme_loc["Profit/loc"] = firme_loc["TotalProfit"]/firme_loc["Populatie"]
cerinta3 = firme_loc[["DenLocalitate","Profit/loc","Judet"]].groupby(by="Judet").apply(
    func= lambda x: x["DenLocalitate"].iloc[x["Profit/loc"].argmax()],
    include_groups=False
)
cerinta3.name="Localitate"
cerinta3.to_csv("data_out/Output3.csv")

# Să se calculeze valorile medii ale indicatorilor la nivel de județ 
# (media localităților din județ) și să se salveze în fișierul Output4.csv. 
# Se va calcula media ponderată, folosind ca pondere populația localităților. 
# Pentru fiecare județ se va afișa indicativul de județ și cele 5 medii.
#Cerinta 4
cerinta4 = firme_loc[indicatori+["Populatie","Judet"]].groupby(by="Judet").apply(
    func=calcul_medie_ponderata,
    include_groups=False
)
cerinta4.round(3).to_csv("data_out/Output4.csv")



import numpy as np
import sys
import copy
#
#Klasa resurs predstavlja izvor 'sredstava' koje se prosledjuju korisnicima. Resurs da bi se koristio mora da
#bude aktivan a sama aktivaciaj resursa kosta. Sredstava jednog resursa su ogranicena.
#Klasu resurs definisu sledeci atributi
#cenaAktivacije - cena koja je potrebno platiti da bi se koristio kapacitet ovog resurs
#dostupnostResursa - kolicina koja je preostala od ovog resursa i koja je dostupna dati drugim korisnicima
#ukupnoResurs - pocetna informacija o kapacitetu ovog resura
#
class Resurs:
    def __init__(self, cenaAktivacije, dostupnoResursa, resursAktiviran):
        self.cenaAktivacije = cenaAktivacije
        self.resursAktiviran = resursAktiviran
        self.dostupnoResursa = dostupnoResursa
        self.ukupnoResursa = dostupnoResursa
#
#Klasa koristik predstavlja potrazivaca resursa.
#Jedini atribut je upravo potraznaResursa koja predstavlja koliko sredstava joj je potrebno dodeliti od 
#jednog ili vise resursa
#
class Korisnik:
    def __init__(self, potraznjaResursa):
        self.potraznjaResursa = potraznjaResursa

#najboljeGrane - lista grana koje daju najbolju cenu.
#putanja - prolazak kroz sve moguce kombinacije, u trenutku najbolje kombinacije se prosledjuje u najboljeGrane
#najboljaCena - globalna promenljiva koja cuva informaciju o trenutnoj najboljoj ceni, za pocetak se postavlja
#               na inf kako bi prvi put sigurno bio manje cene

global najboljeGrane
global putanja
najboljaCena = float('inf')

#trenutnaCena predstavlja za trenutni put koliko kosta prenos resurasa
#indeksKorisnika predstavlja dubinu rekurzije. Fokus problema je da se potraznja korisnika zadovolji, tako da je sam
#algoritam zamisljen da se rotira oko korisnika.
#putanja je globalna promenljiva
def bnb(matricaCena, korisnici, resursi, indeksKorisnika, trenutnaCena, putanja = []):
    global najboljaCena
    global najboljeGrane
    #ako smo zadovoljili sve korisnike izlazimo iz rekurzije
    #postavljamo trenutnu cenu kao najbolju cenu ako su uslovi zadovoljeni
    #najboljeGrane se inicijalizuju trenutnom putanjom
    if indeksKorisnika == len(korisnici):
        if najboljaCena > trenutnaCena:
            najboljaCena = trenutnaCena
            najboljeGrane = copy.copy(putanja)
        return najboljaCena, najboljeGrane
    #prolazimo krez sve resurse koje jos uvek imaju sredstava na raspolaganju
    for indeksResursa in range(len(resursi)):
        if resursi[indeksResursa].dostupnoResursa > 0:
            dodatakCeni = 0
            sadAktiviran = False
            #ako resurs nije aktivan treba platiti cenu njegove aktivacije
            if (resursi[indeksResursa].resursAktiviran == False):
                sadAktiviran = True
                dodatakCeni += resursi[indeksResursa].cenaAktivacije
            #ako resurs moze da zadovolji celu potraznju korisnika, sve dajemo tom korisniku
            #ako resurs moze da zadovolji samo deo, onda korisniku dodeljujemo sve sto moze ali korisnik jos uvek  
            #nije zadovoljen
            #udeo je onoliko koliko zapravo prebacujemo od trenutnog resursa do trenutnog korisnika
            if (resursi[indeksResursa].dostupnoResursa < korisnici[indeksKorisnika].potraznjaResursa):
                #procenat = resursi[indeksResursa].dostupnoResursa / resursi[indeksResursa].ukupnoResursa
                #dajemo korisniku onliko koliko resurs ima sredstava
                udeo = resursi[indeksResursa].dostupnoResursa
            else:
                #procenat = korisnici[indeksKorisnika].potraznjaResursa / resursi[indeksResursa].ukupnoResursa
                #dajemo korisniku onoliko koliko trazi
                udeo = korisnici[indeksKorisnika].potraznjaResursa

            #dodatakCeni je za koliko se ukupna trenutna cena uvecava 
            dodatakCeni += udeo * matricaCena[indeksResursa][indeksKorisnika]

            # Ako bi trenutna cena postala veca od najbolje cene odsecamo tu granu
            # i ne menjamo trenutnu cenu.
            if trenutnaCena + dodatakCeni >= najboljaCena:
                continue
            #obelezavamo da je resurs aktivan kako bi sledecem koriscenju se ne bi ponovo placala cena aktivacije
            if sadAktiviran:
                resursi[indeksResursa].resursAktiviran = True

            #Novo stanje promenljivih. Umanjujemo dostupnost resursa i potraznju resursa za udeo 
            #trenutna cena se uvecava za dodatak jer je ovo resenje i dalje ima sansu da bude najbolje
            resursi[indeksResursa].dostupnoResursa -= udeo
            trenutnaCena += dodatakCeni
            korisnici[indeksKorisnika].potraznjaResursa -= udeo
            #ako je potraznja zadovoljena prelazimo na sledeceg, ako ne zadrzavamo se na trenutnom
            if korisnici[indeksKorisnika].potraznjaResursa > 0:
                noviIndeksKorisnika = indeksKorisnika
            else:
                noviIndeksKorisnika = indeksKorisnika + 1
            #prosirujemo putanju
            putanja.append('{} iz R{} za K{}'.format(udeo, indeksResursa, indeksKorisnika))
            
            #rekurzivni poziv sa novim vrednostima
            bnb(matricaCena, korisnici, resursi, noviIndeksKorisnika, trenutnaCena, putanja)
            
            putanja.pop();

            #Vracamo sve na staro stanje
            resursi[indeksResursa].dostupnoResursa += udeo
            trenutnaCena -= dodatakCeni
            korisnici[indeksKorisnika].potraznjaResursa += udeo
            #ako smo u ovoj iteraciji ukljucili resurs, kad sve vracamo na staro moramo da obelezimo da 
            #vise se ne vodi kao aktivan jer nije iskoriscen uopste i oduzeli smo cenu aktivacije iz trenutne cene
            if sadAktiviran:
                resursi[indeksResursa].resursAktiviran = False
                
    return najboljaCena, najboljeGrane

#resursi - lista inicijalizovanih objekata tipa Resurs
#korisnici - lista inicijalizovanih objekata tipa Korisnik
#matricaCena - indeksi redova predstavljaju resurs a kolone korisnike. matricaCena[i][j] i-ti resurs i j-ti
#              Cena ovde predstavlja koliko kosta dostaviti resurs korisniku. Cena se odnosi samo na jednu instancu.
#              Ako od i-tog resursa dostavljamo j-tom korisniku kolicinu od X tog resursa ukupna cena se racuna kao
#              matricaCena[i][j]*X. Primer, od resursa 1 do korisnika 3 cena po komadu je 3 i zelimo da posaljemo 
#              100, nasa cena je 3*100=300.

#resursi = [Resurs(1000, 500, False), Resurs(1000, 500, False), Resurs(1000, 500, False)]
#korisnici = [Korisnik(80), Korisnik(270), Korisnik(250), Korisnik(160), Korisnik(180)]
#matricaCena = np.array([[4, 5, 6, 8, 10], [6, 4, 3, 5, 8], [9, 7, 4, 3, 4]])

#ulaz je morao biti malo formatiran radi lakseg citanja.
podaci = open('ulaz.txt', 'r')
linija = podaci.readlines()
#na pocetku ulaza se nalazi informacija o tome koliko resursa i korisnika imamo
brojResursa = int(linija[0].strip().split(' ')[0])
brojKorisnika = int(linija[0].strip().split(' ')[1])
resursi = []
korisnici = []
k = 0
matricaCena = np.empty([brojResursa, brojKorisnika])
#iz fajla generisemo listu resursa
for i in range(1, brojResursa+1):
    aktivacija = float(linija[i].strip().split(' ')[1])
    kapacitet = float(linija[i].strip().split(' ')[0])
    resursi.append(Resurs(aktivacija, kapacitet,False))
#iz fajla generisemo listu korisnika i matricu cena
for i in range(brojResursa+1, brojKorisnika*2+brojResursa+1):
    if i % 2 == 1:
        korisnici.append(Korisnik(float(linija[i].strip())))
    elif i % 2 == 0:
        for j in range(0, brojResursa):
            matricaCena[j][k] = float(linija[i].strip().split(' ')[j])
        k += 1

# for r in resursi:
#     print(r.cenaAktivacije, r.resursAktiviran, r.dostupnoResursa)
    
# for k in korisnici:
#     print(k.potraznjaResursa)

# for i in range(matricaCena.shape[0]):
#     for j in range(matricaCena.shape[1]):
#         print(matricaCena[i][j], end =" ")
#     print()
#Poziv funkcije. trenutnaCena je 0 jer je ovo inicijalni poziv. indeksKorisnika je 0 jer krecemo sa vrha.
print(bnb(matricaCena, korisnici, resursi,0, 0))

#!/usr/bin/python
# -*- coding: utf-8 -*-
import os, random, argparse, time, sys

class colors:
    RED 	= '\033[91m'
    GREEN 	= '\033[92m'
    YELLOW 	= '\033[93m'
    BLUE 	= '\033[94m'
    MAGNETA = '\033[95m'
    CYAN	= '\033[96m'
    WHITE	= '\033[97m'
    ENDC 	= '\033[0m'

def testCzas(a,b):
		c = a - b
		print a.strCzas() + " - " + b.strCzas() + " = " + c.strCzas()

class Cczas:

		def __init__(self, g,m,s):
				self.godzina = g
				self.minuta = m
				self.sekunda = s
				self.znak = 1

		def __add__(self, c):
				#Zmienna pomocniczna
				result = Cczas(0,0,0)

				t1 	= self.znak * self.czasNaUsec()
				t2 	= c.znak * c.czasNaUsec()
				diff = t1 + t2

				# Zamiana na wynik
				result.usecNaCzas(abs(diff))
				result.znak = diff / abs(diff)
				return result
		
		def __sub__(self, c):
				#Zmienna pomocniczna
				result = Cczas(0,0,0)

				t1 	= self.znak * self.czasNaUsec()
				t2 	= c.znak * c.czasNaUsec()
				diff = t1 - t2

				# Zamiana na wynik
				result.usecNaCzas(abs(diff))
				result.znak = diff / abs(diff)
				return result
				

		def czasNaUsec(self):
				myTime = self.godzina * 3600 + self.minuta * 60 + self.sekunda
				return myTime

		def usecNaCzas(self,usec):
				self.godzina = usec / 3600
				usec = usec % 3600

				self.minuta = usec / 60
				self.sekunda = usec % 60

		def strCzas(self):
				if (self.znak > 0) :
						znakChr = ''
				else:
						znakChr = '-'
				return znakChr + format(self.godzina,'02') + ":" \
								+ format(self.minuta,'02') + ":" \
								+ format(self.sekunda,'02')



class Cdzien:
		
		def __init__(self, n):
				self.czasy = []
				self.numerdnia = n
				self.dniowka = Cczas(0,0,0)
				self.roznica = Cczas(0,0,0)

		def dodajCzas(self, czas):
				self.czasy.append(czas)

		def obliczDniowke(self):
				i = 0
				while (i < len(self.czasy)):
						self.dniowka = self.dniowka + (self.czasy[i+1] - self.czasy[i])
						i += 2
				#Obliczamy roznice
				self.roznica  = self.dniowka - Cczas(8,0,0)


		def czyDobryZapis(self):
				if ( (len(self.czasy)%2) == 0):
						return True
				else:
						return False

		def wyswietlDzien(self):
				sys.stdout.write("Dzien " + str(self.numerdnia) + "\n")
				
				if self.czyDobryZapis():
						i = 0
						while (i < len(self.czasy)):
							sys.stdout.write("--> "+ self.czasy[i].strCzas() +"\n")
							sys.stdout.write("<-- "+ self.czasy[i+1].strCzas() +"\n")
							i+=2
						sys.stdout.write( colors.YELLOW + self.dniowka.strCzas()\
										+ colors.ENDC  \
										+", dodatkowo "+ self.roznica.strCzas() \
										+".\n")

				else:
						sys.stdout.write("Zapis niepoprawny.\n")

						




#Parsowanie danych wejsciowych
parser = argparse.ArgumentParser()
parser.add_argument("-c", "--cardnr", 	type=int, 		 		required=False)
parser.add_argument("-m", "--month", 	type=int, 		 		required=False)
#parser.add_argument("-o", "--outputfile", 	type=str, 		 		required=False)
#parser.add_argument("-k", "--keyfile", 		type=str, 		 		required=False)
#parser.add_argument("-c", "--crypt", 		action='store_true', 	required=False)
#parser.add_argument("-n", "--newkey", 		type=int, 				required=False)
args = parser.parse_args()

# TODO
# - Dodac klase person
# - - klasa oblicza czas pracy
# - - klasa odczytuje linie i zamienia na zmienne 
# - Zapis do pliku excel

katalog = os.getenv("HOME") + "/Dokumenty/czytnik/"
filename = "mojZapis.fil"


#Odczyt z pliku
filename = katalog + filename
f = open(filename,'r')
while f.closed:
	time.sleep(1)
	f = open(filename,'r')
content = f.readlines()
f.close()

# Wyswietlanie pliku 
i = 0
day = 0
lastday = 0
dni = list(range(1,32)) # Trzeba robic do 32, poniewaz range robi o 1 mniej.
while (i<len(content)):
		# Parsowanie danych do zmiennych
		parameter = content[i][:3]
		cardnr 	= int(content[i][4:11])
		month 	= int(content[i][11:13])
		day 	= int(content[i][13:15])
		hour 	= int(content[i][15:17])
		minute 	= int(content[i][17:19])
		second 	= int(content[i][19:21])

		if (args.cardnr):
				if (args.cardnr == cardnr):
					if (args.month == month):
						# Dodajemy nowy obiekt
						if (isinstance( dni[day], int)):
								dni[day] = Cdzien(day)

						#Dodajemy czas do obiektu
						dni[day].dodajCzas( Cczas(hour,minute,second) )
		i+=1

# Wyświetlanie danych
przepracowane = Cczas(0,0,0)
niedogodziny  = Cczas(0,0,0)
for i in range(1,31):
		if (isinstance(dni[i],Cdzien)):
			# Sprawdzamy czy jest poprawny zapis
			if (dni[i].czyDobryZapis()):
				dni[i].obliczDniowke()

			# Wyświetlamy dane
			dni[i].wyswietlDzien()

			#Obliczenia miesieczne
			przepracowane 	= przepracowane +  	dni[i].dniowka 
			niedogodziny 	= niedogodziny 	+ 	dni[i].roznica 

sys.stdout.write("\n Rozliczenie miesieczne \n");
sys.stdout.write(" Przepracowane : " + przepracowane.strCzas() + "\n");
if (niedogodziny.znak > 0 ): 
	sys.stdout.write(colors.GREEN + " Jesteś do przodu "+ niedogodziny.strCzas() + colors.ENDC + ".\n");
else:
	sys.stdout.write(colors.RED + " Musisz odrobić"+ niedogodziny.strCzas() + colors.ENDC + ".\n" );






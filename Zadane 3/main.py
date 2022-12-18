# coding=utf-8
import random
import copy

#funkcia na vypísanie záhrada
def vypis_zahradu(zahrada, vyska, sirka):
    for r in range(0, vyska):
        for s in range(0, sirka):
            print("{:>3}".format(zahrada[r][s]), end="")
        print("")


#určenie fitness funkcie a vyplnenie záhrady
def hrabanie(povodna_zahrada, geny, kopia):
    fitness = 0
    #zaistenie, aby v pamäti ostala prázdna záhrada a ostala iba v prípade, ak je to už finálne riešenie
    if kopia:
        zahrada = copy.deepcopy(povodna_zahrada)
    else:
        zahrada = povodna_zahrada

    poradie_hrabania = 1

    #prechádzanie všetkých génov uložených v jedincovi
    for gen in geny:
        x = gen[0][1]
        y = gen[0][0]
        smer = gen[1]

        #ak je tam kameň alebo pohrabané, rovno sa posunie ďalej
        if zahrada[y][x] != 0 or zahrada[y][x] == 'K':
            continue

        #ak nie, pokračuje v hrabaní, kým môže
        while True:
            posledna_pozicia = [x, y]
            zahrada[y][x] = poradie_hrabania
            fitness += 1

            #najdenie novej pozicie
            if smer == "hore": y -= 1
            elif smer == "dole": y += 1
            elif smer == "doprava": x += 1
            elif smer == "dolava": x -= 1

            if x < 0 or x >= len(zahrada[0]) or y < 0 or y >= len(zahrada):
                break

            if zahrada[y][x] == 'K' or zahrada[y][x] != 0:
                #ak narazí na prekážku, odčíta sa fitness a vráti sa na predchádzajúcu pozíciu
                fitness -= 1
                x = posledna_pozicia[0]
                y = posledna_pozicia[1]

                #nájdenie nového smeru, ak už sa nemá kde otočiť a skončil uprostred záhrady, hrabanie skončí
                if smer == "hore" or smer == "dole":
                    if x+1 < len(zahrada[0]) and zahrada[y][x+1] == 0:
                        smer = "doprava"
                    elif x-1 >= 0 and zahrada[y][x-1] == 0:
                        smer = "dolava"
                    elif x == 0 or x == len(zahrada[0])-1 or y == 0 or y == len(zahrada):
                        break
                    else:
                        return fitness
                else:
                    if y+1 < len(zahrada) and zahrada[y+1][x] == 0:
                        smer = "dole"
                    elif y-1 >= 0 and zahrada[y-1][x] == 0:
                        smer = "hore"
                    elif x == 0 or x == len(zahrada[0])-1 or y == 0 or y == len(zahrada):
                        break
                    else:
                        return fitness

        poradie_hrabania += 1
    return fitness

#Vytvorí sa gén podľa pozície na obvode
def vytvorenie_genu(vyska, sirka):
    pozicia = random.randrange(2 * (vyska + sirka))
    if pozicia < vyska:
        zaciatok = (pozicia, 0)
        smer = 'doprava'
    elif vyska <= pozicia < sirka + vyska:
        zaciatok = (vyska - 1, pozicia - vyska)
        smer = 'hore'
    elif sirka + vyska <= pozicia < 2 * vyska + sirka:
        zaciatok = (2 * vyska + sirka - pozicia - 1, sirka - 1)
        smer = 'dolava'
    else:
        zaciatok = (0, 2 * (sirka + vyska) - pozicia - 1)
        smer = 'dole'

    return [zaciatok, smer]


def vytvorenie_jedinca(zahrada, vyska, sirka, pocet_kamenov):
    #formát jedinca - fitness, gény
    geny = []

    #každý gén má začiatok, kde mníh vstupuje do záhrady a smer
    for _ in range(vyska+sirka+pocet_kamenov):
        novy_gen = vytvorenie_genu(vyska, sirka)
        zaciatok = novy_gen[0]
        smer = novy_gen[1]
        geny.append([zaciatok, smer])

    fitness = hrabanie(zahrada, geny, True)
    return [fitness, geny]


def krizenie(povodna_zahrada, rodic1, rodic2, vyska, sirka):
    zahrada = copy.deepcopy(povodna_zahrada)
    potomkovia = []
    typ = random.choice(["polovica", "nahodne"])
    #náhodne sa zvolí aký typ kríženia sa použije

    geny_prveho = rodic1[1]
    geny_druheho = rodic2[1]

    if typ == "polovica":
        #polovica z jedného, polovica z druhého
        bod = len(geny_prveho)
        geny_dietata = geny_prveho[:bod] + geny_druheho[bod:]

    else:
        #náhodne vybrane geny
        geny_dietata = []
        for i in range(0, len(geny_prveho)):
            aktualny_gen1 = geny_prveho[i]
            aktualny_gen2 = geny_druheho[i]
            geny_dietata.append(random.choice([aktualny_gen1, aktualny_gen2]))

    #mutácia, ak je percento mensie ako 5
    for i in range(0, len(geny_dietata)):
        percento = random.randrange(0, 100)
        if percento < 6:
            geny_dietata[i] = vytvorenie_genu(vyska, sirka)

    fitness = hrabanie(zahrada, geny_dietata, True)
    potomkovia.append([fitness, geny_dietata])
    return potomkovia


def geneticky_algoritmus(zahrada, vyska, sirka, pocet_kamenov):
    populacia = []
    #vytvorenie prvej generácie
    for _ in range(100):
        populacia.append(vytvorenie_jedinca(zahrada, vyska, sirka, pocet_kamenov))

    for generacia in range(500):
        nova_generacia = []

        #turnaj
        for _ in range(99):
            turnaj = random.sample(populacia, 2)
            if turnaj[0][0] > turnaj[1][0]:
                rodic1 = turnaj[0]
            else:
                rodic1 = turnaj[1]

            turnaj = random.sample(populacia, 2)
            if turnaj[0][0] > turnaj[1][0]:
                rodic2 = turnaj[0]
            else:
                rodic2 = turnaj[1]

            potomkovia = krizenie(zahrada, rodic1, rodic2, vyska, sirka)
            nova_generacia.append(potomkovia[0])

        # elitarizums
        max_fitness = 0
        max_jedinec = []
        for i in populacia:
            if i[0] > max_fitness:
                max_fitness = i[0]
                max_jedinec = i
        nova_generacia.append(max_jedinec)

        populacia = nova_generacia

        max_fitness = 0
        priemerna_fitness = 0
        for i in populacia:
            if i[0] > max_fitness:
                max_fitness = i[0]
            priemerna_fitness += i[0]

        priemerna_fitness = round(priemerna_fitness / len(populacia))
        print("Číslo generácie: ", generacia+1, ", Priemerná fitness: ", priemerna_fitness, ", Maximálna fitness: ",
              max_fitness)

        #kontrola či sa nenašlo riešenieza
        for jedinec in populacia:
            fitness = jedinec[0]
            if fitness == vyska*sirka-pocet_kamenov:
                hrabanie(zahrada, jedinec[1], False)
                print("")
                vypis_zahradu(zahrada, vyska, sirka)
                print("")
                return

    print("Prerkročený počet generácii")


def main():
    while True:
        vstup = input("Riešenie pre mapu podľa zadania alebo vlastnu? zadanie/vlastna\n")
        if vstup == "zadanie":
            vyska = 10
            sirka = 12
            pocet_kamenov = 6
            zahrada = [[0] * sirka for _ in range(vyska)]
            zahrada[2][1], zahrada[1][5], zahrada[3][4], zahrada[4][2], zahrada[6][8], zahrada[6][9] = pocet_kamenov*['K']
            geneticky_algoritmus(zahrada, vyska, sirka, pocet_kamenov)

        elif vstup == "vlastna":
            sirka = input("Šírka:\n")
            vyska = input("Výška:\n")
            pocet_kamenov = input("Počet kameňov:\n")
            if sirka.isnumeric() and vyska.isnumeric() and pocet_kamenov.isnumeric():
                sirka = int(sirka)
                vyska = int(vyska)
                pocet_kamenov = int(pocet_kamenov)
            else:
                print("zle zadaný vstup")
                continue

            zadanie_kamenov = input("Zadať pozíciu kameňov alebo generovať náhdone? zadat/nahodne\n")
            zahrada = [[0] * sirka for _ in range(vyska)]

            if zadanie_kamenov == "nahodne":
                vygenerovane = 0
                while vygenerovane < pocet_kamenov:
                    x = int(random.randrange(0, sirka))
                    y = int(random.randrange(0, vyska))
                    if zahrada[y][x] == 0:
                        zahrada[y][x] = 'K'
                        vygenerovane += 1
            elif zadanie_kamenov == "zadat":
                for i in range(pocet_kamenov):
                    suradnice = (input("zadajte súradnice vo formáte y x\n")).split()
                    x = int(suradnice[1])
                    y = int(suradnice[0])
                    if x < sirka and y < vyska:
                        zahrada[y][x] = 'K'
                    else:
                        print("zle zadané súradnice")
                        continue
            geneticky_algoritmus(zahrada, vyska, sirka, pocet_kamenov)


main()

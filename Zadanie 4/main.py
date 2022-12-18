import matplotlib.pyplot as plt
import random
import math
import numpy
import time

def vykresli_body(klastre):
    farby = ["Lavender", "MediumPurple", "Indigo", "MidnightBlue", "DodgerBlue", "SkyBlue", "Turquoise", "Teal",
             "SeaGreen", "DarkGreen", "NavajoWhite", "Brown", "Gold", "Coral", "Crimson", "LightPink", "Sienna",
             "SlateGray", "SandyBrown", "AliceBlue"]
    x = []
    y = []

    for klaster in klastre:
        body = klastre[klaster]
        for bod in body:
            x.append(bod[0])
            y.append(bod[1])
        plt.scatter(x, y, s=0.2, color=farby[list(klastre.keys()).index(klaster)])

        x = []
        y = []
    plt.show()


def vytvor_body(vyska, sirka, pocet_bodov):
    body = []
    # vytvorenie povodnych 20 bodov
    while len(body) < 20:
        x = random.randrange(0, vyska)
        y = random.randrange(0, sirka)
        if [x, y] not in body:
            body.append([x, y])

    # pridanie dalsich 20 000 bodov
    # ak by nova suradnica bola von z mapy, odcita sa namiesto pricitania
    while len(body) < pocet_bodov+20:
        vybrany_bod = random.choice(body)
        if vybrany_bod[0]-100 < 0 or vybrany_bod[0]+100 > vyska:
            x = random.randrange(-50, 50)
            if vybrany_bod[0]+x <= 0 or vybrany_bod[0]+x >= vyska:
                x *= -1
        else:
            x = random.randrange(-100, 100)
        if vybrany_bod[1] - 100 < 0 or vybrany_bod[1] + 100 > sirka:
            y = random.randrange(-50, 50)
            if vybrany_bod[1] + y <= 0 or vybrany_bod[1] + y >= vyska:
                y *= -1
        else:
            y = random.randrange(-100, 100)

        body.append([vybrany_bod[0] + x, vybrany_bod[1] + y ])
    return body


def vypocitaj_vzdialenost(bod1, bod2):
    x = abs(bod1[0]-bod2[0])
    y = abs(bod1[1]-bod2[1])
    vzdialenost = round(math.sqrt((x*x) + (y*y)))
    return int(vzdialenost)


def vypocitanie_priemernej_vzdialenosti(stred, body):
    priemerna_vzdialenost = 0
    for bod in body:
        priemerna_vzdialenost += vypocitaj_vzdialenost(bod, stred)
    priemerna_vzdialenost /= len(body)
    return priemerna_vzdialenost


def najdi_stred(body):
    x = 0
    y = 0

    for bod in body:
        x += bod[0]
        y += bod[1]

    stred = [int(x / len(body)), int(y / len(body))]
    return stred


def vypocitaj_medoid(klastre):
    nove_klastre = {}

    #prechadza vsetky klastre
    for klaster in klastre:
        body = klastre[klaster]
        stred = klaster

        najmensia_vzdialenost = 10000
        # najde bod, ktory ma ma najmensiu priemernu vzdialenost so statnymi
        for novy_stred in body:
            priemerna_vzdialenost = vypocitanie_priemernej_vzdialenosti(novy_stred, body)
            if priemerna_vzdialenost < najmensia_vzdialenost:
                najmensia_vzdialenost = priemerna_vzdialenost
                stred = novy_stred

        # zapise sa ako novy stred
        nove_klastre[(stred[0], stred[1])] = []
    return nove_klastre


def vypocitaj_centroid(klastre):
    nove_klastre = {}
    for klaster in klastre:
        body = klastre[klaster]
        stred = najdi_stred(body)
        nove_klastre[(stred[0], stred[1])] = []
    return nove_klastre


def kmeans(body, typ):
    k = random.randrange(5, 13)
    klastre = {}
    #nahodne vyberiem k bodov ako  stredy
    while len(klastre) < k:
        klaster_list = random.choice(body)
        klaster = (klaster_list[0], klaster_list[1])
        if klaster not in klastre.keys():
            klastre[klaster] = []

    while True:
        # prechadzam body a zistujem, ku ktoremu centroidu su najblizie
        for bod in body:
            najmensia_vzdialenost = 100000
            for stred in klastre.keys():
                vzdialenost = vypocitaj_vzdialenost(bod, stred)
                if vzdialenost < najmensia_vzdialenost and bod != stred:
                    najmensia_vzdialenost = vzdialenost
                    najmensi_stred = stred
            klastre[najmensi_stred].append(bod)

        #urci sa novy stred podla centroidu alebo medoidu
        povodne_klastre = klastre
        if typ == "centroid":
            klastre = vypocitaj_centroid(klastre)
        elif typ == "medoid":
            klastre = vypocitaj_medoid(klastre)
        if klastre != povodne_klastre:
            break

    return povodne_klastre


def vypocitat_nove(vzdialenosti, stred, body, dlzka):
    nove_vzdialenosti = []

    # vypocita sa vzdialenost noveho stredu od ostatnych
    for i in range(dlzka):
        nova_vzdialenost = vypocitaj_vzdialenost(stred, body[i])
        nove_vzdialenosti.append(nova_vzdialenost)

    # prida sa do matice
    vzdialenosti = numpy.vstack((vzdialenosti, nove_vzdialenosti))
    nove_vzdialenosti.append(10000)
    column_to_add = numpy.array(nove_vzdialenosti)
    vzdialenosti = numpy.column_stack((vzdialenosti, column_to_add))
    return vzdialenosti


def aglomerativne_zhlukovanie(body):
    povodne_body = body
    dlzka = len(body)
    vzdialenosti = numpy.zeros((dlzka, dlzka)).astype(int)
    klastre = {}

    # naplnenie matice vzdialenosti
    for riadok in range(dlzka):
        for stlpec in range(dlzka):
            if riadok != stlpec:
                vzdialenost = vypocitaj_vzdialenost(body[riadok], body[stlpec])
                vzdialenosti[riadok][stlpec] = vzdialenost
                vzdialenosti[stlpec][riadok] = vzdialenost
            else:
                vzdialenosti[riadok][stlpec] = 10000

    minimalna_vzdialenost = 0
    while minimalna_vzdialenost < 500:
        # najdenie minima
        indexy = numpy.where(vzdialenosti == vzdialenosti.min())
        minimum = [indexy[0][0], indexy[1][0]]
        minimalna_vzdialenost = vzdialenosti.min()

        index1 = min([minimum[0], minimum[1]])
        index2 = max([minimum[0], minimum[1]])-1

        # body medzi ktorymi je najmensia vzdialenost
        bod1 = body[index1]
        bod2 = body[index2+1]
        stred = najdi_stred([bod1, bod2])

        # vymazanie bodov zo zoznamu aj matice vzdialenosti
        del body[index1]
        del body[index2]
        dlzka -= 2
        vzdialenosti = numpy.delete(vzdialenosti, index1, 0)
        vzdialenosti = numpy.delete(vzdialenosti, index1, 1)
        vzdialenosti = numpy.delete(vzdialenosti, index2, 0)
        vzdialenosti = numpy.delete(vzdialenosti, index2, 1)

        # vypocitanie novej vzdialenosti
        vzdialenosti = vypocitat_nove(vzdialenosti, stred, body, dlzka)
        body.append(stred)
        bod1_v_klastri = (bod1[0], bod1[1]) in list(klastre.keys())
        bod2_v_klastri = (bod2[0], bod2[1]) in list(klastre.keys())

        # ak uz boli oba body stredmi v existujucich klastroch, spoja sa
        if bod1_v_klastri and bod2_v_klastri:
            nove_body1 = klastre.pop((bod1[0], bod1[1]))
            nove_body2 = klastre.pop((bod2[0], bod2[1]))

            if bod1 in povodne_body:
                nove_body1.append(bod1)
            if bod2 in povodne_body:
                nove_body1.append(bod2)
            nove_body1.extend(nove_body2)
            klastre[(stred[0], stred[1])] = nove_body1

        # ak bol iba jeden stredom, druhy sa prida k nemu a nastavi sa novy stred
        elif bod1_v_klastri:
            nove_body = klastre.pop((bod1[0], bod1[1]))
            if bod2 in povodne_body:
                nove_body.append(bod2)
            klastre[(stred[0], stred[1])] = nove_body
        elif bod2_v_klastri:
            nove_body = klastre.pop((bod2[0], bod2[1]))
            if bod1 in povodne_body:
                nove_body.append(bod1)
            klastre[(stred[0], stred[1])] = nove_body

        #ak nebol ani jeden ešte zaradený do klastrov, vytvorí sa nový
        else:
            klastre[(stred[0], stred[1])] = [bod1, bod2]

        dlzka += 1
    return klastre


def rozdelit_najvacsi(klastre, stred):
    # k means algoritmus
    # vyberú sa 2 náhdone body ako stredy
    body = klastre.pop(stred)
    stred1 = random.choice(body)
    stred2 = random.choice(body)
    nove_body1 = [stred1]
    nove_body2 = [stred2]

    while True:
        #priraduju sa postupne body a stredy sa aktualizuju
        povodny_stred1 = stred1
        povodny_stred2 = stred2
        for bod in body:
            if vypocitaj_vzdialenost(stred1, bod) < vypocitaj_vzdialenost(stred2, bod):
                nove_body1.append(bod)
            else:
                nove_body2.append(bod)
        stred1 = najdi_stred(nove_body1)
        stred2 = najdi_stred(nove_body2)

        # ak su stredy rovnake, aj body budu rovnake a cyklus moze skoncit
        if stred1 == povodny_stred1 and stred2 == povodny_stred2:
            break

        nove_body1 = []
        nove_body2 = []

    # vlozia sa nove klastre
    klastre[(stred1[0], stred1[1])] = nove_body1
    klastre[(stred2[0], stred2[1])] = nove_body2
    return klastre


def divizivne_zhlukovanie(body):
    stred = najdi_stred(body)
    klastre = {(stred[0], stred[1]): body}

    while True:
        # pocitaju sa priemerne vzdialenosti bodov v klastri od stredu
        maximalna_vzdialenost = 0
        vzdialenosti = []
        for klaster in klastre:
            aktualna_priemerna = vypocitanie_priemernej_vzdialenosti(klaster, klastre[klaster])
            vzdialenosti.append(aktualna_priemerna)
            if maximalna_vzdialenost < aktualna_priemerna:
                maximalna_vzdialenost = aktualna_priemerna
                klaster_max = klaster

        # klaster s najvacsou priemernou vzdialenosotu je vybraty na rozdelenie
        klastre = rozdelit_najvacsi(klastre, klaster_max)
        if maximalna_vzdialenost < 500:
            break

    return klastre


def main():
    vyska = 10000
    sirka = 10000
    pocet_bodov = 20000


    while True:
        algoritmus = input("1.k-means medoid\n2.k-means centroid\n3.aglomeraticne zhlukovanie\n4.divizivne zhlukovanie\n5.koniec\n")
        body = vytvor_body(vyska, sirka, pocet_bodov)
        start = time.time()
        if algoritmus == "1":
            klastre = kmeans(body, "medoid")
        elif algoritmus == "2":
            klastre = kmeans(body, "centroid")
        elif algoritmus == "3":
            klastre = aglomerativne_zhlukovanie(body)
        elif algoritmus == "4":
            klastre = divizivne_zhlukovanie(body)
        elif algoritmus == "5":
            return
        else:
            print("zlý vstup")
        end = time.time()
        print("čas: ", round(end-start, 2))

        uspesne = 0
        for i in klastre:
            if vypocitanie_priemernej_vzdialenosti(i, klastre[i]) < 500:
                uspesne += 1
        print("úspešnosť: ", round(uspesne/(len(klastre)/100), 2))

        vykresli_body(klastre)


if __name__ == '__main__':
    main()

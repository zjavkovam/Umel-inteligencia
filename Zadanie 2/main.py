import random
import time


#rekurzívna funkcia, ktorá prejde celú šachovnicu
def eulerov_tah(sachovnica, aktualna_pozicia, pohyb,tah, cas_zaciatok,limit):
    x = aktualna_pozicia[0]
    y = aktualna_pozicia[1]

    #ak sa počet ťahov rovná veľkosti šachovnice, znamená to, že sa prešli všetky políčka
    if(tah == len(sachovnica)*len(sachovnica)):
        return True

    #prechádza všetky možné posuny v rámci súradníc zadefinovaných v poli pohyb
    for i in pohyb:
        nove_x = i[0]
        nove_y = i[1]


        #podmienka, či sa pohybom nedostane kôň zo šachovnice alebo či tam už nebol v predchádzajúcich krokoch
        if x+nove_x >= 0 and nove_x+x <= len(sachovnica)-1 and y+nove_y >= 0 and nove_y+y <= len(sachovnica)-1:
            nova_pozicia = [x + nove_x, y + nove_y]
            if (sachovnica[x+nove_x][y+nove_y] == 0):
                sachovnica[x + nove_x][y + nove_y] = tah+1

                #podmienka na zistenie, či nebol prekročený časový limit
                aktualny_cas = time.time() - cas_zaciatok
                if(limit >0 and aktualny_cas >= limit):
                    return False

                #rekurzívne vnáranie na zistenie ďalšej pozície
                if (eulerov_tah(sachovnica,nova_pozicia,pohyb,tah+1,cas_zaciatok, limit)):
                    return True

                #keď sa vynorí z rekurzie, znamená to, že nenašlo správne políčko a vynuluje sa
                sachovnica[x + nove_x][y + nove_y] = 0

    #ukončenie rekurzívnej vetvy
    return False




def main():
        pohyb = [[1, 2], [1, -2], [2, 1], [2, -1], [-1, 2], [-1, -2], [-2, 1], [-2, -1]]

        while(True):
            casovy_limit = input("Časový limit v sekundách?\n")
            velkost = input("Veľkosť šachovnice?\n")
            if not velkost:
                break

            if not casovy_limit:
                casovy_limit = 0


            velkost_sachovnice = int(velkost)
            zaciatok = [velkost_sachovnice-1,0]

            for i in range(0,5):

                print("Bod č.",i+1,"\nsúradnice:",zaciatok)

                #inicializovanie zoznamu a zapísanie začiatku
                sachovnica = [[0] * velkost_sachovnice for i in range(velkost_sachovnice)]
                sachovnica[zaciatok[0]][zaciatok[1]] = 1

                #rekurzívna funkcia na nájdenie riešenia
                zaciatok_casu = time.time()
                eulerov_tah(sachovnica,zaciatok,pohyb,1,zaciatok_casu, int(casovy_limit))

                #vypočítaný čas na rriešenie
                celkovy_cas = time.time()-zaciatok_casu
                print("Čas: ", round(celkovy_cas,3),"\nRiešenie: ",end="")

                #zistí, či riešenie je celé alebo riešenie nenašlo
                vyriesene = True
                for j in sachovnica:
                    if 0 in j:
                        vyriesene = False

                if(vyriesene):
                    print("\n",end="")
                    for r in sachovnica:
                        print(r)
                    print("\n")
                else:
                    print("Riešenie sa nenašlo\n")

                #nový začiatok, kde sú x a y súradnice zvolené náhodne
                zaciatok = [random.randint(0,velkost_sachovnice-1), random.randint(0,velkost_sachovnice-1)]



# funkcia na vypísanie všetkých možností bez limitu
def testovanie_vsetky(velkost_sachovnice):
    pohyb = [[1, 2], [1, -2], [2, 1], [2, -1], [-1, 2], [-1, -2], [-2, 1], [-2, -1]]

    n=1
    for i in range(0, velkost_sachovnice):
        for j in range(0, velkost_sachovnice):
            zaciatok = [i, j]

            print("Bod č.", n, "\nsúradnice:", zaciatok)
            # inicializovanie zoznamu a zapísanie začiatku
            sachovnica = [[0] * velkost_sachovnice for i in range(velkost_sachovnice)]
            sachovnica[zaciatok[0]][zaciatok[1]] = 1

            # rekurzívna funkcia na nájdenie riešenia
            zaciatok_casu = time.time()
            eulerov_tah(sachovnica, zaciatok, pohyb, 1, zaciatok_casu, 0)

            # vypočítaný čas na riešenie
            celkovy_cas = time.time() - zaciatok_casu
            print("Čas: ", round(celkovy_cas, 3), "\nRiešenie: ", end="")

            # zistí, či riešenie je celé alebo riešenie nenašlo
            vyriesene = True
            for j in sachovnica:
                if 0 in j:
                    vyriesene = False

            if (vyriesene):
                print("\n", end="")
                for r in sachovnica:
                    print(r)
                print("\n")
            else:
                print("Riešenie sa nenašlo\n")

            n += 1


main()
#testovanie_vsetky(5)

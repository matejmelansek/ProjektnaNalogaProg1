# ProjektnaNalogaProgramiranje1

Analiziral bom vse igralce iz najboljših petih nogometnih lig v Evropi (Premier League, LaLiga, Bundesliga, Serie A, Ligue 1). [Transfermarkt](https://www.transfermarkt.com/)

**Za vsakega igralca bom zajel:**

- starost
- tržno vrednost
- višino 
- močnejšo nogo
- državljanstvo


**Delovne hipozeze:**

- najdražji igralci so Brazilci
- LaLiga (ES1) ima povprečno najnižje igralce
- Serie A (IT1) ima povprečno najstarejše igralce
- delež nogometašev najboljših petih evropskih lig, ki raje uporabljajo levo nogo, je večji kot delež ljudi, ki raje uporabljajo levo nogo v splošni populaciji
- ne obstaja korelacija med igralčevo višino in njegovo tržno vrednostjo
- v vsaki ligi je največji delež igralcev državljanov tiste države, ki gosti ligo


**Navodila:**

Dodana je CSV datoteka 27 nogometašev z vsemi podatki, ki jih bomo analizirali. Če želimo ponovno sneti podatke iz Transfermarkt-a, poženemo python program zbiranje_podatkov. Ta bo najprej poiskal vse povezave do Transfermarkt strani vsakega igralca v določeni ligi, ustvaril datoteko, katere ime je kratica lige in začel shranjevati html-je spletne strani vsakega igralca. Nato bo ponovno odprl shranjene datoteke in z regularnimi izrazi poiskal vse želene podatke, katere bo shranil v slovar. To bo ponovil za vse lige. Če smo program že kdaj zaganli in imamo shranjenih del html datotek, nam jih program ne bo ponovno shranjeval. Če programa še nismo nikoli zagnali, bo proces shranjevanja igralcev trajal nekoliko dlje časa. 

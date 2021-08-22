import orodja
import zbiranje_igralcev
import re
import os

STEVILO_LIG = 5

linki_lig = ['https://www.transfermarkt.com/premier-league/startseite/wettbewerb/GB1',
'https://www.transfermarkt.com/laliga/startseite/wettbewerb/ES1',
'https://www.transfermarkt.com/bundesliga/startseite/wettbewerb/L1',
'https://www.transfermarkt.com/serie-a/startseite/wettbewerb/IT1',
'https://www.transfermarkt.com/ligue-1/startseite/wettbewerb/FR1']

imena_lig = ['GB1','ES1','L1','IT1','FR1']

#Vzorec podatkov vsakega igralca (ID, Ime, Trzna Vrednost, Starost, Visina, Drzavljanstvo, Mocnejsa Noga)
vzorec_podatkov = (
    r'Current market value:\n\s*</div>\n\s*<div class="right-td">\n\s*'
    r'(<a href=.*target="_blank">)*\D*'
    r'(?P<TrznaVrednost>\d{1,3}\.?\d\d[mTh]+)'
    r'\.*.*\s*</div>\n\s*</div>(\n.*){1,100}'
    r'\s*<a title="'
    r'(?P<Ime>.{1,100})'
    r'" class="spielprofil_tooltip" id="'
    r'(?P<ID>\d{1,15})"'
    r' href=".*(\n.*){1,100}\s*<th>Age:</th>\n\s*<td>'
    r'(?P<Starost>\d{2})'
    r'</td>\n\s*</tr>\n\s*<tr>\n\s*'
    r'(<th>Height:</th>\n\s*<td>(?P<Visina>\d,\d\d)&nbsp;m</td>\n\s*</tr>\n\s*<tr>\n\s*)?'
    r'<th>Citizenship:'
    r'</th>\n\s*<td>\n\s*<img src="https://tmssl.akamaized.net/images/flagge/tiny/\d*.png\?lm=\d*" title="'
    r'(?P<Drzavljanstvo>.{1,60})"'
    r' alt=.*\n\s*</tr>\n\s*<tr>\n\s*<th>Position:</th>\n\s*<td>\n\s*.*\s*</td>'
    r'\n\s*</tr>\n\s*<tr>\n\s*'
    r'(<th>Foot:</th>\n\s*<td>(?P<MocnejsaNoga>\w{1,10})</td>)?'
   )

#Nekatere trzne vrednosti so podane v milijonih, druge pa v tisočih, oboje spremenimo v floate štete v milijonih
def popravi_trzno_vrednost(igralec):
    if 'm' in igralec['TrznaVrednost']:
        vrednost_str = igralec['TrznaVrednost'].replace('m','')
        vrednost = float(vrednost_str)
        igralec['TrznaVrednost'] = vrednost
    else:
        vrednost_str = igralec['TrznaVrednost'].replace('Th','')
        vrednost = int(vrednost_str)
        igralec['TrznaVrednost'] = vrednost/1000
    return igralec

#Visina je podana kot string z vejico med metri in centimetri, spremenimo jo v int podan v centimetrih
def popravi_visino(igralec):
    if igralec['Visina'] == None:
        return igralec
    else:
        visina_str = igralec['Visina']
        visina = int(visina_str[0]) * 100 + int(visina_str[-2:])
        igralec['Visina'] = visina
        return igralec


#Najprej shranimo html-je spletnih strani vseh igralcev lige v mapo imenovano s kratico lige
for n in range(STEVILO_LIG):
    url_lige = linki_lig[n]
    ime_datoteke = imena_lig[n]
    zbiranje_igralcev.shrani_igralce(url_lige,ime_datoteke)


#Pripravimo si prazen seznam, ki bo vseboval slovarje s podatki posameznih igralcev
igralci = []


#Funkcija ki odpre mapo vsake lige, izlušči podatke vseh igralcev, jih popravi in shrani v seznam 
def zberi_podatke():
    for n in range(STEVILO_LIG):
        ime_lige = imena_lig[n]
        st_igralcev_v_ligi = len(os.listdir(ime_lige))
        for m in range(st_igralcev_v_ligi):
            ime_datoteke = ime_lige + '/' + str(m) + '.html'
            vsebina = orodja.vsebina_datoteke(ime_datoteke)
            for zadetek in re.finditer(vzorec_podatkov,vsebina):
                igralec = zadetek.groupdict()
                igralec['Liga'] = ime_lige
                igralec['ID'] = int(igralec['ID'])
                igralec['Starost'] = int(igralec['Starost'])
                igralec = popravi_trzno_vrednost(igralec)
                igralec = popravi_visino(igralec)
                igralec_ord = {k : igralec[k] for k in ['ID','Ime','TrznaVrednost','Starost','Visina','Drzavljanstvo','MocnejsaNoga','Liga']}
                igralci.append(igralec_ord)
    zapisi_v_csv(igralci)


#Funkcija, ki uredi igralce po ID-ju in shrani njihove podatke v csv datoteko
def zapisi_v_csv(igralci):
    igralci.sort(key=lambda igralec: igralec['ID'])
    orodja.zapisi_csv(igralci,['ID','Ime','TrznaVrednost','Starost','Visina','Drzavljanstvo','MocnejsaNoga','Liga'],'podatki.csv')


zberi_podatke()
print(igralci)
print(len(igralci))
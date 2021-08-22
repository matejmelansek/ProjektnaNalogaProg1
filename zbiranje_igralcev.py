import orodja
import re
import requests


def nalozi_stran(url):
    stran = requests.get(url, headers={'User-Agent': 'Custom'})
    return stran.text

vzorec_ekipe = (r'rechts"><a class="vereinprofil_tooltip" href="(?P<Ekipa>.{30,120})"><img')
vzorec_igralca = (
    r'"hide-for-small"><a title="\D{1,32}" class="spielprofil_tooltip" id="\d{1,8}" href="(?P<Igralec>.{17,70})">'
    r'.{1,40}</a></span></div><div class="di nowrap">'
    )


#Pobere delne linke ekip iz spletne strani lige in da polne linke v seznam
def ekipe(url_lige):
    vsebina = nalozi_stran(url_lige)
    linki_ekip = []
    for zadetek in re.finditer(vzorec_ekipe, vsebina):
        linki_ekip.append(zadetek['Ekipa'])
    for ekipa in range(len(linki_ekip)):
        linki_ekip[ekipa] = 'https://www.transfermarkt.com' + linki_ekip[ekipa]
    return linki_ekip


#Pobere delne linke igralcev iz vsake ekipe iz seznama polnih linkov ekip lige in da polne linke igralcev v seznam
def igralci(url_lige):
    linki_igralcev = []
    for ekipa in ekipe(url_lige):
        vsebina = nalozi_stran(ekipa)
        l_igralcev = []
        for zadetek in re.finditer(vzorec_igralca, vsebina):
            l_igralcev.append(zadetek['Igralec'])
        for igralec in range(len(l_igralcev)):
            l_igralcev[igralec] = 'https://www.transfermarkt.com' + l_igralcev[igralec]
        linki_igralcev = linki_igralcev + l_igralcev
    return linki_igralcev


#Shrani vsebino spletnih strani vseh igralcev lige v datoteko z imenom lige
def shrani_igralce(url_lige, ime_datoteke):
    vsi_igralci_lige = igralci(url_lige)
    for igralec in range(len(vsi_igralci_lige)):
        url = vsi_igralci_lige[igralec]
        datoteka = ime_datoteke + '/' + str(igralec) + '.html'  
        orodja.shrani_spletno_stran(url, datoteka)
    

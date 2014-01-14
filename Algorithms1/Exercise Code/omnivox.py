"""
Created on Jan 4, 2014

@author: Lucas
"""
import urllib2
import urllib
import cookielib
import requests
import re
from mechanize import Browser
from BeautifulSoup import BeautifulSoup

viewstate = "VwlXDFjyFvUuDRQKEl5Qz/3OquyohnuhTFVsP6z7YmAf5HR2tYTgoiuYOG2CWTltrTEOYGG/d3M8flnF5hVTyn4wU/Asw2VVwwIb8aAh+axr0F1B4XJCZcc4ZGWqNK2pTDBLqux5Iuvy4njICsGkE/RRN20vApIw24hBP23XuNMz4ZLk/LWFzNyx/SpuUWRaYl7VFCLEylnOTqAmYNSRIiDn3xXP7FtjM3JQXAStsfj+kSyTkqwcDVH6/7zHUkEMWjlPBM71XIaXnjY/EL3p15ZENO0cjEKZGjTFa7SzeMmOBDXE/PrvnpKgnS4SnvsV8TI/rX9o7+rKbM2/bw+p/WBBwH56m/quHdYgyvTDuzkSQHCopNVLL3R8+BgMFS+8HpcPbitQUdpLo9j2m871gqs+5VZqP4EgnLHIDf2iX2RQmxPwSh727EM8NT1oxWg6kEmcpgZsCO/xESk7TXimsy05Rst/lCmG/K/6HgAg0qZ1GJxPNKC5WHspFUacktPuHwT25NoecFsO4jz/SNaUtOnrWS28YejS5TlcaL4jwYLJDskEPsnTiHr/7lTGqsTR07u/a1JDOVEca9SC9q/MidLz1AI0rUVf9y6yn6KbNbfPQaflVEB70BlnVmsf7Dkdp92rIU7EKrrFVGi3FeQhlUhFz/uGMWx9TJaCBF9yducB67LasFv7XBBpR01O7djHws/9X3JRa2UHRRl6FofUjSDMp2VKcFtQPHbI5dX1LBr4rXmRJg+FQ0X6yF8="
url = "https://marianopolis.omnivox.ca/intr/Module/Identification/Login/Login.aspx?"
s=requests.Session()

headers = {
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Encoding":"gzip,deflate,sdch",
    "Accept-Language":"en-US,en;q=0.8",
    "Cache-Control":"max-age=0",
    "Connection":"keep-alive",
    "Content-Length":"398",
    "Content-Type":"application/x-www-form-urlencoded",
    "Cookie":"L=ANG; Resolution=1280; TypeIndividu=Etudiant; UsersNbCouleurs=32; TypeProfil=; ParametresModule=H4sIAMwWom8A/+VUXUrDQBBObJKmSO+QA4TQ9Me0D3mKfyBCsdqXEOgmDrp0s9HdjRCP4RFFvIMg6E6o4FPfCkp3YWZ2mB3mm29nDdMwjC+9UOOy0Hg1F41UUAZJxRgUilZcBmfAQdAiOKatg4hmNUzTTeBCCcrvfK+URSUYzX1vCULqsHgcDHD7XlIzVQuIOdRKEOZ78zpntLiA5rpaA4/zKCKTYnIUzkZjGExnmb/L5JmlcXY3edykKh+IAOGeE3m/oM/Q1zeXhNUwJ1RIo2N03JdtTdnok8eaMKqan3yrcKcdytz3bUX9xvCvuUqzA81WD0UHDRQWnv4iJzhFXaywna225re9YMn61P/IfkBtWV1DYz8hHNN0bO3oX1a3cAVSCaBcOY522aeESTA/dGOwOY6rfe6NBMFJCU4PX0o4HIVROD38BiX7fIWKBQAAJft8hYoFAAA=; IsSessionInitialise=; IdControlDefault=NoDA; k=eXdtS1N1dXB2TTF6bUx6YkpETjZVVm9tL0NEdlhrb25JbHNUTFBXOTVVVkRxeG5vc3pIOVJaWHo3OTFycE11NQ__; comn=MPOP; chkcookie=1388861178006",
    "Host":"marianopolis.omnivox.ca",
    "Origin":"https://marianopolis.omnivox.ca",
    "Referer":"https://marianopolis.omnivox.ca/intr/Module/Identification/Login/Login.aspx?ReturnUrl=%2fintr%2f%3fC%3dMPO%26E%3dP%26L%3dANG%26Ref%3d20140104134109&C=MPO&E=P&L=ANG&Ref=20140104134109",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.62 Safari/537.36"
}

# AS OF NOW THE COOKIE IN HEADERS2 IS ARTIFICIALLY INSERTED
headers2 = {
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Encoding":"gzip,deflate,sdch",
    "Accept-Language":"en-US,en;q=0.8",
    "Cache-Control":"max-age=0",
    "Connection":"keep-alive",
    "Cookie":"L=ANG; comn=MPOP; IsSessionInitialise=; Resolution=1280; TypeIndividu=Etudiant; UsersNbCouleurs=32; TypeProfil=; ParametresModule=H4sIAAvPxG8A/+VUXUrDQBBObJKmSO+QA4TQ9Me0D3mKfyBCsdqXEOgmDrp0s9HdjRCP4RFFvIMg6E6o4FPfCkp3YWZ2mB3mm29nDdMwjC+9UOOy0Hg1F41UUAZJxRgUilZcBmfAQdAiOKatg4hmNUzTTeBCCcrvfK+URSUYzX1vCULqsHgcDHD7XlIzVQuIOdRKEOZ78zpntLiA5rpaA4/zKCKTYnIUzkZjGExnmb/L5JmlcXY3edykKh+IAOGeE3m/oM/Q1zeXhNUwJ1RIo2N03JdtTdnok8eaMKqan3yrcKcdytz3bUX9xvCvuUqzA81WD0UHDRQWnv4iJzhFXaywna225re9YMn61P/IfkBtWV1DYz8hHNN0bO3oX1a3cAVSCaBcOY522aeESTA/dGOwOY6rfe6NBMFJCU4PX0o4HIVROD38BiX7fIWKBQAAJft8hYoFAAA=; TKINTR=6663EE079E247AF79DBC159A4B058D79A32B4C4C2A5AD834F48ACBA88FAF977D1EF103BA17B90A21F3C4B41786EABF7276356158D3C4E655AFB243479E84A92DCF9398E33EF124BBDAECCD9D573A0503E1FA6B4740A64200F918084F2D3212F30C8119AC04DC19B169552E84; TKSMPOP=OXo3dkkyTEp1YVZrTHB2UXVqdGFKTUthVGNMM0dLc2dPWWkxWXkvemxrYTFyRWxhTnB4MEFLM0pER0VLUUQxUg__; IdControlDefault=NoDA; k=d0NSa2s5clVXMmNrRUtOTXk0Z3NiVTdZTWhPS241cmxQTENVcnpBRFlsYm5DRDA1K3l6NDBqMkUrRjlaV0FkOA__",
    "Host":"marianopolis.omnivox.ca",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.62 Safari/537.36"
}

headers3 = {
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Encoding":"gzip,deflate,sdch",
    "Accept-Language":"en-US,en;q=0.8",
    "Cache-Control":"max-age=0",
    "Connection":"keep-alive",
    "Cookie":"L=ANG; comn=MPOP; IsSessionInitialise=; Resolution=1280; TypeIndividu=Etudiant; UsersNbCouleurs=32; TypeProfil=; ParametresModule=H4sIAAvPxG8A/+VUXUrDQBBObJKmSO+QA4TQ9Me0D3mKfyBCsdqXEOgmDrp0s9HdjRCP4RFFvIMg6E6o4FPfCkp3YWZ2mB3mm29nDdMwjC+9UOOy0Hg1F41UUAZJxRgUilZcBmfAQdAiOKatg4hmNUzTTeBCCcrvfK+URSUYzX1vCULqsHgcDHD7XlIzVQuIOdRKEOZ78zpntLiA5rpaA4/zKCKTYnIUzkZjGExnmb/L5JmlcXY3edykKh+IAOGeE3m/oM/Q1zeXhNUwJ1RIo2N03JdtTdnok8eaMKqan3yrcKcdytz3bUX9xvCvuUqzA81WD0UHDRQWnv4iJzhFXaywna225re9YMn61P/IfkBtWV1DYz8hHNN0bO3oX1a3cAVSCaBcOY522aeESTA/dGOwOY6rfe6NBMFJCU4PX0o4HIVROD38BiX7fIWKBQAAJft8hYoFAAA=; TKINTR=6663EE079E247AF79DBC159A4B058D79A32B4C4C2A5AD834F48ACBA88FAF977D1EF103BA17B90A21F3C4B41786EABF7276356158D3C4E655AFB243479E84A92DCF9398E33EF124BBDAECCD9D573A0503E1FA6B4740A64200F918084F2D3212F30C8119AC04DC19B169552E84; TKSMPOP=OXo3dkkyTEp1YVZrTHB2UXVqdGFKTUthVGNMM0dLc2dPWWkxWXkvemxrYTFyRWxhTnB4MEFLM0pER0VLUUQxUg__; IdControlDefault=NoDA; k=d0NSa2s5clVXMmNrRUtOTXk0Z3NiVTdZTWhPS241cmxQTENVcnpBRFlsYm5DRDA1K3l6NDBqMkUrRjlaV0FkOA__",
    "Host":"marianopolis.omnivox.ca",
    "Referer":"https://marianopolis.omnivox.ca/intr/?C=MPO&E=P&L=ANG&Ref=20140104141105",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.62 Safari/537.36"     
            }

def requestStackOverFlow():
    r = requests.post('http://stackoverflow.com/search', data={'q':'python html'}) # this works
    f = open('viewcontent.html', 'w')
    f.write(r.content)
    
#requestStackOverFlow()
def makeOmnPostRequest():
    login_data = {"NoDA": "1231718", "PasswordEtu": "elgoog09", "x" : "-930", "y" : "-180", "TypeIdentification" : "Etudiant", "StatsEnvUsersResolution":"1280", "StatsEnvUsersNbCouleurs": "32" , "__VIEWSTATE" : viewstate , "k":"635244402139531250"}
    r1=s.post(url, data=login_data, headers = headers)
    f = open('viewcontent.html', 'w')
    f.write(r1.content)
    r2= s.get("https://marianopolis.omnivox.ca/intr/?C=MPO&E=P&L=ANG&Ref=20140104134109",  headers=headers2)
    print r2.cookies

    
def getOmnInfo():
    r2= s.get("https://marianopolis.omnivox.ca/intr/?C=MPO&E=P&L=ANG&Ref=20140104134109",  headers=headers2)
    r3 = s.get('https://marianopolis.omnivox.ca/intr/webpart.ajax?IdWebPart=00000000-0000-0000-0003-000000000008&L=ANG', headers=headers3)
    info = r3.content
    soup = BeautifulSoup(info)
    open('C:\Documents and Settings\Lucas\Desktop\Dropbox\COMP250\Exercise Code\infoomni.html','w').write(str(soup.prettify))
    
    test = soup.findAll('span', {"class" : "TitreQDN"})
    
    results = []
    for a in test:
        blah = re.findall('title=".+>[0-9]',str(a))[0].split('"')[1]
        results.append(blah)
    
    print results


makeOmnPostRequest()

import  requests
from bs4 import BeautifulSoup as bs
from prettytable import PrettyTable
from pymongo import MongoClient
client=MongoClient("mongodb://localhost:27017/")
db=client["ev"]
kiralik_evler=db["kiralik_evler"]
url="https://www.hepsiemlak.com/istanbul"
baslik={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"}
sayfa=requests.get(url,headers=baslik)
soup=bs(sayfa.content,"lxml")
fiyatlar=soup.find_all("span",{"class":"list-view-price"})

basliklar=soup.find_all("div",{"class":"list-view-title"})

ozellikler=soup.find_all("span",{"class":"short-property"})

konumlar=soup.find_all("span",{"class":"list-view-location"})

for i in range(len(fiyatlar)):
    baslik=basliklar[i].text.strip()
    fiyat=fiyatlar[i].text.strip().split("TL")[0]
    fiyat=fiyat.replace(".","")
    fiyat=int(fiyat)
    ozellik=" ".join(ozellikler[i].text.strip().split())
    konum=konumlar[i].text.strip()
    kiralik_evler.insert_one(
        {
            "baslik":baslik,
            "fiyat":fiyat,
            "ozellik":ozellik,
            "konum":konum
        }
    )
def min_price_home():
    fiyatlar=[i["fiyat"]  for  i in kiralik_evler.find()]
    min_price=min(fiyatlar)
    home=kiralik_evler.find_one({"fiyat":min_price})
    table=PrettyTable(["baslik","fiyat","ozellik","konum"])
    table.add_row([str(home["baslik"]),home["fiyat"],str(home["ozellik"]),str(home["konum"])])
    print(table)
def max_price_home():
    fiyatlar=[i["fiyat"]  for  i in kiralik_evler.find()]
    min_price=max(fiyatlar)
    home=kiralik_evler.find_one({"fiyat":min_price})
    table=PrettyTable(["baslik","fiyat","ozellik","konum"])
    table.add_row([str(home["baslik"]),home["fiyat"],str(home["ozellik"]),str(home["konum"])])
    print(table)
def print_home():
    evler=kiralik_evler.find()
    table=PrettyTable(["baslik","fiyat","ozellik","konum"])
    for ev in evler:
        table.add_row([str(ev["baslik"]),ev["fiyat"],str(ev["ozellik"]),str(ev["konum"])])
    print(table)
def sort_list():
    evler=kiralik_evler.find().sort("fiyat",1)
    table=PrettyTable(["baslik","fiyat","ozellik","konum"])
    for ev in evler:
        table.add_row([str(ev["baslik"]),ev["fiyat"],str(ev["ozellik"]),str(ev["konum"])])
    print(table)

icerik="""
-----------FİYAT KARŞILAŞTIRMA----------
1. En ucuz evi goster
2.En pahalı evi goster
3.butun evleri goster
4.fiyata gore sirala
5. cikis
"""
def main():
    while True:
        print(icerik)
        choice=int(input("tercihinizi giriniz :"))
        if choice==1:
            min_price_home()
        elif choice==2:
            max_price_home()
        elif choice==3:
            print_home()
        elif choice==4:
            sort_list()
        elif choice==5:
            break
        else:
            print("yanlis deger girdiniz")
if __name__=="__main__":
    main()



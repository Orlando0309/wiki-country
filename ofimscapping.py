import csv
import re
import requests
from bs4 import BeautifulSoup

class Tany:
    addresse=""
    tel_commercial=""
    prix_m2=0
    description=""
    conseiller=""
    source=""
    
class TanyScrap:
    collected=[]
    pass
        
    
    def scrap_contact(self,url,tany:Tany):
        response = requests.get(url)
        new_soup = BeautifulSoup(response.content, 'html.parser')
        
        table = new_soup.find("table",attrs={'class':'table table-striped table-bordered'})
        if table is not None:
            # Extract Conseiller immobilier
            temp_td=new_soup.find('td', text='Conseiller immobilier')
            temp_td2=new_soup.find('td', text='Tél. commercial')
            if temp_td is not None:
                tany.conseiller = temp_td.find_next_sibling('td').text
            
            if temp_td2 is not None:
                tany.tel_commercial = temp_td2.find_next_sibling('td').text
            
            if temp_td2 is None:
                contact_text = new_soup.find(text=lambda t: "contact" in t).strip()
                contact_info = contact_text.split("contact")[1].strip()
                self.tel_commercial=contact_info
                
        pass
    def get_Card(self,limit,start=0):
        print("Go on"+str(start))
        if start >=limit:
            return self.collected
        self.url="https://www.ofim.mg/recherche.html?rp=2&rr1=5&rt=3&rc1=3&start="+str(start)
        # print(self.url)
        response = requests.get(self.url)
        self.mainSoup=BeautifulSoup(response.content, 'html.parser')
        divs=self.mainSoup.find_all(name='div',attrs={'class':'list-group-item'})
        for div in divs:
            a=Tany()
            if div is not None:
                titre=div.find("h4",attrs={"class":'list-group-item-heading title'})
                link=div.find("p",attrs={'class':'list-group-item-text'})
                price=div.find("span",attrs={"class":'label label-price'})
            if titre is not None:
                a.titre= titre.get_text()
                print("Titre: " + a.titre)
            if link is not None:
                a.description = link.get_text()
                source=link.find('a')['href']
                self.scrap_contact(source,a)
                a.source=source
                # print("Description: " + a.description)
                # print("Contact: " + a.tel_commercial)
            if price is not None:
                a.prix_m2 = price.get_text()
                # print("prix_m2: " + a.prix_m2)
            self.collected.append(a)
        self.get_Card(limit,start+10)
        
                
a= TanyScrap()
a.get_Card(140,0)

csv_file = "terrains.csv"

# Write the Tany array to a CSV file
with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    
    # Write the header
    writer.writerow(["Description","Prix/m²", "Tél. commercial", "Conseiller immobilier","Source"])
    
    # Write the data rows
    for terrain in a.collected:
        writer.writerow([terrain.description, terrain.prix_m2, terrain.conseiller, terrain.tel_commercial,terrain.source])

print(f"Data has been written to {csv_file}")
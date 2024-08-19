import re
import requests
from bs4 import BeautifulSoup
# nom pays / nombre population / superficie / langueOfficielle / nom de la capitale/ habitant dans la capitale / latitude_capitale / longitude_capitale
# url = "https://fr.wikipedia.org/wiki/Japon"
# response = requests.get(url)
# #on utilise un parser HTML pour lire le contenu facilement
# soup = BeautifulSoup(response.content, 'html.parser')
# restrict = soup.find(name='div',attrs={'class':'infobox_v3 infobox infobox--frwiki noarchive'})
# # print(restrict)
# tables = restrict.find_all('table')

class Pays:
    capital = ""
    official_language = ""
    cap_latitude = ""
    latitude = ""
    cap_longitude = ""
    longitude = ""
    capital_url = ""
    capial_pop=0
    pop=0
    nomPays=""
    superficie=0
    
    def setPays(self,pays):
        self.nomPays = pays
        
    def __str__(self) -> str:
        retour = ""
        retour += f"Capitale: {self.capital}\n"
        retour += f"Langue officielle: {self.official_language}\n"
        retour += f"Latitude: {self.latitude}\n"
        retour += f"Longitude: {self.longitude}\n"
        retour += f"Cap Latitude: {self.cap_latitude}\n"
        retour += f"Cap Longitude: {self.cap_longitude}\n"
        retour += f"Cap pop: {self.capial_pop}\n"
        retour += f"pop: {self.pop}\n"
        retour += f"Sup: {self.superficie}\n"
        return retour

        
    
    def __init__(self,mainUrl):
        self.url="https://fr.wikipedia.org"+mainUrl
        # print(self.url)
        response = requests.get(self.url)
        self.mainSoup=BeautifulSoup(response.content, 'html.parser')
    
    def getLongitudeAndLatitude(self):
        span=self.mainSoup.find(name='span', attrs={'id':'coordinates'})
        if span is not None:
            map_link=span.find('a', class_='mw-kartographer-maplink')
            if map_link:
                self.latitude = map_link['data-lat']
                self.longitude = map_link['data-lon']
            else:
                        # Coordinates may be embedded directly in text
                coords_text = span.get_text()
                coords_match = re.search(r'(\d+)° (\d+\' [NS]), (\d+)° (\d+\' [EW])', coords_text)
                if coords_match:
                    lat_degrees, lat_minutes, lon_degrees, lon_minutes = coords_match.groups()
                    self.latitude = dms_to_decimal(lat_degrees, lat_minutes[:-2], lat_minutes[-1])
                    self.longitude = dms_to_decimal(lon_degrees, lon_minutes[:-2], lon_minutes[-1])
    
    def goToCapital(self):
        if self.capital_url == "":
            return
        capital_url = "https://fr.wikipedia.org" + self.capital_url  # Complete URL
        # print('cap: ',capital_url)
        capital_response = requests.get(capital_url)
        capital_soup = BeautifulSoup(capital_response.content, 'html.parser')
        
        # Find the correct table with 'Démographie' header
        table = capital_soup.find('table', attrs={'class': 'infobox_v2 infobox infobox--frwiki noarchive'})
        
        span=capital_soup.find(name='span', attrs={'id':'coordinates'})
        print(span)
        if span is not None:
            map_link=span.find('a', class_='mw-kartographer-maplink')
            if map_link:
                self.cap_latitude = map_link['data-lat']
                self.cap_longitude = map_link['data-lon']
            else:
                            # Coordinates may be embedded directly in text
                coords_text = span.get_text()
                coords_match = re.search(r'(\d+)° (\d+\' [NS]), (\d+)° (\d+\' [EW])', coords_text)
                if coords_match:
                    lat_degrees, lat_minutes, lon_degrees, lon_minutes = coords_match.groups()
                    self.cap_latitude = dms_to_decimal(lat_degrees, lat_minutes[:-2], lat_minutes[-1])
                    self.cap_longitude = dms_to_decimal(lon_degrees, lon_minutes[:-2], lon_minutes[-1])
        if not table:
            return
        
        print("ato")
        # Check if the table has the 'Démographie' section
        # demography,geo = self.getSection('Démographie',capital_soup),self.getSection('Géographie',capital_soup)

        # if not demography:
        #     raise ValueError("No 'Démographie' section found.")
        
        # Find and process the population row
        last =None
        for row in table.find_all('tr'):
            header = row.find('th')
            data = row.find('td')
            if header and data:
                header_text = header.get_text(strip=True)
                if "Population"  in header_text or ("" in header_text and last == "Gentilé"):
                    text = data.get_text(separator=' ').strip()
                    text = text.replace('\xa0', '')  # Remove non-breaking spaces
                    # Extract the number using regex
                    number_match = re.search(r'\d+', text)
                    if number_match:
                        number = number_match.group()  # Extracts the number as a string
                        capital_pop = number  # Prints population
                        # print(capital_pop)
                        self.capial_pop=capital_pop
                if "Coordonnées" in header_text:
                    map_link=data.find('a', class_='mw-kartographer-maplink')
                    if map_link:
                        self.cap_latitude = map_link['data-lat']
                        self.cap_longitude = map_link['data-lon']
                last=header_text
       
        
            

    def getPopulations(self):
        demography = self.getSection('Démographie')
        if not demography:
            return
        
        # Find and process the population row
        last =None
        for row in demography.find_all('tr'):
            header = row.find('th')
            data = row.find('td')
            if header and data:
                header_text = header.get_text(strip=True)
                if "Population totale"  in header_text or ("" in header_text and last == "Gentilé"):
                    text = data.get_text(separator=' ').strip()
                    text = text.replace('\xa0', '')  # Remove non-breaking spaces
                    # Extract the number using regex
                    number_match = re.search(r'\d+', text)
                    if number_match:
                        number = number_match.group()  # Extracts the number as a string
                        capital_pop = number  # Prints population
                        # print(capital_pop)
                        self.pop=capital_pop
                    
                last=header_text
    def getOffical_LanguageAndCapital(self):
        admin_table,geo=self.getSection('Administration'),self.getSection('Géographie')
        
        if not admin_table or not geo:
            # admin_table=self.getSectionCap('Adminis')
            return
            # raise ValueError("No table with the caption 'Administration' found.")
        
        for row in admin_table.find_all('tr'):
            header = row.find('th')
            data = row.find('td')
            # print(data)

            if header and data:
                header_text = header.get_text(strip=True)

                if "Capitale" in header_text:
                    self.capital = data.find('a').get_text(strip=True)
                    self.capital_url = data.find('a')['href']  # Get the link to the capital page
                    # map_link = data.find('p').find('a', class_='mw-kartographer-maplink')
                    # if map_link:
                    #     self.cap_latitude = map_link['data-lat']
                    #     self.cap_longitude = map_link['data-lon']
                    # else:
                    #     # Coordinates may be embedded directly in text
                    #     coords_text = data.get_text()
                    #     coords_match = re.search(r'(\d+)° (\d+\' [NS]), (\d+)° (\d+\' [EW])', coords_text)
                    #     if coords_match:
                    #         lat_degrees, lat_minutes, lon_degrees, lon_minutes = coords_match.groups()
                    #         self.cap_latitude = dms_to_decimal(lat_degrees, lat_minutes[:-2], lat_minutes[-1])
                    #         self.cap_longitude = dms_to_decimal(lon_degrees, lon_minutes[:-2], lon_minutes[-1])
                elif "Langues officielles" in header_text or "Langue officielle" in header_text:
                    self.official_language = data.get_text(strip=True)
        for row in geo.find_all('tr'):
            header = row.find('th')
            data = row.find('td')
            if header and data:
                header_text = header.get_text(strip=True)
                if "Superficie totale" in header_text:
                    superficie = data.get_text(separator=' ').strip()
                    self.superficie = toNumber(superficie)
            
    
    def getSection(self,name,soup=None):
        admin_table = None
        s=soup
        if soup is None:
            s = self.mainSoup
        for table in s.find_all('table'):
            caption = table.find('caption')
            if caption and caption.get_text(strip=True) == name:
                admin_table = table
                break
        return admin_table
    def getSectionCap(self,name,soup=None):
        admin_table = None
        s=soup
        if soup is None:
            s = self.mainSoup
        for table in s.find_all('table'):
            caption = table.find('caption')
            if caption and caption.get_text(strip=True) == name:
                admin_table = table
                break
        return admin_table
    
    
def dms_to_decimal(degrees, minutes, direction):
    decimal = float(degrees.replace('\'','')) + float(minutes.replace('\'','')) / 60
    if direction in ['S', 'W']:
        decimal = -decimal
    return decimal
def toNumber(text):
    text = text.replace('\xa0', '')  # Remove non-breaking spaces
                    # Extract the number using regex
    number_match = re.search(r'\d+', text)
    if number_match:
        number = number_match.group()  # Extracts the number as a string
        return number  # Prints population
    return 0


from flask import Flask, render_template, request
import sqlite3
from scrapper import Pays
app = Flask(__name__)

# Function to get a list of countries from the database
def get_countries():
    conn = sqlite3.connect('countries.db')
    c = conn.cursor()
    c.execute('SELECT nom FROM pays')
    countries = c.fetchall()
    conn.close()
    return [country[0] for country in countries]

def scrape_country_info(country_name:str):
    p=country_name.replace(' ','_')
    a = Pays(f'/wiki/{p}')
    a.getLongitudeAndLatitude()
    a.getOffical_LanguageAndCapital()
    a.getPopulations()
    a.goToCapital()
    
    return a

@app.route('/')
def select_country():
    countries = get_countries()
    return render_template('select_country.html', countries=countries)

@app.route('/country_info', methods=['POST'])
def country_info():
    country_name = request.form['country']
    info = scrape_country_info(country_name)
    print(info)
    return render_template('display_country.html', country_name=country_name, info=info)

if __name__ == '__main__':
    app.run(debug=True)
# Country Information Web App
## Overview

This project is a mini-site built with Flask and SQLite that displays detailed information about countries fetched via web scraping. Users can select a country from a dropdown menu and view comprehensive details about it, including a map centered on the capital city.

## Features

- **Country Selection**: Choose a country from a dropdown menu.
- **Detailed Information**: View detailed country information such as capital, official language, population, and area.
- **Interactive Map**: See a map centered on the capital city using OpenStreetMap and Leaflet.

## Setup

### 1. Clone the Repository

To get started, clone the repository to your local machine:

```bash
git clone https://github.com/Orlando0309/wiki-country.git
cd wiki-country
```

### 2. Install Dependencies

Ensure you have `pip` installed. Then, install the necessary Python packages:

```bash
pip install -r requirements.txt
```

### 3. Create the Database

Initialize the SQLite database and create the required tables by running:

```bash
python create_db.py
```

This script will set up the database and create the `pays` table.

## Usage

### 1. Running the Web App

Start the Flask web server by running:

```bash
python app.py
```

Open your web browser and navigate to `http://127.0.0.1:5000` to access the application.

### 2. Functionality

- **Home Page**: Select a country from the dropdown menu and submit the form.
- **Country Information Page**: View detailed information about the selected country, including a map centered on the capital city.

## Code Overview

- **`app.py`**: The main Flask application file containing routes for the country selection page and the country information page.
- **`create_db.py`**: Script to initialize the SQLite database and create the `pays` table.
- **`scrape.py`**: Handles web scraping to retrieve country information from Wikipedia.
- **Templates**: HTML files for rendering the country selection form and the country information page with a map.

## Requirements

The required Python packages are listed in the `requirements.txt` file. These include:

- `Flask`: Web framework for the application.
- `requests`: For making HTTP requests to scrape country information.
- `beautifulsoup4`: For parsing HTML content.
- `leaflet`: For embedding interactive maps (included via CDN).

## Contributing

Contributions are welcome! If you have suggestions for improvements or new features, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
